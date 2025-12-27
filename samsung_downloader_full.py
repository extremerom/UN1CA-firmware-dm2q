#!/usr/bin/env python3
"""
Samsung Firmware/OTA Downloader - Versión Completa
==================================================

Análisis completo de:
- FotaAgent.apk + libdprw.so
- SOAgent76.apk  
- OMCAgent5.apk
- Binarios system/bin, vendor/bin

Este script usa dependencias externas para implementar
el protocolo completo de descarga de Samsung.

Requiere:
    pip install requests cryptography lxml

Datos del dispositivo de prueba:
    Modelo: SM-S916B
    CSC: TPA
    Boot ID: 8df0c594-9852-48ff-a649-4d6824eb9fbb
    UFS UN: CE0523757243B468157E
"""

import argparse
import hashlib
import hmac
import os
import sys
import time
from typing import Dict, Optional, Tuple

# Dependencias externas necesarias
try:
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
except ImportError:
    print("❌ Error: Se requiere 'requests'")
    print("   Instalar: pip install requests")
    sys.exit(1)

try:
    from cryptography.hazmat.primitives import hashes, hmac as crypto_hmac
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
except ImportError:
    print("❌ Error: Se requiere 'cryptography'")
    print("   Instalar: pip install cryptography")
    sys.exit(1)

try:
    from lxml import etree as ET
except ImportError:
    print("⚠️  Warning: 'lxml' no instalado, usando xml.etree")
    print("   Recomendado: pip install lxml")
    import xml.etree.ElementTree as ET


class SamsungFirmwareDownloader:
    """
    Samsung Firmware Downloader - Implementación completa
    
    Basado en análisis exhaustivo de:
    - FotaAgent.apk: Servidores y protocolo FOTA
    - SOAgent76.apk: Autenticación y device management
    - OMCAgent5.apk: Servicios Samsung Apps
    - libdprw.so: Funciones nativas de encriptación
    """
    
    # Servidores del análisis (NO terceros)
    FOTA_SERVER = "https://fota-cloud-dn.ospserver.net"
    FUS_SERVER = "http://fus2.shop.v-cdn.net/FUS2"
    SAMSUNG_IDP = "https://api.samsungidp.com"
    SAMSUNG_DM = "https://dir-apis.samsungdm.com"
    VAS_SERVER = "https://vas.samsungapps.com"
    
    # Claves de encriptación de libdprw.so
    ENCRYPTION_KEYS = {
        'key1': '2cbmvps5z4',
        'key2': 'j5p7ll8g33',
        'key3': '5763D0052DC1462E13751F753384E9A9',
        'key4': 'AF87056C54E8BFD81142D235F4F8E552',
        'key5': 'dkaghghkehlsvkdlsmld'
    }
    
    def __init__(self, model: str, region: str, imei: Optional[str] = None,
                 boot_id: Optional[str] = None, ufs_un: Optional[str] = None):
        """
        Inicializa el downloader con información del dispositivo
        
        Args:
            model: Modelo Samsung (SM-S916B)
            region: Código CSC (TPA)
            imei: IMEI 15 dígitos (opcional)
            boot_id: Boot ID del dispositivo (opcional)
            ufs_un: UFS Unique Number (opcional)
        """
        self.model = model
        self.region = region
        self.imei = imei or "000000000000000"
        self.boot_id = boot_id or self._generate_boot_id()
        self.ufs_un = ufs_un or "0" * 20
        
        # Configurar sesión HTTP con retry
        self.session = self._create_session()
        
        # Headers basados en análisis
        self.headers = {
            'User-Agent': 'FOTA_Agent/7.0',
            'X-Device-Model': self.model,
            'X-Device-CSC': self.region,
            'Accept': 'application/xml, text/xml, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
    
    def _create_session(self) -> requests.Session:
        """
        Crea sesión HTTP con retry automático
        """
        session = requests.Session()
        
        # Configurar retry
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _generate_boot_id(self) -> str:
        """Genera boot ID aleatorio"""
        import uuid
        return str(uuid.uuid4())
    
    def _hmac_sha1(self, key: str, message: str) -> str:
        """
        HMAC-SHA1 basado en análisis de libdprw.so
        
        Args:
            key: Clave HMAC
            message: Mensaje a encriptar
            
        Returns:
            Hash hexadecimal en mayúsculas
        """
        h = hmac.new(key.encode(), message.encode(), hashlib.sha1)
        return h.hexdigest().upper()
    
    def _crypto_hmac_sha256(self, key: bytes, message: bytes) -> bytes:
        """
        HMAC-SHA256 usando cryptography
        """
        h = crypto_hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
        h.update(message)
        return h.finalize()
    
    def get_nonce_fus(self) -> str:
        """
        Obtiene nonce del servidor FUS
        
        Returns:
            Nonce del servidor
        """
        url = f"{self.FUS_SERVER}/getNonce"
        data = {
            'id': self.imei,
            'mode': 'Nonce'
        }
        
        print(f"🔑 Obteniendo nonce de FUS...")
        print(f"   URL: {url}")
        
        try:
            response = self.session.post(url, data=data, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # Parsear XML
            root = ET.fromstring(response.text)
            nonce = root.find('.//nonce').text
            
            print(f"   ✅ Nonce obtenido: {nonce[:20]}...")
            return nonce
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            raise
    
    def get_firmware_info_fus(self) -> Dict[str, str]:
        """
        Obtiene información de firmware via FUS
        
        Returns:
            Dict con información del firmware
        """
        # Obtener nonce
        nonce = self.get_nonce_fus()
        
        # Generar auth token
        auth_data = f"{self.imei}{self.model}{self.region}"
        auth_token = self._hmac_sha1(nonce, auth_data)
        
        url = f"{self.FUS_SERVER}/getVersionLists"
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
            'auth': auth_token
        }
        
        print(f"\n📋 Obteniendo información de firmware...")
        print(f"   Servidor: FUS ({self.FUS_SERVER})")
        print(f"   Modelo: {self.model}, CSC: {self.region}")
        
        try:
            response = self.session.post(url, data=data, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # Parsear XML
            root = ET.fromstring(response.text)
            
            info = {}
            latest_ver = root.find('.//latest/version/firmware')
            if latest_ver is not None:
                info['version'] = latest_ver.text
            else:
                info['version'] = root.find('.//firmware/version/latest').text
            
            info['model'] = root.find('.//firmware/model').text
            info['csc'] = root.find('.//firmware/csc').text
            
            logic_value = root.find('.//firmware/version/upgrade/value')
            if logic_value is not None:
                info['logic_value'] = logic_value.text
            
            print(f"   ✅ Versión: {info['version']}")
            return info
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            raise
    
    def get_firmware_info_fota(self) -> Dict[str, str]:
        """
        Obtiene información via servidor FOTA directo
        
        Returns:
            Dict con información del firmware
        """
        url = f"{self.FOTA_SERVER}/firmware/{self.region}/{self.model}/version.xml"
        
        print(f"\n📋 Obteniendo información de firmware...")
        print(f"   Servidor: FOTA ({self.FOTA_SERVER})")
        print(f"   URL: {url}")
        
        try:
            response = self.session.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # Parsear XML
            root = ET.fromstring(response.text)
            
            info = {}
            firmware_node = root.find('.//firmware') or root.find('.//versioninfo/firmware')
            
            if firmware_node is not None:
                version_node = (firmware_node.find('.//version/latest') or
                               firmware_node.find('.//version') or
                               firmware_node.find('.//upgrade/value'))
                
                if version_node is not None:
                    info['version'] = version_node.text
                
                info['model'] = firmware_node.find('.//model').text if firmware_node.find('.//model') is not None else self.model
                info['csc'] = firmware_node.find('.//csc').text if firmware_node.find('.//csc') is not None else self.region
                
                # Información adicional
                size_node = firmware_node.find('.//size')
                if size_node is not None:
                    info['size'] = size_node.text
                
                filename_node = firmware_node.find('.//filename')
                if filename_node is not None:
                    info['filename'] = filename_node.text
                
                path_node = firmware_node.find('.//path')
                if path_node is not None:
                    info['path'] = path_node.text
            
            print(f"   ✅ Versión: {info.get('version', 'Unknown')}")
            return info
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            raise
    
    def download_firmware(self, firmware_info: Dict[str, str], output_dir: str = ".",
                         use_fus: bool = True) -> str:
        """
        Descarga firmware
        
        Args:
            firmware_info: Información del firmware
            output_dir: Directorio de salida
            use_fus: Usar servidor FUS (True) o FOTA directo (False)
            
        Returns:
            Ruta al archivo descargado
        """
        # Determinar URL de descarga
        if use_fus:
            # Usar FUS getBinaryFile
            nonce = self.get_nonce_fus()
            auth_data = f"{self.imei}{self.model}{self.region}"
            auth_token = self._hmac_sha1(nonce, auth_data)
            
            # Obtener binary info
            url = f"{self.FUS_SERVER}/getBinaryInform"
            data = {
                'id': self.imei,
                'mode': 'binary_inform',
                'type': 'firmware',
                'device_model_code': self.model,
                'device_imei_push': self.imei,
                'device_fwver': firmware_info['version'],
                'device_csc_code2': self.region,
                'device_chnl_code': '0',
                'nonce': nonce,
                'auth': auth_token,
                'logic_check': firmware_info['version']
            }
            
            print(f"\n📦 Obteniendo información binaria...")
            response = self.session.post(url, data=data, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            root = ET.fromstring(response.text)
            filename = root.find('.//firmware/filename').text
            file_path = root.find('.//firmware/path').text
            file_size = int(root.find('.//firmware/size').text)
            
            download_url = f"{self.FUS_SERVER}/getBinaryFile?file={file_path}/{filename}"
        else:
            # Usar FOTA directo
            if 'filename' in firmware_info and 'path' in firmware_info:
                filename = firmware_info['filename']
                download_url = f"{self.FOTA_SERVER}/firmware{firmware_info['path']}/{filename}"
            else:
                filename = f"{self.model}_{firmware_info['version']}_OTA_{self.region}.zip"
                download_url = f"{self.FOTA_SERVER}/firmware/{self.region}/{self.model}/{filename}"
            
            file_size = int(firmware_info.get('size', 0))
        
        output_path = os.path.join(output_dir, filename)
        
        print(f"\n⬇️  Descargando firmware...")
        print(f"   Archivo: {filename}")
        if file_size > 0:
            print(f"   Tamaño: {file_size / (1024*1024):.2f} MB")
        print(f"   URL: {download_url}")
        print()
        
        try:
            # Descargar con streaming
            response = self.session.get(download_url, headers=self.headers, stream=True, timeout=60)
            response.raise_for_status()
            
            # Obtener tamaño si no lo tenemos
            if file_size == 0:
                file_size = int(response.headers.get('Content-Length', 0))
            
            downloaded = 0
            start_time = time.time()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Mostrar progreso
                        if file_size > 0:
                            progress = (downloaded / file_size) * 100
                            speed = downloaded / (time.time() - start_time + 0.001) / 1024 / 1024
                            print(f"\r   ⏳ {progress:.1f}% - {downloaded/(1024*1024):.1f}/{file_size/(1024*1024):.1f} MB - {speed:.2f} MB/s", end='', flush=True)
                        else:
                            print(f"\r   ⏳ {downloaded/(1024*1024):.1f} MB descargados", end='', flush=True)
            
            print()
            print(f"   ✅ Descarga completada!")
            print(f"   📁 Guardado en: {os.path.abspath(output_path)}")
            
            return output_path
            
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            print(f"\n   ❌ Error en descarga: {e}")
            raise


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Samsung Firmware/OTA Downloader - Versión Completa",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Información del dispositivo de prueba:
  Modelo:   SM-S916B (Galaxy S23)
  CSC:      TPA (Taiwán)
  Boot ID:  8df0c594-9852-48ff-a649-4d6824eb9fbb
  UFS UN:   CE0523757243B468157E

Ejemplos:
  # Verificar firmware (FUS)
  %(prog)s -m SM-S916B -r TPA --check-only --use-fus
  
  # Verificar firmware (FOTA directo)
  %(prog)s -m SM-S916B -r TPA --check-only
  
  # Descargar con datos del dispositivo
  %(prog)s -m SM-S916B -r TPA -i 352496803361546 \\
      --boot-id 8df0c594-9852-48ff-a649-4d6824eb9fbb \\
      --ufs-un CE0523757243B468157E -o ./firmware

Requiere:
  pip install requests cryptography lxml
        """
    )
    
    parser.add_argument('-m', '--model', required=True, help='Modelo Samsung')
    parser.add_argument('-r', '--region', required=True, help='Código CSC')
    parser.add_argument('-i', '--imei', help='IMEI 15 dígitos')
    parser.add_argument('--boot-id', help='Boot ID del dispositivo')
    parser.add_argument('--ufs-un', help='UFS Unique Number')
    parser.add_argument('-o', '--output-dir', default='.', help='Directorio de salida')
    parser.add_argument('-c', '--check-only', action='store_true', help='Solo verificar versión')
    parser.add_argument('--use-fus', action='store_true', help='Usar servidor FUS (más completo)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Salida detallada')
    
    args = parser.parse_args()
    
    # Crear directorio de salida
    if not args.check_only:
        os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        print("╔══════════════════════════════════════════════════════╗")
        print("║   Samsung Firmware Downloader - Versión Completa    ║")
        print("╚══════════════════════════════════════════════════════╝")
        print(f"Con dependencias: requests, cryptography, lxml")
        print("═" * 54)
        print(f"📱 Modelo:  {args.model}")
        print(f"🌍 Región:  {args.region}")
        if args.imei:
            print(f"🔢 IMEI:    {args.imei}")
        if args.boot_id:
            print(f"🆔 Boot ID: {args.boot_id[:20]}...")
        if args.ufs_un:
            print(f"💾 UFS UN:  {args.ufs_un}")
        
        # Inicializar downloader
        downloader = SamsungFirmwareDownloader(
            model=args.model,
            region=args.region,
            imei=args.imei,
            boot_id=args.boot_id,
            ufs_un=args.ufs_un
        )
        
        # Obtener información de firmware
        if args.use_fus:
            firmware_info = downloader.get_firmware_info_fus()
        else:
            firmware_info = downloader.get_firmware_info_fota()
        
        print(f"\n✅ Firmware encontrado:")
        print(f"   Versión: {firmware_info.get('version', 'Unknown')}")
        print(f"   Modelo:  {firmware_info.get('model', 'Unknown')}")
        print(f"   CSC:     {firmware_info.get('csc', 'Unknown')}")
        
        if args.check_only:
            print("\n✅ Verificación completa")
            return 0
        
        # Confirmar descarga
        print()
        response = input("¿Descargar firmware? (s/n): ")
        if response.lower() != 's':
            print("Descarga cancelada")
            return 0
        
        # Descargar
        downloaded_file = downloader.download_firmware(firmware_info, args.output_dir, args.use_fus)
        
        print()
        print("╔══════════════════════════════════════════════════════╗")
        print("║              ✅ ¡Proceso Completo!                    ║")
        print("╚══════════════════════════════════════════════════════╝")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelado por usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
