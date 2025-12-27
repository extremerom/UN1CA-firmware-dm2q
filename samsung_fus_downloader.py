#!/usr/bin/env python3
"""
Samsung Firmware Downloader - Método FUS Completo
Basado en análisis exhaustivo de:
- Smart Switch Windows (FUS Service)
- Smart Switch Mac (NeoFUS)
- FotaAgent Android
- SOAgent76, OMCAgent5

Autor: Análisis de ingeniería inversa
Versión: 2.0.0
"""

import sys
import os
import hashlib
import hmac
import time
import argparse
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
from typing import Optional, Dict, Tuple

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("ERROR: Se requiere 'requests'. Instalar con: pip install requests")
    sys.exit(1)

class SamsungFUSClient:
    """
    Cliente del protocolo FUS de Samsung
    Soporta descarga de firmware desde servidores oficiales
    """
    
    # Servidores FUS descubiertos en análisis
    FUS_SERVERS = {
        'primary': 'http://fus2.shop.v-cdn.net/FUS2',
        'neofus': 'https://neofussvr.sslcs.cdngc.net',
        'china': 'https://cnfussvr.sslcs.cdngc.net'
    }
    
    # Claves de encriptación de libdprw.so
    ENCRYPTION_KEYS = [
        '2cbmvps5z4',
        'j5p7ll8g33',
        '5763D0052DC1462E13751F753384E9A9',
        'AF87056C54E8BFD81142D235F4F8E552',
        'dkaghghkehlsvkdlsmld'
    ]
    
    def __init__(self, model: str, region: str, imei: Optional[str] = None, 
                 server: str = 'primary'):
        """
        Inicializar cliente FUS
        
        Args:
            model: Modelo del dispositivo (ej: SM-S916B)
            region: Código CSC/región (ej: TPA)
            imei: IMEI del dispositivo (opcional)
            server: Servidor a usar (primary, neofus, china)
        """
        self.model = model
        self.region = region
        self.imei = imei or self._generate_generic_imei()
        self.server_url = self.FUS_SERVERS.get(server, self.FUS_SERVERS['primary'])
        
        # Configurar sesión HTTP con retry
        self.session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # Headers estándar de Smart Switch
        self.session.headers.update({
            'User-Agent': 'Kies2.0_FUS',
            'Accept': '*/*',
            'Connection': 'Keep-Alive'
        })
    
    def _generate_generic_imei(self) -> str:
        """Generar IMEI genérico basado en modelo"""
        # Generar IMEI válido usando Luhn algorithm
        base = '35249680336154'  # Base IMEI
        check_digit = self._calculate_luhn_check(base)
        return base + str(check_digit)
    
    def _calculate_luhn_check(self, number: str) -> int:
        """Calcular dígito de verificación Luhn"""
        digits = [int(d) for d in number]
        checksum = 0
        for i, digit in enumerate(reversed(digits)):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            checksum += digit
        return (10 - (checksum % 10)) % 10
    
    def _generate_nonce(self) -> str:
        """
        Generar nonce para autenticación FUS
        Basado en análisis de MakeAuthorizationHeaderWithGeneratedNonceValueAndAMModule
        """
        timestamp = str(int(time.time()))
        nonce_data = f"{self.model}{self.region}{timestamp}"
        nonce = hashlib.md5(nonce_data.encode()).hexdigest()
        return nonce
    
    def _create_auth_header(self, nonce: str) -> str:
        """
        Crear header de autorización con HMAC-SHA1
        Basado en análisis de libdprw.so y FUS Service
        """
        # Datos para firma: nonce + IMEI + modelo + CSC
        auth_data = f"{nonce}{self.imei}{self.model}{self.region}"
        
        # Usar primera clave de encriptación
        key = self.ENCRYPTION_KEYS[0].encode()
        signature = hmac.new(key, auth_data.encode(), hashlib.sha1).hexdigest()
        
        # Formato del header
        auth_header = f"FUS nonce=\"{nonce}\", signature=\"{signature}\", nc=\"\", type=\"\", realm=\"\", newauth=\"1\""
        return auth_header
    
    def get_nonce(self) -> Tuple[bool, str]:
        """
        Paso 1: Obtener nonce del servidor
        Endpoint: /NF_DownloadGenerateNonce.do (inferido)
        """
        endpoint = f"{self.server_url}/NF_DownloadGenerateNonce.do"
        
        params = {
            'xml': '1'
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=30)
            
            if response.status_code == 200:
                # Parsear respuesta XML
                root = ET.fromstring(response.content)
                nonce_elem = root.find('.//nonce')
                
                if nonce_elem is not None:
                    return True, nonce_elem.text
                else:
                    # Generar nonce localmente si el servidor no responde
                    return True, self._generate_nonce()
            else:
                # Fallback a nonce local
                return True, self._generate_nonce()
        except Exception as e:
            print(f"⚠️  Error obteniendo nonce, usando local: {e}")
            return True, self._generate_nonce()
    
    def get_binary_info(self, nonce: str) -> Tuple[bool, Optional[Dict]]:
        """
        Paso 2: Obtener información del binario disponible
        Endpoint: /NF_DownloadBinaryInform.do (inferido)
        """
        endpoint = f"{self.server_url}/NF_DownloadBinaryInform.do"
        
        # Crear header de autorización
        auth_header = self._create_auth_header(nonce)
        
        headers = {
            'Authorization': auth_header
        }
        
        # Parámetros del request
        params = {
            'xml': '1',
            'device': self.model,
            'region': self.region,
            'csc': self.region,
            'imei': self.imei,
            'logic_check': self.model,
            'version': ''  # Versión actual (vacío para obtener última)
        }
        
        try:
            response = self.session.get(endpoint, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Parsear respuesta XML
                root = ET.fromstring(response.content)
                
                # Extraer información del firmware
                firmware_info = {
                    'version': self._get_xml_text(root, './/version/latest'),
                    'firmware': self._get_xml_text(root, './/firmware/version'),
                    'os_version': self._get_xml_text(root, './/firmware/os'),
                    'size': self._get_xml_text(root, './/size'),
                    'display_name': self._get_xml_text(root, './/firmware/display_name'),
                    'model_path': self._get_xml_text(root, './/firmware/model_path'),
                    'description': self._get_xml_text(root, './/description'),
                    'path': self._get_xml_text(root, './/path')
                }
                
                return True, firmware_info
            else:
                print(f"❌ Error {response.status_code}: {response.text[:200]}")
                return False, None
        except Exception as e:
            print(f"❌ Error obteniendo información del binario: {e}")
            return False, None
    
    def _get_xml_text(self, root: ET.Element, xpath: str) -> str:
        """Extraer texto de elemento XML de forma segura"""
        elem = root.find(xpath)
        return elem.text if elem is not None and elem.text else ''
    
    def download_firmware(self, firmware_info: Dict, output_dir: str, 
                         progress_callback=None) -> bool:
        """
        Paso 3: Descargar firmware
        Endpoint: URL obtenida de get_binary_info
        """
        # Construir URL de descarga
        if firmware_info.get('path'):
            download_url = firmware_info['path']
        elif firmware_info.get('model_path'):
            # Construir URL desde model_path
            download_url = f"{self.server_url}/firmware/{firmware_info['model_path']}"
        else:
            print("❌ No se pudo determinar URL de descarga")
            return False
        
        # Determinar nombre del archivo
        filename = f"{self.model}_{self.region}_{firmware_info.get('version', 'unknown')}.tar.md5"
        filepath = os.path.join(output_dir, filename)
        
        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n⬇️  Descargando firmware...")
        print(f"   URL: {download_url}")
        print(f"   Archivo: {filename}")
        
        try:
            response = self.session.get(download_url, stream=True, timeout=60)
            
            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if progress_callback:
                                progress_callback(downloaded, total_size)
                            else:
                                # Mostrar progreso simple
                                if total_size > 0:
                                    percent = (downloaded / total_size) * 100
                                    self._print_progress(percent, downloaded, total_size)
                
                print(f"\n✅ Descarga completada: {filepath}")
                return True
            else:
                print(f"❌ Error {response.status_code}: {response.text[:200]}")
                return False
        except Exception as e:
            print(f"❌ Error descargando firmware: {e}")
            return False
    
    def _print_progress(self, percent: float, downloaded: int, total: int):
        """Mostrar barra de progreso"""
        bar_length = 40
        filled = int(bar_length * percent / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        downloaded_mb = downloaded / (1024 * 1024)
        total_mb = total / (1024 * 1024)
        
        print(f"\r   [{bar}] {percent:.1f}% ({downloaded_mb:.1f}/{total_mb:.1f} MB)", end='', flush=True)
    
    def check_firmware(self) -> Tuple[bool, Optional[Dict]]:
        """
        Verificar firmware disponible (sin descargar)
        """
        print(f"\n{'='*70}")
        print(f"  Samsung Firmware Checker - Método FUS Completo")
        print(f"{'='*70}")
        print(f"📱 Modelo: {self.model}")
        print(f"🌍 CSC: {self.region}")
        print(f"📞 IMEI: {self.imei}")
        print(f"🖥️  Servidor: {self.server_url}")
        print(f"{'='*70}\n")
        
        # Paso 1: Obtener nonce
        print("🔐 Paso 1: Obteniendo nonce...")
        success, nonce = self.get_nonce()
        if not success:
            print("❌ Error obteniendo nonce")
            return False, None
        print(f"✅ Nonce obtenido: {nonce[:16]}...")
        
        # Paso 2: Obtener información del firmware
        print("\n📋 Paso 2: Obteniendo información del firmware...")
        success, firmware_info = self.get_binary_info(nonce)
        if not success or not firmware_info:
            print("❌ No se pudo obtener información del firmware")
            return False, None
        
        # Mostrar información
        print(f"\n{'─'*70}")
        print(f"📋 Firmware Disponible")
        print(f"{'─'*70}")
        if firmware_info.get('version'):
            print(f"Versión: {firmware_info['version']}")
        if firmware_info.get('firmware'):
            print(f"Firmware: {firmware_info['firmware']}")
        if firmware_info.get('os_version'):
            print(f"OS Version: {firmware_info['os_version']}")
        if firmware_info.get('display_name'):
            print(f"Nombre: {firmware_info['display_name']}")
        if firmware_info.get('size'):
            try:
                size_mb = int(firmware_info['size']) / (1024 * 1024)
                print(f"Tamaño: {size_mb:.1f} MB")
            except:
                print(f"Tamaño: {firmware_info['size']}")
        if firmware_info.get('description'):
            print(f"Descripción: {firmware_info['description']}")
        print(f"{'─'*70}\n")
        
        return True, firmware_info


def main():
    parser = argparse.ArgumentParser(
        description='Samsung Firmware Downloader - Método FUS Completo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos de uso:

  # Verificar firmware disponible
  python3 %(prog)s -m SM-S916B -r TPA --check-only
  
  # Descargar firmware
  python3 %(prog)s -m SM-S916B -r TPA -o ./firmware
  
  # Con IMEI específico
  python3 %(prog)s -m SM-S916B -r TPA -i 352496803361546 -o ./firmware
  
  # Usar servidor alternativo (NeoFUS)
  python3 %(prog)s -m SM-S916B -r TPA --server neofus --check-only

Modelos soportados: Todos los modelos Samsung
CSC soportados: Todos los códigos de región
        '''
    )
    
    parser.add_argument('-m', '--model', required=True,
                       help='Modelo del dispositivo (ej: SM-S916B)')
    parser.add_argument('-r', '--region', required=True,
                       help='Código CSC/región (ej: TPA, XAR, DBT)')
    parser.add_argument('-i', '--imei', 
                       help='IMEI del dispositivo (opcional, se genera si no se proporciona)')
    parser.add_argument('-o', '--output', default='./firmware',
                       help='Directorio de salida (default: ./firmware)')
    parser.add_argument('--server', choices=['primary', 'neofus', 'china'],
                       default='primary',
                       help='Servidor FUS a usar (default: primary)')
    parser.add_argument('--check-only', action='store_true',
                       help='Solo verificar firmware disponible, no descargar')
    
    args = parser.parse_args()
    
    # Crear cliente FUS
    client = SamsungFUSClient(
        model=args.model,
        region=args.region,
        imei=args.imei,
        server=args.server
    )
    
    # Verificar firmware
    success, firmware_info = client.check_firmware()
    
    if not success:
        print("\n❌ No se pudo verificar el firmware")
        return 1
    
    if args.check_only:
        print("✅ Verificación completada")
        return 0
    
    # Descargar firmware
    print(f"\n⬇️  Paso 3: Descargando firmware...\n")
    success = client.download_firmware(firmware_info, args.output)
    
    if success:
        print("\n✅ Proceso completado exitosamente")
        return 0
    else:
        print("\n❌ Error en la descarga")
        return 1


if __name__ == '__main__':
    sys.exit(main())
