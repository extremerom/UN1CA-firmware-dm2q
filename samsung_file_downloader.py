#!/usr/bin/env python3
"""
Samsung APK & File Downloader
==============================

Descarga APKs, plugins y archivos desde servidores Samsung descubiertos
en el análisis de Smart Switch y aplicaciones Android.

Autor: Análisis completo de firmware Samsung
Fecha: 2025-12-27
"""

import requests
import hashlib
import sys
import os
from typing import Optional, List, Dict
from datetime import datetime
import json

class SamsungFileDownloader:
    """
    Descargador universal de archivos Samsung
    Usa todos los servidores descubiertos en el análisis
    """
    
    # Servidores descubiertos
    SERVERS = {
        'vas': 'https://vas.samsungapps.com',
        'update_kies': 'https://update.kies.samsung.com',
        'smartswitch_api': 'https://api.sec-smartswitch.com',
        'sspc': 'https://sspc.sec-smartswitch.com',
        'neofus': 'https://neofussvr.sslcs.cdngc.net',
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Smart Switch Mac/5.0.43.1',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        })
    
    def _print(self, message: str, prefix: str = "ℹ️"):
        """Imprimir mensaje"""
        print(f"{prefix}  {message}")
    
    def download_file(self, url: str, output_path: str, description: str = "archivo") -> bool:
        """Descargar archivo con progreso"""
        try:
            self._print(f"Descargando {description}...", "⬇️")
            self._print(f"URL: {url}")
            
            response = self.session.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            if total_size > 0:
                size_mb = total_size / (1024 * 1024)
                self._print(f"Tamaño: {size_mb:.2f} MB")
            
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            downloaded = 0
            start_time = datetime.now()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            downloaded_mb = downloaded / (1024 * 1024)
                            
                            elapsed = (datetime.now() - start_time).total_seconds()
                            if elapsed > 0:
                                speed_mbps = (downloaded / elapsed) / (1024 * 1024)
                                print(f"\rProgreso: {progress:.1f}% ({downloaded_mb:.1f}/{size_mb:.1f} MB) "
                                      f"- {speed_mbps:.2f} MB/s", end='', flush=True)
            
            print()
            self._print(f"✅ Archivo descargado: {output_path}")
            
            # Calcular MD5
            md5_hash = hashlib.md5()
            with open(output_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    md5_hash.update(chunk)
            self._print(f"MD5: {md5_hash.hexdigest()}", "🔐")
            
            return True
            
        except Exception as e:
            self._print(f"❌ Error: {e}")
            return False
    
    def download_easy_mover_apk(self, csc: str, output_dir: str = "./apks") -> bool:
        """
        Descargar Easy Mover APK desde VAS
        Endpoint descubierto en DeviceCenter.framework
        """
        self._print("Descargando Easy Mover APK...", "📱")
        
        # Parámetros del endpoint VAS
        device_id = hashlib.md5(f"SSPC_{csc}".encode()).hexdigest()
        
        url = (
            f"{self.SERVERS['vas']}/stub/stubDownload.as"
            f"?appId=com.sec.android.easyMover"
            f"&callerId=SSPC"
            f"&deviceId={device_id}"
            f"&csc={csc}"
            f"&sdkVer=30"
            f"&mcc=450&mnc=05"
            f"&isAutoUpdate=0"
            f"&pd=0"
        )
        
        filename = f"EasyMover_{csc}.apk"
        output_path = os.path.join(output_dir, filename)
        
        return self.download_file(url, output_path, "Easy Mover APK")
    
    def download_device_image(self, model: str, csc: str, output_dir: str = "./images") -> bool:
        """
        Descargar imagen del dispositivo
        Endpoint confirmado funcional
        """
        self._print(f"Descargando imagen de {model}...", "🖼️")
        
        url = f"{self.SERVERS['update_kies']}/update/smartswitchpc/image?model={model}&ProductCode={csc}"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('resultCode') == 0 and data.get('url'):
                image_url = data['url']
                filename = os.path.basename(image_url)
                output_path = os.path.join(output_dir, filename)
                
                return self.download_file(image_url, output_path, f"imagen de {model}")
            else:
                self._print(f"❌ Error: {data.get('resultMessage', 'Unknown')}")
                return False
                
        except Exception as e:
            self._print(f"❌ Error: {e}")
            return False
    
    def check_easy_mover_update(self, csc: str) -> Optional[Dict]:
        """Verificar actualización de Easy Mover"""
        self._print("Verificando versión de Easy Mover...", "🔍")
        
        device_id = hashlib.md5(f"SSPC_{csc}".encode()).hexdigest()
        
        url = (
            f"{self.SERVERS['vas']}/stub/stubUpdateCheck.as"
            f"?appId=com.sec.android.easyMover"
            f"&callerId=SSPC"
            f"&versionCode=1"
            f"&deviceId={device_id}"
            f"&csc={csc}"
            f"&sdkVer=30"
            f"&mcc=450&mnc=05"
            f"&pd=0"
        )
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # La respuesta puede ser XML o JSON
            data = response.text
            self._print(f"Respuesta: {data}")
            
            return {'url': url, 'response': data}
            
        except Exception as e:
            self._print(f"❌ Error: {e}")
            return None
    
    def download_smart_switch_update(self, output_dir: str = "./updates") -> bool:
        """Descargar actualización de Smart Switch para Mac"""
        self._print("Verificando actualización de Smart Switch Mac...", "🔄")
        
        # URLs de actualización descubiertas
        notice_url = f"{self.SERVERS['update_kies']}/update/smartswitch_mac/notice?region=US&isTest=false"
        
        try:
            response = self.session.get(notice_url, timeout=30)
            response.raise_for_status()
            
            self._print(f"Respuesta de actualización: {response.text[:200]}...")
            
            # Parsear respuesta para obtener URL de descarga
            # (El formato exacto depende de la respuesta del servidor)
            
            return True
            
        except Exception as e:
            self._print(f"❌ Error: {e}")
            return False
    
    def list_available_downloads(self, model: str = None, csc: str = None):
        """Listar archivos disponibles para descargar"""
        print("\n" + "="*70)
        print("  Archivos Disponibles para Descargar")
        print("="*70)
        
        downloads = []
        
        # 1. Imagen del dispositivo
        if model and csc:
            downloads.append({
                'type': 'Imagen de dispositivo',
                'server': 'update.kies.samsung.com',
                'description': f'Imagen PNG de {model}',
                'command': f'--image -m {model} -r {csc}'
            })
        
        # 2. Easy Mover APK
        if csc:
            downloads.append({
                'type': 'Easy Mover APK',
                'server': 'vas.samsungapps.com',
                'description': 'Aplicación de transferencia Samsung',
                'command': f'--easymover -r {csc}'
            })
        
        # 3. Smart Switch update
        downloads.append({
            'type': 'Smart Switch Mac Update',
            'server': 'update.kies.samsung.com',
            'description': 'Actualización de Smart Switch',
            'command': '--smartswitch-update'
        })
        
        for i, item in enumerate(downloads, 1):
            print(f"\n{i}. {item['type']}")
            print(f"   Servidor: {item['server']}")
            print(f"   Descripción: {item['description']}")
            print(f"   Comando: python3 samsung_file_downloader.py {item['command']}")
        
        print("\n" + "="*70 + "\n")


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Samsung APK & File Downloader',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Descargar imagen de dispositivo
  python3 %(prog)s --image -m SM-S916B -r TPA

  # Descargar Easy Mover APK
  python3 %(prog)s --easymover -r TPA -o ./apks

  # Verificar actualización de Easy Mover
  python3 %(prog)s --check-easymover -r TPA

  # Listar archivos disponibles
  python3 %(prog)s --list -m SM-S916B -r TPA

Servidores usados (descubiertos en análisis):
  - vas.samsungapps.com (APKs)
  - update.kies.samsung.com (Imágenes, actualizaciones)
  - sspc.sec-smartswitch.com (Smart Switch)
        """
    )
    
    parser.add_argument('-m', '--model',
                        help='Modelo del dispositivo (ej: SM-S916B)')
    parser.add_argument('-r', '--region',
                        help='Código CSC/región (ej: TPA)')
    parser.add_argument('-o', '--output', default='./downloads',
                        help='Directorio de salida (default: ./downloads)')
    
    # Tipos de descarga
    parser.add_argument('--image', action='store_true',
                        help='Descargar imagen del dispositivo')
    parser.add_argument('--easymover', action='store_true',
                        help='Descargar Easy Mover APK')
    parser.add_argument('--check-easymover', action='store_true',
                        help='Verificar actualización de Easy Mover')
    parser.add_argument('--smartswitch-update', action='store_true',
                        help='Descargar actualización de Smart Switch')
    parser.add_argument('--list', action='store_true',
                        help='Listar archivos disponibles')
    
    args = parser.parse_args()
    
    downloader = SamsungFileDownloader()
    
    success = True
    
    if args.list:
        downloader.list_available_downloads(args.model, args.region)
    elif args.image:
        if not args.model or not args.region:
            print("❌ Error: --image requiere -m MODEL y -r REGION")
            sys.exit(1)
        success = downloader.download_device_image(args.model, args.region, args.output)
    elif args.easymover:
        if not args.region:
            print("❌ Error: --easymover requiere -r REGION")
            sys.exit(1)
        success = downloader.download_easy_mover_apk(args.region, args.output)
    elif args.check_easymover:
        if not args.region:
            print("❌ Error: --check-easymover requiere -r REGION")
            sys.exit(1)
        result = downloader.check_easy_mover_update(args.region)
        success = result is not None
    elif args.smartswitch_update:
        success = downloader.download_smart_switch_update(args.output)
    else:
        parser.print_help()
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
