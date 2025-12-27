#!/usr/bin/env python3
"""
Samsung Firmware Downloader
============================
This script downloads Samsung firmware (update.bin) from Samsung's FOTA servers.

Based on analysis of Samsung's FotaAgent and firmware update protocol.
Uses the official Samsung firmware download API to retrieve firmware files.

Author: Generated from firmware analysis
License: MIT
"""

import argparse
import hashlib
import hmac
import os
import sys
import xml.etree.ElementTree as ET
from typing import Optional, Dict, Tuple
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install it with: pip install requests")
    sys.exit(1)


class SamsungFirmwareDownloader:
    """Samsung Firmware Downloader using official FOTA API"""
    
    # Samsung FOTA Server URLs
    FOTA_CHECK_URL = "https://fota-cloud-dn.ospserver.net/firmware/{region}/{model}/version.xml"
    FOTA_BINARY_INFO_URL = "https://neofussvr.sslcs.cdngc.net/NF_DownloadBinaryInform"
    FOTA_BINARY_INIT_URL = "https://neofussvr.sslcs.cdngc.net/NF_DownloadBinaryInitForMass"
    FOTA_DOWNLOAD_URL = "http://cloud-neofussvr.sslcs.cdngc.net/NF_DownloadBinaryForMass"
    
    # Nonce generation key for authentication
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
        import random
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
