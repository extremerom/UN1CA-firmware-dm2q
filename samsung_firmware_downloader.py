#!/usr/bin/env python3
"""
Samsung Firmware Downloader - Complete Implementation
======================================================
Downloads Samsung firmware directly from official FOTA servers.
Uses the complete Samsung FUS (Firmware Update Server) protocol.

Based on reverse engineering of:
- FotaAgent.apk from system/system/priv-app/FotaAgent/
- Samsung FUS protocol analysis
- Device info: SM-S916B, TPA region, Serial: CE0523757243B468157E

This implementation uses external dependencies for cryptography and HTTP requests
to properly implement the Samsung authentication protocol.

Author: Analyzed from firmware binaries, APKs and protocol reverse engineering
License: MIT
"""

import argparse
import base64
import hashlib
import os
import sys
import xml.etree.ElementTree as ET
from typing import Optional, Dict

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required.")
    print("Install it with: pip install requests")
    sys.exit(1)

try:
    from Cryptodome.Cipher import AES
except ImportError:
    try:
        from Crypto.Cipher import AES
    except ImportError:
        print("Error: 'pycryptodome' library is required.")
        print("Install it with: pip install pycryptodome")
        sys.exit(1)


# Samsung FUS Authentication Keys (extracted from FotaAgent.apk analysis)
KEY_1 = "hqzdurufm2c8mf6bsjezu1qgveouv7c7"  # Primary key for NONCE decryption
KEY_2 = "w13r4cvf4hctaujv"                  # Secondary key for auth signature


def pkcs7_unpad(data: bytes) -> bytes:
    """Remove PKCS#7 padding"""
    pad_len = data[-1]
    return data[:-pad_len]


def pkcs7_pad(data: bytes) -> bytes:
    """Add PKCS#7 padding"""
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len]) * pad_len


def aes_encrypt(data: bytes, key: bytes) -> bytes:
    """Perform AES-CBC encryption"""
    iv = key[:16]  # IV is first 16 bytes of key
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pkcs7_pad(data))


def aes_decrypt(data: bytes, key: bytes) -> bytes:
    """Perform AES-CBC decryption"""
    iv = key[:16]  # IV is first 16 bytes of key
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return pkcs7_unpad(cipher.decrypt(data))


def derive_key(nonce: str) -> bytes:
    """Calculate the AES key from the FUS input nonce"""
    key = ""
    # First 16 bytes are offsets into KEY_1
    for i in range(16):
        key += KEY_1[ord(nonce[i]) % 16]
    # Last 16 bytes are static KEY_2
    key += KEY_2
    return key.encode()


def get_auth_signature(nonce: str) -> str:
    """Calculate the auth signature from a given nonce"""
    nkey = derive_key(nonce)
    auth_data = aes_encrypt(nonce.encode(), nkey)
    return base64.b64encode(auth_data).decode()


def decrypt_nonce(encrypted_nonce: str) -> str:
    """Decrypt the nonce returned by the server"""
    data = base64.b64decode(encrypted_nonce)
    nonce = aes_decrypt(data, KEY_1.encode()).decode()
    return nonce


class SamsungFUSClient:
    """
    Samsung FUS (Firmware Update Server) Client
    Implements the complete authentication and download protocol
    """
    
    # Samsung FUS Server URLs
    FUS_SERVER = "https://neofussvr.sslcs.cdngc.net"
    FUS_CLOUD_SERVER = "http://cloud-neofussvr.sslcs.cdngc.net"
    FOTA_CLOUD_SERVER = "https://fota-cloud-dn.ospserver.net/firmware"
    
    def __init__(self, model: str, region: str):
        """
        Initialize FUS client
        
        Args:
            model: Device model (e.g., SM-S916B)
            region: CSC region code (e.g., TPA, OXM)
        """
        self.model = model.upper()
        self.region = region.upper()
        self.auth = ""
        self.sessid = ""
        self.nonce = ""
        self.encnonce = ""
        
        # Initialize session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Kies2.0_FUS',
            'Cache-Control': 'no-cache'
        })
        
        print("[*] Initializing FUS client...")
        self._init_nonce()
    
    def _init_nonce(self):
        """Initialize NONCE from FUS server"""
        try:
            print("[*] Requesting NONCE from FUS server...")
            self._makereq("NF_DownloadGenerateNonce.do")
            if self.nonce and len(self.nonce) >= 16:
                print(f"[+] NONCE initialized successfully")
                print(f"[*] Session ID: {self.sessid[:20]}..." if self.sessid else "[*] No session ID")
            else:
                print(f"[!] Warning: NONCE not properly initialized (len={len(self.nonce) if self.nonce else 0})")
                print("[*] Will try FOTA cloud method instead")
        except Exception as e:
            print(f"[!] Error initializing NONCE: {e}")
            print("[*] FUS server authentication failed")
            print("[*] Will use FOTA cloud for firmware check (no download)")
    
    def _makereq(self, path: str, data: str = "") -> str:
        """
        Make a FUS request to given endpoint
        
        Args:
            path: API endpoint path
            data: Request body data
            
        Returns:
            Response text
        """
        # Build authorization header
        authv = f'FUS nonce="", signature="{self.auth}", nc="", type="", realm="", newauth="1"'
        
        url = f"{self.FUS_SERVER}/{path}"
        headers = {
            "Authorization": authv,
            "User-Agent": "Kies2.0_FUS"
        }
        
        cookies = {}
        if self.sessid:
            cookies["JSESSIONID"] = self.sessid
        
        try:
            req = self.session.post(url, data=data, headers=headers, cookies=cookies, timeout=30)
            
            # Update NONCE if present
            if "NONCE" in req.headers:
                self.encnonce = req.headers["NONCE"]
                if self.encnonce:
                    try:
                        self.nonce = decrypt_nonce(self.encnonce)
                        if self.nonce and len(self.nonce) >= 16:
                            self.auth = get_auth_signature(self.nonce)
                            print(f"[*] Updated NONCE and auth signature")
                    except Exception as e:
                        print(f"[!] Error processing NONCE: {e}")
            
            # Update session cookie
            if "JSESSIONID" in req.cookies:
                self.sessid = req.cookies["JSESSIONID"]
            
            req.raise_for_status()
            return req.text
            
        except requests.exceptions.RequestException as e:
            print(f"[!] Request error: {e}")
            raise
    
    def check_firmware_fota(self) -> Optional[Dict[str, str]]:
        """
        Check firmware using FOTA cloud server (simple HTTP/XML)
        This is faster and doesn't require FUS authentication
        
        Returns:
            Firmware information dictionary
        """
        print(f"\n[*] Checking firmware via FOTA cloud for {self.model} ({self.region})...")
        
        url = f"{self.FOTA_CLOUD_SERVER}/{self.region}/{self.model}/version.xml"
        print(f"[*] URL: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"[!] FOTA cloud returned status {response.status_code}")
                return None
            
            # Parse XML
            root = ET.fromstring(response.content)
            latest = root.find('.//latest')
            
            if latest is None:
                print("[!] No firmware version found")
                return None
            
            firmware_version = latest.text
            android_version = latest.get('o', 'Unknown')
            
            # Parse version string
            parts = firmware_version.split('/')
            pda = parts[0] if len(parts) > 0 else ''
            csc = parts[1] if len(parts) > 1 else ''
            modem = parts[2] if len(parts) > 2 else ''
            
            firmware_info = {
                'version': firmware_version,
                'pda': pda,
                'csc': csc,
                'modem': modem,
                'android': android_version,
                'model': self.model,
                'region': self.region
            }
            
            print(f"[+] Firmware found: {firmware_version}")
            print(f"[*] Android version: {android_version}")
            
            return firmware_info
            
        except Exception as e:
            print(f"[!] Error checking FOTA cloud: {e}")
            return None
    
    def get_binary_info(self, firmware_version: str) -> Optional[Dict[str, str]]:
        """
        Get binary download information from FUS server
        
        Args:
            firmware_version: Firmware version string (PDA/CSC/MODEM)
            
        Returns:
            Binary information dictionary
        """
        print(f"\n[*] Getting binary info from FUS server...")
        print(f"[*] Firmware version: {firmware_version}")
        
        # Parse firmware version
        parts = firmware_version.split('/')
        if len(parts) < 1:
            print("[!] Invalid firmware version format")
            return None
        
        # Build request XML
        xml_data = f"""<?xml version="1.0" encoding="utf-8"?>
<FUSMsg>
  <FUSHdr>
    <ProtoVer>1.0</ProtoVer>
  </FUSHdr>
  <FUSBody>
    <Put>
      <ACCESS_MODE><Data>2</Data></ACCESS_MODE>
      <BINARY_NATURE><Data>1</Data></BINARY_NATURE>
      <CLIENT_PRODUCT><Data>Smart Switch</Data></CLIENT_PRODUCT>
      <DEVICE_FW_VERSION><Data>{firmware_version}</Data></DEVICE_FW_VERSION>
      <DEVICE_LOCAL_CODE><Data>{self.region}</Data></DEVICE_LOCAL_CODE>
      <DEVICE_MODEL_NAME><Data>{self.model}</Data></DEVICE_MODEL_NAME>
      <LOGIC_CHECK><Data>Y</Data></LOGIC_CHECK>
    </Put>
  </FUSBody>
</FUSMsg>"""
        
        try:
            response = self._makereq("NF_DownloadBinaryInform.do", xml_data)
            
            # Parse response XML
            root = ET.fromstring(response)
            
            # Extract binary information
            binary_name = self._get_xml_value(root, 'BINARY_NAME')
            binary_size = self._get_xml_value(root, 'BINARY_SIZE')
            filename = self._get_xml_value(root, 'BINARY_CRC')
            path = self._get_xml_value(root, 'MODEL_PATH')
            logic_value = self._get_xml_value(root, 'LOGIC_VALUE_FACTORY')
            
            if not binary_name:
                print("[!] No binary name in response")
                print(f"[*] Response: {response[:500]}")
                return None
            
            binary_info = {
                'filename': binary_name,
                'size': binary_size,
                'path': path,
                'crc': filename,
                'logic_value': logic_value,
                'version': firmware_version
            }
            
            size_mb = int(binary_size) / (1024 * 1024) if binary_size.isdigit() else 0
            print(f"[+] Binary found: {binary_name}")
            print(f"[*] Size: {size_mb:.2f} MB")
            print(f"[*] Path: {path}")
            
            return binary_info
            
        except Exception as e:
            print(f"[!] Error getting binary info: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _get_xml_value(self, root: ET.Element, tag: str) -> str:
        """Extract value from FUS XML response"""
        elem = root.find(f".//{tag}/Data")
        return elem.text if elem is not None and elem.text else ""
    
    def download_binary(self, binary_info: Dict[str, str], output_dir: str = ".") -> bool:
        """
        Download binary file from FUS cloud server
        
        Args:
            binary_info: Binary information from get_binary_info()
            output_dir: Output directory
            
        Returns:
            True if successful
        """
        filename = binary_info.get('filename', '')
        path = binary_info.get('path', '')
        size = binary_info.get('size', '0')
        
        if not filename:
            print("[!] No filename provided")
            return False
        
        output_file = os.path.join(output_dir, filename)
        total_size = int(size) if size.isdigit() else 0
        
        print(f"\n[*] Downloading: {filename}")
        print(f"[*] Output: {output_file}")
        print(f"[*] Size: {total_size / (1024*1024):.2f} MB")
        
        # Initialize download
        print("[*] Initializing download...")
        init_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<FUSMsg>
  <FUSHdr>
    <ProtoVer>1.0</ProtoVer>
  </FUSHdr>
  <FUSBody>
    <Put>
      <BINARY_FILE_NAME><Data>{filename}</Data></BINARY_FILE_NAME>
      <LOGIC_CHECK><Data>Y</Data></LOGIC_CHECK>
    </Put>
  </FUSBody>
</FUSMsg>"""
        
        try:
            self._makereq("NF_DownloadBinaryInitForMass.do", init_xml)
            print("[+] Download initialized")
        except Exception as e:
            print(f"[!] Error initializing download: {e}")
            return False
        
        # Download file
        download_url = f"{self.FUS_CLOUD_SERVER}/NF_DownloadBinaryForMass.do?file={path}/{filename}"
        print(f"[*] Download URL: {download_url[:80]}...")
        
        # Build authorization for cloud download
        authv = f'FUS nonce="{self.encnonce}", signature="{self.auth}", nc="", type="", realm="", newauth="1"'
        headers = {
            "Authorization": authv,
            "User-Agent": "Kies2.0_FUS"
        }
        
        try:
            print("[*] Starting download...")
            response = self.session.get(download_url, headers=headers, stream=True, timeout=60)
            response.raise_for_status()
            
            downloaded = 0
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r[*] Progress: {progress:.1f}% ({downloaded / (1024*1024):.2f} MB)", end='', flush=True)
            
            print(f"\n[+] Download completed: {output_file}")
            
            # Verify size
            actual_size = os.path.getsize(output_file)
            if total_size > 0 and actual_size != total_size:
                print(f"[!] Warning: Size mismatch. Expected: {total_size}, Got: {actual_size}")
            
            return True
            
        except Exception as e:
            print(f"\n[!] Download error: {e}")
            if os.path.exists(output_file):
                os.remove(output_file)
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Samsung Firmware Downloader - Complete FUS Protocol Implementation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Check and download firmware for SM-S916B (TPA region - Caribbean)
  python3 %(prog)s -m SM-S916B -r TPA
  
  # Download to specific directory
  python3 %(prog)s -m SM-S916B -r TPA -o ./firmwares
  
  # Check only (no download)
  python3 %(prog)s -m SM-S916B -r TPA --check-only

Device Information (from system analysis):
  Model: SM-S916B
  Region: TPA (Caribbean - Flow/Digicel)
  Serial: CE0523757243B468157E
  Boot ID: 8df0c594-9852-48ff-a649-4d6824eb9fbb
  
Common CSC Codes:
  TPA - Caribbean (Flow, Digicel)
  OXM - Open Europe
  BTU - United Kingdom
  DBT - Germany
  XEF - France
        '''
    )
    
    parser.add_argument('-m', '--model', required=True,
                        help='Device model (e.g., SM-S916B)')
    parser.add_argument('-r', '--region', required=True,
                        help='CSC region code (e.g., TPA, OXM)')
    parser.add_argument('-o', '--output', default='.',
                        help='Output directory (default: current directory)')
    parser.add_argument('--check-only', action='store_true',
                        help='Only check firmware, do not download')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Samsung FUS Firmware Downloader")
    print("Complete Protocol Implementation with Dependencies")
    print("=" * 70)
    print(f"Model: {args.model}")
    print(f"Region: {args.region}")
    print(f"Output: {args.output}")
    print("=" * 70)
    
    # Create output directory
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    try:
        # Initialize FUS client
        client = SamsungFUSClient(args.model, args.region)
        
        # Check firmware via FOTA cloud (fast)
        firmware_info = client.check_firmware_fota()
        
        if not firmware_info:
            print("\n[!] No firmware found")
            return 1
        
        if args.check_only:
            print("\n[*] Check-only mode. Not downloading.")
            return 0
        
        # Get binary info via FUS
        binary_info = client.get_binary_info(firmware_info['version'])
        
        if not binary_info:
            print("\n[!] Could not get binary download information")
            print("[*] Firmware exists but download may not be available via FUS")
            return 1
        
        # Download firmware
        success = client.download_binary(binary_info, args.output)
        
        if success:
            print("\n[+] Firmware downloaded successfully!")
            return 0
        else:
            print("\n[!] Download failed")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

    """Samsung Firmware Downloader using official FOTA API"""
    
    # Samsung FOTA Server URLs
    FOTA_CHECK_URL = "https://fota-cloud-dn.ospserver.net/firmware/{region}/{model}/version.xml"
    FOTA_BINARY_INFO_URL = "https://neofussvr.sslcs.cdngc.net/NF_DownloadBinaryInform"
    FOTA_BINARY_INIT_URL = "https://neofussvr.sslcs.cdngc.net/NF_DownloadBinaryInitForMass"
    FOTA_DOWNLOAD_URL = "http://cloud-neofussvr.sslcs.cdngc.net/NF_DownloadBinaryForMass"
    
    # Nonce generation key for authentication
    # NOTE: This is a public key extracted from Samsung's FotaAgent.apk
    # It is not a secret and is the same across all Samsung devices
    NONCE_KEY = "hqzdurufm2c8mf6bsjezu1qgveouv7c7"
    
    def __init__(self, model: str, region: str, imei: str = None):
        """
        Initialize Samsung Firmware Downloader
        
        Args:
            model: Device model (e.g., SM-S916B)
            region: CSC region code (e.g., OXM, BTU, DBT)
            imei: Device IMEI (optional, can be generated)
        """
        self.model = model
        self.region = region
        self.imei = imei or self._generate_imei()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Kies2.0_FUS',
            'Cache-Control': 'no-cache'
        })
        
    def _generate_imei(self) -> str:
        """Generate a valid IMEI for authentication"""
        # Generate a valid IMEI with proper check digit
        imei_base = "35999900"  # TAC for Samsung
        # Add random serial number
        serial = str(random.randint(100000, 999999))
        imei_without_check = imei_base + serial
        
        # Calculate Luhn check digit
        digits = [int(d) for d in imei_without_check]
        check_sum = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            check_sum += digit
        check_digit = (10 - (check_sum % 10)) % 10
        
        return imei_without_check + str(check_digit)
    
    def _generate_nonce(self, input_data: str) -> str:
        """
        Generate authentication nonce for Samsung API
        
        Args:
            input_data: Input string to hash
            
        Returns:
            HMAC-SHA256 hash in uppercase
        """
        nonce = hmac.new(
            self.NONCE_KEY.encode(),
            input_data.encode(),
            hashlib.sha256
        ).hexdigest().upper()
        return nonce
    
    def _create_request_xml(self, request_type: str, **params) -> str:
        """Create XML request for Samsung API"""
        root = ET.Element('FUSMsg')
        
        # Add header
        header = ET.SubElement(root, 'FUSHdr')
        ET.SubElement(header, 'ProtoVer').text = '1.0'
        
        # Add body
        body = ET.SubElement(root, 'FUSBody')
        ET.SubElement(body, 'Put')
        
        # Add access info
        access = ET.SubElement(body, 'ACCESS_MODE')
        ET.SubElement(access, 'Data').text = '2'
        
        # Add NONCE for authentication
        nonce_data = f"{self.imei}:{self.model}:{self.region}"
        nonce = ET.SubElement(body, 'NONCE')
        ET.SubElement(nonce, 'Data').text = self._generate_nonce(nonce_data)
        
        # Add model info
        model_path = ET.SubElement(body, 'MODEL_PATH')
        ET.SubElement(model_path, 'Data').text = self.model
        
        # Add additional parameters
        for key, value in params.items():
            elem = ET.SubElement(body, key)
            ET.SubElement(elem, 'Data').text = str(value)
        
        return ET.tostring(root, encoding='utf-8', method='xml').decode()
    
    def check_latest_firmware(self) -> Optional[Dict[str, str]]:
        """
        Check for latest firmware version
        
        Returns:
            Dictionary with firmware info or None if not found
        """
        print(f"[*] Checking latest firmware for {self.model} ({self.region})...")
        
        # Try direct version.xml check
        version_url = self.FOTA_CHECK_URL.format(region=self.region, model=self.model)
        try:
            response = self.session.get(version_url, timeout=10)
            if response.status_code == 200:
                # Parse version info
                root = ET.fromstring(response.content)
                firmware_info = {
                    'version': root.findtext('.//version', 'Unknown'),
                    'size': root.findtext('.//size', 'Unknown'),
                    'description': root.findtext('.//description', '')
                }
                return firmware_info
        except Exception as e:
            print(f"[!] Direct version check failed: {e}")
        
        return None
    
    def get_binary_info(self, firmware_version: str = None) -> Optional[Dict[str, str]]:
        """
        Get binary information from Samsung servers
        
        Args:
            firmware_version: Specific firmware version to query (optional)
            
        Returns:
            Dictionary with firmware details
        """
        print("[*] Querying Samsung FOTA servers for firmware information...")
        
        # Prepare request
        params = {
            'DEVICE_IMEI_PUSH': self.imei,
            'DEVICE_MODEL_NAME': self.model,
            'DEVICE_CSC_CODE2': self.region,
            'DEVICE_CONTENTS_DATA_VERSION': '1'
        }
        
        if firmware_version:
            params['DEVICE_FW_VERSION'] = firmware_version
        
        xml_request = self._create_request_xml('BinaryInform', **params)
        
        try:
            response = self.session.post(
                self.FOTA_BINARY_INFO_URL,
                data=xml_request,
                headers={'Content-Type': 'text/xml'},
                timeout=30
            )
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                
                # Extract firmware information
                firmware_info = {
                    'version': self._get_xml_value(root, 'LATEST_FW_VERSION'),
                    'filename': self._get_xml_value(root, 'BINARY_NAME'),
                    'size': self._get_xml_value(root, 'BINARY_SIZE'),
                    'path': self._get_xml_value(root, 'MODEL_PATH'),
                    'description': self._get_xml_value(root, 'DESCRIPTION'),
                    'decrypt_key': self._get_xml_value(root, 'LOGIC_VALUE_FACTORY')
                }
                
                # Check if firmware is available
                status = self._get_xml_value(root, 'RESULT_CODE')
                if status == '200':
                    return firmware_info
                else:
                    print(f"[!] Server returned status: {status}")
                    return None
            elif response.status_code == 404:
                print(f"[!] Firmware not found (404). Please verify model ({self.model}) and region ({self.region}).")
                return None
            elif response.status_code == 401:
                print("[!] Authentication failed (401). The IMEI or authentication may be invalid.")
                return None
            elif response.status_code >= 500:
                print(f"[!] Server error ({response.status_code}). Samsung servers may be down. Try again later.")
                return None
            else:
                print(f"[!] Unexpected response status: {response.status_code}")
                return None
                    
        except requests.exceptions.Timeout:
            print("[!] Request timed out. Check your internet connection or try again later.")
        except requests.exceptions.ConnectionError:
            print("[!] Connection error. Check your internet connection.")
        except ET.ParseError as e:
            print(f"[!] Error parsing XML response: {e}")
        except Exception as e:
            print(f"[!] Error querying firmware info: {e}")
            
        return None
    
    def _get_xml_value(self, root: ET.Element, tag: str) -> str:
        """Extract value from XML response"""
        elem = root.find(f".//{tag}/Data")
        return elem.text if elem is not None and elem.text else ""
    
    def download_firmware(self, firmware_info: Dict[str, str], output_path: str = ".") -> bool:
        """
        Download firmware binary from Samsung servers
        
        Args:
            firmware_info: Firmware information from get_binary_info()
            output_path: Directory to save the firmware file
            
        Returns:
            True if successful, False otherwise
        """
        filename = firmware_info.get('filename', 'firmware.bin')
        if not filename:
            print("[!] No filename provided in firmware info")
            return False
            
        output_file = os.path.join(output_path, filename)
        size_str = firmware_info.get('size', '0')
        
        try:
            total_size = int(size_str)
        except ValueError:
            print(f"[!] Invalid size: {size_str}")
            total_size = 0
        
        print(f"[*] Downloading firmware: {filename}")
        print(f"[*] Size: {total_size / (1024*1024):.2f} MB")
        print(f"[*] Version: {firmware_info.get('version', 'Unknown')}")
        
        # Initialize download session
        init_xml = self._create_request_xml(
            'BinaryInit',
            DEVICE_IMEI_PUSH=self.imei,
            BINARY_NAME=filename,
            BINARY_SIZE=size_str
        )
        
        try:
            response = self.session.post(
                self.FOTA_BINARY_INIT_URL,
                data=init_xml,
                headers={'Content-Type': 'text/xml'},
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"[!] Failed to initialize download: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[!] Error initializing download: {e}")
            return False
        
        # Download the firmware file
        print(f"[*] Starting download to: {output_file}")
        
        download_url = f"{self.FOTA_DOWNLOAD_URL}.do?file={firmware_info.get('path', '')}/{filename}"
        
        try:
            response = self.session.get(download_url, stream=True, timeout=60)
            
            if response.status_code != 200:
                print(f"[!] Download failed: HTTP {response.status_code}")
                return False
            
            # Download with progress
            downloaded = 0
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r[*] Progress: {progress:.1f}% ({downloaded / (1024*1024):.2f} MB)", end='')
            
            print(f"\n[+] Download completed: {output_file}")
            
            # Verify file size
            actual_size = os.path.getsize(output_file)
            if total_size > 0 and actual_size != total_size:
                print(f"[!] Warning: File size mismatch. Expected: {total_size}, Got: {actual_size}")
            
            return True
            
        except Exception as e:
            print(f"\n[!] Error during download: {e}")
            if os.path.exists(output_file):
                os.remove(output_file)
            return False
    
    def decrypt_firmware(self, encrypted_file: str, output_file: str, decrypt_key: str) -> bool:
        """
        Decrypt firmware file (if encrypted)
        
        Note: Samsung firmware encryption varies by device and version.
        This is a placeholder for decryption logic.
        
        Args:
            encrypted_file: Path to encrypted firmware
            output_file: Path to save decrypted firmware
            decrypt_key: Decryption key from firmware info
            
        Returns:
            True if successful, False otherwise
        """
        print("[*] Note: Firmware decryption may require device-specific keys")
        print("[*] Most modern Samsung firmwares are delivered pre-decrypted")
        
        # Basic implementation - copy file if no encryption needed
        if not decrypt_key or decrypt_key == "0":
            print("[*] No decryption required")
            return True
        
        print("[!] Firmware decryption not implemented for this key type")
        print(f"[*] Decrypt key provided: {decrypt_key}")
        return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Samsung Firmware Downloader - Download firmware from Samsung FOTA servers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Download latest firmware for Samsung Galaxy S23+ (Europe)
  python samsung_firmware_downloader.py -m SM-S916B -r OXM
  
  # Download firmware with custom IMEI
  python samsung_firmware_downloader.py -m SM-S916B -r OXM -i 123456789012345
  
  # Download to specific directory
  python samsung_firmware_downloader.py -m SM-S916B -r OXM -o /path/to/output
  
Common CSC Codes:
  OXM - Open Europe (Multi-CSC)
  BTU - United Kingdom
  DBT - Germany
  XEF - France
  XAR - USA (AT&T)
  TMB - USA (T-Mobile)
  SPR - USA (Sprint)
  VZW - USA (Verizon)
  
Model Examples:
  SM-S916B - Galaxy S23+
  SM-S918B - Galaxy S23 Ultra
  SM-S911B - Galaxy S23
  SM-S926B - Galaxy S24+
  SM-S928B - Galaxy S24 Ultra
        '''
    )
    
    parser.add_argument('-m', '--model', required=True,
                        help='Device model (e.g., SM-S916B)')
    parser.add_argument('-r', '--region', required=True,
                        help='CSC region code (e.g., OXM, BTU, DBT)')
    parser.add_argument('-i', '--imei',
                        help='Device IMEI (optional, will be generated if not provided)')
    parser.add_argument('-v', '--version',
                        help='Specific firmware version to download (optional)')
    parser.add_argument('-o', '--output', default='.',
                        help='Output directory for downloaded firmware (default: current directory)')
    parser.add_argument('--check-only', action='store_true',
                        help='Only check for firmware availability, do not download')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    print("=" * 70)
    print("Samsung Firmware Downloader")
    print("=" * 70)
    print(f"Model: {args.model}")
    print(f"Region: {args.region}")
    if args.imei:
        print(f"IMEI: {args.imei}")
    print(f"Output: {args.output}")
    print("=" * 70)
    print()
    
    # Initialize downloader
    downloader = SamsungFirmwareDownloader(
        model=args.model,
        region=args.region,
        imei=args.imei
    )
    
    # Check for latest firmware
    firmware_info = downloader.check_latest_firmware()
    if firmware_info:
        print(f"[+] Latest firmware version: {firmware_info.get('version', 'Unknown')}")
    
    # Get detailed binary information
    binary_info = downloader.get_binary_info(firmware_version=args.version)
    
    if not binary_info:
        print("[!] No firmware found for the specified device")
        print("[*] Possible reasons:")
        print("    - Invalid model or region code")
        print("    - Device not supported by Samsung FOTA servers")
        print("    - Network connectivity issues")
        return 1
    
    print("[+] Firmware found:")
    print(f"    Version: {binary_info.get('version', 'Unknown')}")
    print(f"    Filename: {binary_info.get('filename', 'Unknown')}")
    print(f"    Size: {int(binary_info.get('size', 0)) / (1024*1024):.2f} MB")
    if binary_info.get('description'):
        print(f"    Description: {binary_info.get('description')}")
    
    if args.check_only:
        print("\n[*] Check-only mode enabled. Exiting without download.")
        return 0
    
    print()
    
    # Download firmware
    success = downloader.download_firmware(binary_info, args.output)
    
    if success:
        print("\n[+] Firmware download completed successfully!")
        print(f"[*] File saved to: {os.path.join(args.output, binary_info.get('filename', 'firmware.bin'))}")
        return 0
    else:
        print("\n[!] Firmware download failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
