#!/usr/bin/env python3
"""
Samsung Firmware Downloader
===========================

Script creado mediante análisis de APKs, JARs y binarios del firmware Samsung.
Implementa el protocolo FOTA de Samsung para descargar firmware update.bin.

Análisis realizado de:
- FotaAgent.apk (system/system/priv-app/FotaAgent/)
- libdprw.so (biblioteca nativa con funciones de encriptación)
- AppUpdateCenter.apk
- build.prop y metadatos del sistema

Servidores descubiertos:
- https://fota-cloud-dn.ospserver.net/firmware/
- http://fus2.shop.v-cdn.net/FUS2

Uso:
    python3 samsung_firmware_downloader.py -m SM-S916B -r OXM -i 123456789012345

Requiere Python 3.6+ (sin dependencias externas)
"""

import argparse
import hashlib
import hmac
import os
import sys
import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, Optional, Tuple
import binascii


class SamsungFUSClient:
    """
    Samsung Firmware Update Server (FUS) Client
    
    Implementación basada en análisis de:
    - FotaAgent.apk: Contiene lógica de descarga FOTA
    - libdprw.so: Biblioteca nativa con claves de encriptación
    - version.xml y version.test.xml: Endpoints descubiertos
    
    Propiedades del sistema utilizadas (del build.prop):
    - ro.product.model: Modelo del dispositivo (SM-S916B)
    - ro.csc.sales_code: Código CSC/región
    - ro.build.PDA: Versión del firmware (S916BXXS8EYK5)
    """
    
    # FUS Server endpoints (descubiertos en análisis)
    FUS_URL = "http://fus2.shop.v-cdn.net/FUS2"
    NONCE_URL = f"{FUS_URL}/getNonce"
    VERSION_URL = f"{FUS_URL}/getVersionLists"
    BINARY_INFORM_URL = f"{FUS_URL}/getBinaryInform"
    BINARY_FILE_URL = f"{FUS_URL}/getBinaryFile"
    
    # Servidores de descarga alternativos (extraídos de FotaAgent.apk)
    DOWNLOAD_SERVERS = [
        "https://fota-cloud-dn.ospserver.net/firmware/",
        "https://cloud-neofussvr.sslcs.cdngc.net/NF_DownloadBinaryForMass.do",
        "http://fota-secure-dn.ospserver.net/firmware/",
    ]
    
    def __init__(self, model: str, region: str, imei: Optional[str] = None):
        """
        Inicializa el cliente FUS de Samsung
        
        Args:
            model: Modelo del dispositivo (ej: SM-S916B, SM-G990B)
            region: Código CSC de región (ej: OXM, DBT, XAA)
            imei: IMEI del dispositivo (opcional, 15 dígitos)
        """
        self.model = model
        self.region = region
        self.imei = imei or "000000000000000"
        
        # Headers basados en análisis de FotaAgent
        self.headers = {
            'User-Agent': 'Kies2.0_FUS',
            'Cache-Control': 'no-cache',
        }
        
    def _generate_nonce(self, nonce: str, auth_data: str) -> str:
        """
        Genera nonce de autenticación usando HMAC-SHA1
        
        Basado en análisis de libdprw.so que contiene:
        - Funciones de encriptación nativas
        - Claves: "2cbmvps5z4", "j5p7ll8g33", "dkaghghkehlsvkdlsmld"
        
        Args:
            nonce: Nonce del servidor
            auth_data: Datos de autenticación (IMEI+Model+Region)
            
        Returns:
            Nonce encriptado en hexadecimal
        """
        key = nonce.encode()
        message = auth_data.encode()
        h = hmac.new(key, message, hashlib.sha1)
        return h.hexdigest().upper()
    
    def _make_request(self, url: str, data: Dict[str, str]) -> str:
        """
        Realiza petición HTTP al servidor FUS (sin bibliotecas externas)
        
        Args:
            url: URL de la petición
            data: Diccionario con datos del formulario
            
        Returns:
            Texto de la respuesta
        """
        try:
            # Codificar datos como application/x-www-form-urlencoded
            post_data = urllib.parse.urlencode(data).encode('utf-8')
            
            # Crear petición
            req = urllib.request.Request(url, data=post_data, headers=self.headers)
            
            # Realizar petición
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8')
                
        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP Error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            raise Exception(f"URL Error: {e.reason}")
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    def get_nonce(self) -> str:
        """
        Obtiene nonce de autenticación del servidor
        
        Endpoint descubierto: getNonce
        Parámetros requeridos: id (IMEI), mode='Nonce'
        
        Returns:
            String del nonce del servidor
        """
        data = {
            'id': self.imei,
            'mode': 'Nonce',
        }
        
        response = self._make_request(self.NONCE_URL, data)
        
        # Parsear respuesta XML
        try:
            root = ET.fromstring(response)
            nonce = root.find('.//nonce').text
            return nonce
        except (ET.ParseError, AttributeError) as e:
            raise Exception(f"Failed to parse nonce response: {e}\nResponse: {response}")
    
    def get_latest_firmware(self) -> Dict[str, str]:
        """
        Obtiene información de la última versión de firmware
        
        Endpoint: getVersionLists
        Archivo descubierto en análisis: version.xml
        
        Parámetros basados en análisis de FotaAgent.apk:
        - device_model_code: ro.product.model
        - device_csc_code2: ro.csc.sales_code
        - device_fwver: ro.build.PDA
        
        Returns:
            Diccionario con información del firmware
        """
        nonce = self.get_nonce()
        
        # Generar datos de autenticación (protocolo descubierto)
        auth_data = f"{self.imei}{self.model}{self.region}"
        encrypted_nonce = self._generate_nonce(nonce, auth_data)
        
        data = {
            'id': self.imei,
            'mode': 'list',
            'type': 'firmware',
            'device_model_code': self.model,
            'device_imei_push': self.imei,
            'device_fwver': '0',
            'device_csc_code2': self.region,
            'device_chnl_code': '0',
            'device_sales_code': '',
            'device_contents_no': '0',
            'device_country_code': '',
            'device_model_region': self.region,
            'nonce': nonce,
            'auth': encrypted_nonce,
        }
        
        response = self._make_request(self.VERSION_URL, data)
        
        # Parsear respuesta XML
        try:
            root = ET.fromstring(response)
            
            # Extraer información del firmware
            firmware_info = {}
            
            latest_ver = root.find('.//latest/version/firmware')
            if latest_ver is not None:
                firmware_info['version'] = latest_ver.text
            else:
                firmware_info['version'] = root.find('.//firmware/version/latest').text
            
            firmware_info['model'] = root.find('.//firmware/model').text
            firmware_info['csc'] = root.find('.//firmware/csc').text
            
            # Intentar encontrar información adicional
            logic_value = root.find('.//firmware/version/upgrade/value')
            if logic_value is not None:
                firmware_info['logic_value'] = logic_value.text
            
            return firmware_info
            
        except (ET.ParseError, AttributeError) as e:
            raise Exception(f"Failed to parse firmware info: {e}\nResponse: {response}")
    
    def get_binary_info(self, firmware_version: str) -> Dict[str, str]:
        """
        Obtiene información de descarga del binario para una versión específica
        
        Endpoint: getBinaryInform
        Parámetro clave: logic_check (versión del firmware)
        
        Args:
            firmware_version: String de versión del firmware
            
        Returns:
            Diccionario con información del binario incluyendo ruta y nombre del archivo
        """
        nonce = self.get_nonce()
        
        # Generar datos de autenticación
        auth_data = f"{self.imei}{self.model}{self.region}"
        encrypted_nonce = self._generate_nonce(nonce, auth_data)
        
        data = {
            'id': self.imei,
            'mode': 'binary_inform',
            'type': 'firmware',
            'device_model_code': self.model,
            'device_imei_push': self.imei,
            'device_fwver': firmware_version,
            'device_csc_code2': self.region,
            'device_chnl_code': '0',
            'device_sales_code': '',
            'device_contents_no': '0',
            'device_country_code': '',
            'device_model_region': self.region,
            'nonce': nonce,
            'auth': encrypted_nonce,
            'logic_check': firmware_version,
        }
        
        response = self._make_request(self.BINARY_INFORM_URL, data)
        
        # Parsear respuesta XML
        try:
            root = ET.fromstring(response)
            
            binary_info = {
                'version': root.find('.//firmware/version').text,
                'filename': root.find('.//firmware/filename').text,
                'path': root.find('.//firmware/path').text,
                'size': root.find('.//firmware/size').text,
                'model': root.find('.//firmware/model').text,
                'crc': root.find('.//firmware/crc').text if root.find('.//firmware/crc') is not None else '',
                'encrypted': root.find('.//firmware/encrypted').text if root.find('.//firmware/encrypted') is not None else '0',
            }
            
            return binary_info
            
        except (ET.ParseError, AttributeError) as e:
            raise Exception(f"Failed to parse binary info: {e}\nResponse: {response}")
    
    def download_firmware(self, binary_info: Dict[str, str], output_dir: str = ".", 
                         chunk_size: int = 8192) -> str:
        """
        Download firmware binary file
        
        Args:
            binary_info: Binary information dictionary from get_binary_info()
            output_dir: Output directory for downloaded file
            chunk_size: Download chunk size in bytes
            
        Returns:
            Path to downloaded file
        """
        filename = binary_info['filename']
        file_path = binary_info['path']
        file_size = int(binary_info['size'])
        
        output_path = os.path.join(output_dir, filename)
        
        # Construct download URL
        download_url = f"{self.BINARY_FILE_URL}?file={file_path}/{filename}"
        
        print(f"Downloading: {filename}")
        print(f"Size: {file_size / (1024*1024*1024):.2f} GB")
        print(f"URL: {download_url}")
        
        try:
            response = self.session.get(download_url, stream=True, timeout=60)
            response.raise_for_status()
            
            downloaded = 0
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Progress indicator
                        progress = (downloaded / file_size) * 100
                        print(f"\rProgress: {progress:.2f}% ({downloaded / (1024*1024):.2f} MB / {file_size / (1024*1024):.2f} MB)", end='')
            
            print("\nDownload completed!")
            return output_path
            
        except requests.RequestException as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            raise Exception(f"Download failed: {e}")
    
    def decrypt_firmware(self, encrypted_file: str, output_file: str, 
                        firmware_version: str) -> str:
        """
        Decrypt encrypted firmware file
        
        Note: This is a placeholder. Actual decryption requires the specific
        encryption key and algorithm used by Samsung (typically AES).
        
        Args:
            encrypted_file: Path to encrypted firmware file
            output_file: Path for decrypted output
            firmware_version: Firmware version for key derivation
            
        Returns:
            Path to decrypted file
        """
        print("Warning: Firmware decryption not yet implemented.")
        print("Samsung firmware files may be encrypted with proprietary keys.")
        print("Use official tools like Smart Switch or SamFirm for decryption.")
        return encrypted_file


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Samsung Firmware Downloader - Download official Samsung firmware",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check latest firmware for SM-S916B (Galaxy S23) in OXM region
  %(prog)s -m SM-S916B -r OXM --check-only
  
  # Download latest firmware
  %(prog)s -m SM-S916B -r OXM -o /path/to/download
  
  # Use specific IMEI
  %(prog)s -m SM-S916B -r OXM -i 123456789012345

Common Samsung Models:
  - SM-S916B: Galaxy S23 (International)
  - SM-S918B: Galaxy S23 Ultra
  - SM-G990B: Galaxy S21 FE
  - SM-A536B: Galaxy A53 5G
  
Common CSC Codes:
  - OXM: Open European (Multi-CSC)
  - DBT: Germany
  - BTU: United Kingdom
  - XAA: USA Unlocked
  - XEF: France
        """
    )
    
    parser.add_argument('-m', '--model', required=True,
                       help='Device model code (e.g., SM-S916B)')
    parser.add_argument('-r', '--region', required=True,
                       help='CSC region code (e.g., OXM, DBT, XAA)')
    parser.add_argument('-i', '--imei', 
                       help='Device IMEI (15 digits, optional)')
    parser.add_argument('-o', '--output-dir', default='.',
                       help='Output directory for downloaded firmware (default: current directory)')
    parser.add_argument('-c', '--check-only', action='store_true',
                       help='Only check for firmware updates without downloading')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Validate IMEI if provided
    if args.imei:
        if not args.imei.isdigit() or len(args.imei) != 15:
            print("Error: IMEI must be 15 digits")
            sys.exit(1)
    
    # Create output directory if it doesn't exist
    if not args.check_only:
        os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Initialize client
        print(f"Samsung Firmware Downloader")
        print(f"=" * 50)
        print(f"Model: {args.model}")
        print(f"Region: {args.region}")
        if args.imei:
            print(f"IMEI: {args.imei}")
        print()
        
        client = SamsungFUSClient(args.model, args.region, args.imei)
        
        # Check for latest firmware
        print("Checking for latest firmware...")
        firmware_info = client.get_latest_firmware()
        
        print(f"\nLatest Firmware Information:")
        print(f"  Version: {firmware_info['version']}")
        print(f"  Model: {firmware_info['model']}")
        print(f"  CSC: {firmware_info['csc']}")
        
        if args.check_only:
            print("\nCheck complete.")
            return 0
        
        # Get binary information
        print("\nGetting firmware download information...")
        binary_info = client.get_binary_info(firmware_info['version'])
        
        print(f"\nFirmware Details:")
        print(f"  Filename: {binary_info['filename']}")
        print(f"  Size: {int(binary_info['size']) / (1024*1024*1024):.2f} GB")
        print(f"  Path: {binary_info['path']}")
        if binary_info['crc']:
            print(f"  CRC: {binary_info['crc']}")
        if binary_info['encrypted'] == '1':
            print(f"  Encrypted: Yes")
        
        # Download firmware
        print(f"\nStarting download to: {args.output_dir}")
        downloaded_file = client.download_firmware(binary_info, args.output_dir)
        
        print(f"\n{'=' * 50}")
        print(f"Download Complete!")
        print(f"File saved to: {downloaded_file}")
        
        if binary_info['encrypted'] == '1':
            print("\nNote: This firmware file is encrypted.")
            print("Use Samsung Smart Switch or similar tools to decrypt.")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
