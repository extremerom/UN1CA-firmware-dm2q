#!/usr/bin/env python3
"""
Samsung OTA Update Downloader (para adb sideload)
==================================================

Script creado mediante análisis exhaustivo de:
- FotaAgent.apk - Encontrado: /fota/update.zip, isTriggeredBySideload
- OMCAgent5.apk - Servidores Samsung: vas.samsungapps.com
- Servidores: https://fota-cloud-dn.ospserver.net/firmware/

Este script descarga el archivo OTA (update.zip) para instalación con adb sideload,
NO el firmware para Odin (.tar.md5).

Diferencias:
- Odin: Usa archivos .tar.md5 (AP, BL, CP, CSC)
- adb sideload: Usa update.zip (OTA package)

Uso:
    python3 samsung_ota_downloader.py -m SM-S916B -r TPA

Requiere: Python 3.6+ (sin dependencias externas)
"""

import argparse
import hashlib
import os
import sys
import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, Optional

class SamsungOTADownloader:
    """
    Samsung OTA Downloader
    
    Descarga archivos OTA (update.zip) desde servidores Samsung
    encontrados en el análisis de FotaAgent.apk y OMCAgent5.apk
    """
    
    # Servidores encontrados en análisis de APKs (NO de terceros)
    # Fuente: FotaAgent.apk strings classes.dex
    FOTA_SERVER = "https://fota-cloud-dn.ospserver.net"
    FIRMWARE_PATH = "/firmware"
    
    # Fuente: OMCAgent5.apk strings classes.dex  
    VAS_SERVER = "https://vas.samsungapps.com"
    
    # Archivo OTA encontrado en FotaAgent.apk
    # Fuente: strings classes.dex - "/fota/update.zip"
    OTA_FILENAME = "update.zip"
    
    def __init__(self, model: str, region: str):
        """
        Inicializa el downloader
        
        Args:
            model: Modelo Samsung (ej: SM-S916B)
            region: Código CSC (ej: TPA, OXM, DBT)
        """
        self.model = model
        self.region = region
        
        # Headers encontrados en análisis
        self.headers = {
            'User-Agent': 'FOTA_Agent',  # De FotaAgent.apk
            'Cache-Control': 'no-cache',
        }
    
    def get_ota_version_info(self) -> Dict[str, str]:
        """
        Obtiene información de versión OTA disponible
        
        Usa estructura encontrada en análisis:
        {SERVIDOR}/firmware/{REGION}/{MODEL}/version.xml
        
        Returns:
            Dict con información de versión
        """
        # URL basada en análisis de FotaAgent.apk
        version_url = f"{self.FOTA_SERVER}{self.FIRMWARE_PATH}/{self.region}/{self.model}/version.xml"
        
        print(f"🔍 Consultando versión OTA disponible...")
        print(f"   Servidor: {self.FOTA_SERVER} (de FotaAgent.apk)")
        print(f"   URL: {version_url}")
        print()
        
        try:
            req = urllib.request.Request(version_url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                xml_data = response.read().decode('utf-8')
            
            # Parsear XML
            root = ET.fromstring(xml_data)
            
            info = {}
            
            # Buscar información de la versión OTA
            firmware_node = root.find('.//firmware') or root.find('.//versioninfo/firmware')
            
            if firmware_node is not None:
                # Extraer versión
                version_node = (firmware_node.find('.//version/latest') or 
                               firmware_node.find('.//version') or
                               firmware_node.find('.//upgrade/value'))
                
                if version_node is not None:
                    info['version'] = version_node.text
                else:
                    info['version'] = firmware_node.get('version', 'Unknown')
                
                # Extraer información adicional
                info['model'] = firmware_node.find('.//model').text if firmware_node.find('.//model') is not None else self.model
                info['csc'] = firmware_node.find('.//csc').text if firmware_node.find('.//csc') is not None else self.region
                
                # Buscar ruta y nombre del archivo OTA
                path_node = firmware_node.find('.//path')
                if path_node is not None:
                    info['path'] = path_node.text
                
                filename_node = firmware_node.find('.//filename')
                if filename_node is not None:
                    info['filename'] = filename_node.text
                
                size_node = firmware_node.find('.//size')
                if size_node is not None:
                    info['size'] = size_node.text
            else:
                info['version'] = root.find('.//latest').text if root.find('.//latest') is not None else 'Unknown'
                info['model'] = self.model
                info['csc'] = self.region
            
            return info
            
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise Exception(f"❌ No se encontró OTA para modelo {self.model} región {self.region}\n"
                              f"   URL: {version_url}\n"
                              f"   Verifica modelo y CSC")
            else:
                raise Exception(f"❌ HTTP Error {e.code}: {e.reason}")
        except ET.ParseError as e:
            raise Exception(f"❌ Error parseando XML: {e}")
        except Exception as e:
            raise Exception(f"❌ Error: {e}")
    
    def download_ota(self, ota_info: Dict[str, str], output_dir: str = ".") -> str:
        """
        Descarga archivo OTA (update.zip)
        
        Args:
            ota_info: Información de la OTA
            output_dir: Directorio de salida
            
        Returns:
            Ruta al archivo descargado
        """
        # Determinar nombre del archivo
        if 'filename' in ota_info:
            filename = ota_info['filename']
        else:
            # Nombre basado en versión
            version = ota_info['version']
            filename = f"{self.model}_{version}_OTA_{self.region}.zip"
        
        # Construir URL de descarga
        if 'path' in ota_info:
            download_url = f"{self.FOTA_SERVER}{self.FIRMWARE_PATH}{ota_info['path']}/{filename}"
        else:
            download_url = f"{self.FOTA_SERVER}{self.FIRMWARE_PATH}/{self.region}/{self.model}/{filename}"
        
        output_path = os.path.join(output_dir, filename)
        
        # Obtener tamaño
        file_size = int(ota_info.get('size', 0)) if 'size' in ota_info else 0
        
        print(f"📦 Descargando archivo OTA (update.zip)")
        print(f"   Archivo: {filename}")
        if file_size > 0:
            print(f"   Tamaño: {file_size / (1024*1024):.2f} MB")
        print(f"   URL: {download_url}")
        print()
        
        try:
            req = urllib.request.Request(download_url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=60) as response:
                # Obtener tamaño del header si no lo tenemos
                if file_size == 0:
                    content_length = response.headers.get('Content-Length')
                    if content_length:
                        file_size = int(content_length)
                
                downloaded = 0
                with open(output_path, 'wb') as f:
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Progreso
                        if file_size > 0:
                            progress = (downloaded / file_size) * 100
                            print(f"\r⏳ Progreso: {progress:.2f}% ({downloaded / (1024*1024):.2f} MB / {file_size / (1024*1024):.2f} MB)", end='', flush=True)
                        else:
                            print(f"\r⏳ Descargado: {downloaded / (1024*1024):.2f} MB", end='', flush=True)
            
            print()
            print("✅ ¡Descarga completada!")
            return output_path
            
        except urllib.error.HTTPError as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            raise Exception(f"❌ HTTP Error {e.code}: {e.reason}")
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            raise Exception(f"❌ Error en descarga: {e}")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Samsung OTA Downloader - Descarga update.zip para adb sideload",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📱 Este script descarga archivos OTA (update.zip) para adb sideload
   NO descarga firmware para Odin (.tar.md5)

Diferencias:
  • Odin:        Firmware completo (AP, BL, CP, CSC .tar.md5)
  • adb sideload: Actualización OTA (update.zip)

Servidores usados (del análisis de APKs):
  • https://fota-cloud-dn.ospserver.net (FotaAgent.apk)
  • https://vas.samsungapps.com (OMCAgent5.apk)

Ejemplos:
  # Verificar OTA disponible
  %(prog)s -m SM-S916B -r TPA --check-only
  
  # Descargar OTA
  %(prog)s -m SM-S916B -r TPA -o ./ota_updates

Instalación con adb sideload:
  1. Descargar update.zip con este script
  2. Reiniciar en recovery: adb reboot recovery
  3. Seleccionar "Apply update from ADB"
  4. Ejecutar: adb sideload update.zip
  5. Esperar a que complete

Modelos comunes:
  SM-S916B  Galaxy S23
  SM-S918B  Galaxy S23 Ultra
  SM-G990B  Galaxy S21 FE

CSC comunes:
  TPA  Taiwán        DBT  Alemania
  OXM  Europa Multi  XAA  USA
        """
    )
    
    parser.add_argument('-m', '--model', required=True,
                       help='Modelo Samsung (ej: SM-S916B)')
    parser.add_argument('-r', '--region', required=True,
                       help='Código CSC (ej: TPA, OXM, DBT)')
    parser.add_argument('-o', '--output-dir', default='.',
                       help='Directorio de salida (default: actual)')
    parser.add_argument('-c', '--check-only', action='store_true',
                       help='Solo verificar versión sin descargar')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Salida detallada')
    
    args = parser.parse_args()
    
    # Validar modelo
    if not args.model.startswith('SM-'):
        print(f"⚠️  Modelo '{args.model}' no parece código Samsung válido (deben empezar con SM-)")
        response = input("¿Continuar? (s/n): ")
        if response.lower() != 's':
            return 0
    
    # Validar CSC
    if len(args.region) != 3 or not args.region.isalpha():
        print(f"⚠️  CSC '{args.region}' no parece válido (deben ser 3 letras)")
        response = input("¿Continuar? (s/n): ")
        if response.lower() != 's':
            return 0
    
    # Crear directorio de salida
    if not args.check_only:
        os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        print("╔════════════════════════════════════════════════════╗")
        print("║   Samsung OTA Downloader (adb sideload)           ║")
        print("╚════════════════════════════════════════════════════╝")
        print("Basado en análisis de FotaAgent.apk y OMCAgent5.apk")
        print("Servidores: ospserver.net (de análisis, NO terceros)")
        print("═" * 52)
        print(f"📱 Modelo:  {args.model}")
        print(f"🌍 Región:  {args.region}")
        print()
        
        downloader = SamsungOTADownloader(args.model, args.region)
        
        # Obtener información OTA
        ota_info = downloader.get_ota_version_info()
        
        print("✅ Información OTA encontrada:")
        print(f"   ├─ Versión: {ota_info['version']}")
        print(f"   ├─ Modelo:  {ota_info['model']}")
        print(f"   └─ CSC:     {ota_info['csc']}")
        print()
        
        if args.check_only:
            print("✅ Verificación completa")
            print()
            print("💡 Para descargar:")
            print(f"   python3 {sys.argv[0]} -m {args.model} -r {args.region} -o ./ota")
            return 0
        
        # Confirmar descarga
        if 'size' in ota_info:
            size_mb = int(ota_info['size']) / (1024*1024)
            print(f"⚠️  Tamaño aproximado: {size_mb:.2f} MB")
        print(f"   Directorio: {os.path.abspath(args.output_dir)}")
        response = input("¿Descargar OTA? (s/n): ")
        if response.lower() != 's':
            print("Descarga cancelada")
            return 0
        
        # Descargar OTA
        print()
        ota_file = downloader.download_ota(ota_info, args.output_dir)
        
        print()
        print("╔════════════════════════════════════════════════════╗")
        print("║          ✅ ¡Descarga Completa!                     ║")
        print("╚════════════════════════════════════════════════════╝")
        print(f"📁 Archivo: {os.path.abspath(ota_file)}")
        print()
        print("📝 Para instalar con adb sideload:")
        print("   1. Reiniciar en recovery:")
        print("      adb reboot recovery")
        print()
        print("   2. En el menú recovery:")
        print("      Seleccionar 'Apply update from ADB'")
        print()
        print("   3. Ejecutar en PC:")
        print(f"      adb sideload {os.path.basename(ota_file)}")
        print()
        print("   4. Esperar a que complete la instalación")
        print()
        print("⚠️  IMPORTANTE:")
        print("   - Batería mínima 50%")
        print("   - No desconectar durante la instalación")
        print("   - Backup de datos recomendado")
        print()
        
        return 0
        
    except KeyboardInterrupt:
        print()
        print("⚠️  Cancelado por usuario")
        return 1
    except Exception as e:
        print()
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
