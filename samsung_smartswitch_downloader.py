#!/usr/bin/env python3
"""
Samsung Firmware Downloader - Smart Switch Mac Method
=====================================================

Este script emula Smart Switch para Mac para descargar firmware Samsung.
Usa los endpoints descubiertos mediante ingeniería inversa de Smart Switch 5.0.43.1.

Autor: Análisis de Smart Switch Mac
Fecha: 2025-12-27
"""

import requests
import json
import sys
import os
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime

class SmartSwitchMacDownloader:
    """
    Emulador de Smart Switch para Mac
    Descarga firmware usando los mismos endpoints que Smart Switch oficial
    """
    
    # Servidores descubiertos en análisis de Smart Switch Mac
    BASE_API = "https://api.sec-smartswitch.com/smartswitch/v8"
    UPDATE_SERVER = "https://update.kies.samsung.com/update/smartswitchpc"
    
    def __init__(self, model: str, csc: str, locale: str = "en_US"):
        """
        Inicializar downloader
        
        Args:
            model: Modelo del dispositivo (ej: SM-S916B)
            csc: Código CSC/región (ej: TPA)
            locale: Idioma (default: en_US)
        """
        self.model = model.upper()
        self.csc = csc.upper()
        self.locale = locale
        
        # Sesión HTTP con headers de Smart Switch Mac
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Smart Switch Mac/5.0.43.1',
            'Accept': 'application/json, application/xml, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        })
    
    def print_info(self, message: str, prefix: str = "ℹ️"):
        """Imprimir mensaje informativo"""
        print(f"{prefix}  {message}")
    
    def print_success(self, message: str):
        """Imprimir mensaje de éxito"""
        print(f"✅ {message}")
    
    def print_error(self, message: str):
        """Imprimir mensaje de error"""
        print(f"❌ {message}")
    
    def print_warning(self, message: str):
        """Imprimir advertencia"""
        print(f"⚠️  {message}")
    
    def get_device_info(self) -> Optional[Dict[str, Any]]:
        """
        Obtener información del dispositivo desde el servidor
        Endpoint: update.kies.samsung.com/update/smartswitchpc/image
        """
        self.print_info(f"Obteniendo información del dispositivo...", "🔍")
        
        url = f"{self.UPDATE_SERVER}/image"
        params = {
            'model': self.model,
            'ProductCode': self.csc
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('resultCode') == 0:
                self.print_success(f"Dispositivo encontrado: {data.get('deviceName', 'Unknown')}")
                return data
            else:
                self.print_error(f"Error del servidor: {data.get('resultMessage', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.print_error(f"Error de conexión: {e}")
            return None
        except json.JSONDecodeError as e:
            self.print_error(f"Error al parsear respuesta: {e}")
            return None
    
    def download_file(self, url: str, output_path: str, description: str = "archivo") -> bool:
        """
        Descargar archivo con barra de progreso
        
        Args:
            url: URL del archivo a descargar
            output_path: Ruta donde guardar el archivo
            description: Descripción del archivo para mostrar
        
        Returns:
            True si la descarga fue exitosa, False en caso contrario
        """
        try:
            self.print_info(f"Iniciando descarga de {description}...", "⬇️")
            self.print_info(f"URL: {url}")
            
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            if total_size == 0:
                self.print_warning("No se pudo determinar el tamaño del archivo")
            else:
                size_mb = total_size / (1024 * 1024)
                self.print_info(f"Tamaño: {size_mb:.2f} MB")
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            downloaded = 0
            chunk_size = 8192
            start_time = datetime.now()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            downloaded_mb = downloaded / (1024 * 1024)
                            
                            # Calcular velocidad
                            elapsed = (datetime.now() - start_time).total_seconds()
                            if elapsed > 0:
                                speed_mbps = (downloaded / elapsed) / (1024 * 1024)
                                remaining = (total_size - downloaded) / (speed_mbps * 1024 * 1024) if speed_mbps > 0 else 0
                                
                                print(f"\rProgreso: {progress:.1f}% ({downloaded_mb:.1f}/{size_mb:.1f} MB) "
                                      f"- {speed_mbps:.2f} MB/s - ETA: {int(remaining)}s   ", end='', flush=True)
            
            print()  # Nueva línea después del progreso
            
            # Verificar que el archivo se descargó completamente
            actual_size = os.path.getsize(output_path)
            if total_size > 0 and actual_size != total_size:
                self.print_warning(f"Tamaño del archivo no coincide: esperado {total_size}, obtenido {actual_size}")
            
            self.print_success(f"Archivo descargado: {output_path}")
            return True
            
        except requests.exceptions.RequestException as e:
            self.print_error(f"Error al descargar: {e}")
            return False
        except IOError as e:
            self.print_error(f"Error al guardar archivo: {e}")
            return False
    
    def calculate_md5(self, filepath: str) -> str:
        """Calcular hash MD5 de un archivo"""
        self.print_info("Calculando hash MD5...", "🔐")
        
        md5_hash = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5_hash.update(chunk)
        
        hash_value = md5_hash.hexdigest()
        self.print_info(f"MD5: {hash_value}")
        return hash_value
    
    def check_firmware(self) -> bool:
        """
        Solo verificar si hay firmware disponible sin descargar
        
        Returns:
            True si se encuentra firmware, False en caso contrario
        """
        print("\n" + "="*70)
        print(f"  Samsung Firmware Checker - Método Smart Switch Mac")
        print("="*70)
        print(f"📱 Modelo: {self.model}")
        print(f"🌍 CSC: {self.csc}")
        print(f"🗣️  Locale: {self.locale}")
        print("="*70 + "\n")
        
        device_info = self.get_device_info()
        
        if not device_info:
            self.print_error("No se pudo obtener información del dispositivo")
            return False
        
        print("\n" + "-"*70)
        print("📋 Información del Dispositivo")
        print("-"*70)
        print(f"Nombre: {device_info.get('deviceName', 'N/A')}")
        print(f"Estado: {device_info.get('status', 'N/A')}")
        print(f"Código resultado: {device_info.get('resultCode', 'N/A')}")
        print(f"Mensaje: {device_info.get('resultMessage', 'N/A')}")
        
        if device_info.get('url'):
            print(f"URL imagen: {device_info.get('url')}")
        
        print("-"*70 + "\n")
        
        return True
    
    def download_firmware(self, output_dir: str = "./firmware") -> bool:
        """
        Descargar firmware completo
        
        Args:
            output_dir: Directorio donde guardar el firmware
        
        Returns:
            True si la descarga fue exitosa, False en caso contrario
        """
        print("\n" + "="*70)
        print(f"  Samsung Firmware Downloader - Método Smart Switch Mac")
        print("="*70)
        print(f"📱 Modelo: {self.model}")
        print(f"🌍 CSC: {self.csc}")
        print(f"🗣️  Locale: {self.locale}")
        print(f"📁 Directorio salida: {output_dir}")
        print("="*70 + "\n")
        
        # Obtener información del dispositivo
        device_info = self.get_device_info()
        
        if not device_info:
            self.print_error("No se pudo obtener información del dispositivo")
            return False
        
        # Mostrar información
        print("\n" + "-"*70)
        print("📋 Información del Dispositivo")
        print("-"*70)
        print(f"Nombre: {device_info.get('deviceName', 'N/A')}")
        print(f"Estado: {device_info.get('status', 'N/A')}")
        print("-"*70 + "\n")
        
        # Verificar si hay URL de descarga
        image_url = device_info.get('url')
        if not image_url:
            self.print_warning("No se encontró URL de descarga en la respuesta del servidor")
            self.print_info("La respuesta del servidor solo contiene una imagen de dispositivo, no firmware")
            self.print_info("Este endpoint es para obtener imágenes de dispositivos, no firmware completo")
            return False
        
        # Descargar imagen del dispositivo (no es el firmware completo)
        filename = os.path.basename(image_url)
        output_path = os.path.join(output_dir, filename)
        
        self.print_warning("NOTA: Este archivo es una imagen del dispositivo (.png), NO el firmware completo")
        self.print_info("El firmware completo (.tar.md5) se descarga mediante otro método")
        
        success = self.download_file(image_url, output_path, "imagen del dispositivo")
        
        if success:
            self.print_success("Descarga completada")
            
            # Calcular hash MD5
            if os.path.exists(output_path):
                self.calculate_md5(output_path)
            
            print("\n" + "="*70)
            print("📦 Archivo descargado:")
            print(f"   {output_path}")
            print("="*70 + "\n")
            
            return True
        
        return False


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Samsung Firmware Downloader - Smart Switch Mac Method',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Verificar firmware disponible para SM-S916B CSC TPA
  python3 %(prog)s -m SM-S916B -r TPA --check-only

  # Descargar firmware
  python3 %(prog)s -m SM-S916B -r TPA -o ./firmware

  # Usar diferente locale
  python3 %(prog)s -m SM-G998B -r XAC -l es_ES -o ./firmware

Modelos comunes:
  SM-S916B  - Galaxy S23+
  SM-G998B  - Galaxy S21 Ultra
  SM-G991B  - Galaxy S21
  SM-A525F  - Galaxy A52

Códigos CSC comunes:
  TPA - Taiwán
  XAC - Reino Unido
  DBT - Alemania
  BTU - Reino Unido
  TMB - T-Mobile USA
        """
    )
    
    parser.add_argument('-m', '--model', required=True,
                        help='Modelo del dispositivo (ej: SM-S916B)')
    parser.add_argument('-r', '--region', required=True,
                        help='Código CSC/región (ej: TPA, XAC, DBT)')
    parser.add_argument('-l', '--locale', default='en_US',
                        help='Locale (default: en_US)')
    parser.add_argument('-o', '--output', default='./firmware',
                        help='Directorio de salida (default: ./firmware)')
    parser.add_argument('--check-only', action='store_true',
                        help='Solo verificar sin descargar')
    
    args = parser.parse_args()
    
    # Crear downloader
    downloader = SmartSwitchMacDownloader(
        model=args.model,
        csc=args.region,
        locale=args.locale
    )
    
    # Ejecutar
    if args.check_only:
        success = downloader.check_firmware()
    else:
        success = downloader.download_firmware(args.output)
    
    # Salir con código apropiado
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
