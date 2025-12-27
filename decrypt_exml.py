#!/usr/bin/env python3
"""
Samsung FotaAgent EXML Decryptor
=================================

Desencripta archivos .exml de FotaAgent usando las claves encontradas en libdprw.so

Basado en análisis de:
- libdprw.so (funciones JNI de encriptación)
- Claves extraídas del binario
- Análisis de FotaAgent.apk

Autor: Análisis de firmware Samsung
Fecha: 2025-12-27
"""

import os
import sys
from pathlib import Path
from typing import Optional, List
import struct

# Add user site-packages to path
sys.path.insert(0, os.path.expanduser('~/.local/lib/python3.10/site-packages'))

try:
    from Crypto.Cipher import AES, DES, DES3
    from Crypto.Util.Padding import unpad
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️  pycryptodome no instalado. Instalando...")
    os.system("pip install --user pycryptodome")
    # Retry import
    sys.path.insert(0, os.path.expanduser('~/.local/lib/python3.10/site-packages'))
    from Crypto.Cipher import AES, DES, DES3
    from Crypto.Util.Padding import unpad
    CRYPTO_AVAILABLE = True


class EXMLDecryptor:
    """
    Desencriptador de archivos .exml de FotaAgent
    """
    
    # Claves extraídas de libdprw.so mediante análisis de strings
    KEYS = {
        'key1': b'2cbmvps5z4',
        'key2': b'j5p7ll8g33',
        'key3': bytes.fromhex('5763D0052DC1462E13751F753384E9A9'),
        'key4': bytes.fromhex('AF87056C54E8BFD81142D235F4F8E552'),
        'key5': b'dkaghghkehlsvkdlsmld',  # Clave larga encontrada
    }
    
    # IVs comunes en Samsung
    IVS = [
        b'\x00' * 16,  # IV nulo
        bytes.fromhex('0102030405060708090A0B0C0D0E0F10'),
        bytes.fromhex('1234567890ABCDEF1234567890ABCDEF'),
    ]
    
    def __init__(self):
        self.decrypted_count = 0
        self.failed_count = 0
    
    def _print(self, message: str, prefix: str = "ℹ️"):
        """Imprimir mensaje"""
        print(f"{prefix}  {message}")
    
    def _prepare_key(self, key: bytes, key_size: int) -> bytes:
        """Preparar clave al tamaño correcto"""
        if len(key) == key_size:
            return key
        elif len(key) > key_size:
            return key[:key_size]
        else:
            # Pad con ceros
            return key + b'\x00' * (key_size - len(key))
    
    def _try_aes_decrypt(self, data: bytes, key: bytes, iv: bytes) -> Optional[bytes]:
        """Intentar desencriptar con AES"""
        try:
            # AES-128
            if len(key) <= 16:
                key_128 = self._prepare_key(key, 16)
                cipher = AES.new(key_128, AES.MODE_CBC, iv[:16])
                decrypted = cipher.decrypt(data)
                # Verificar si es XML válido
                if decrypted.startswith(b'<?xml') or decrypted.startswith(b'<'):
                    return unpad(decrypted, AES.block_size)
            
            # AES-256
            key_256 = self._prepare_key(key, 32)
            cipher = AES.new(key_256, AES.MODE_CBC, iv[:16])
            decrypted = cipher.decrypt(data)
            if decrypted.startswith(b'<?xml') or decrypted.startswith(b'<'):
                return unpad(decrypted, AES.block_size)
                
        except Exception:
            pass
        
        return None
    
    def _try_des_decrypt(self, data: bytes, key: bytes) -> Optional[bytes]:
        """Intentar desencriptar con DES/3DES"""
        try:
            # DES
            if len(key) >= 8:
                key_des = key[:8]
                cipher = DES.new(key_des, DES.MODE_ECB)
                decrypted = cipher.decrypt(data)
                if decrypted.startswith(b'<?xml') or decrypted.startswith(b'<'):
                    return decrypted
            
            # 3DES
            if len(key) >= 24:
                key_3des = key[:24]
                cipher = DES3.new(key_3des, DES3.MODE_ECB)
                decrypted = cipher.decrypt(data)
                if decrypted.startswith(b'<?xml') or decrypted.startswith(b'<'):
                    return decrypted
            elif len(key) >= 16:
                # 3DES con clave de 16 bytes (usa los primeros 8 dos veces)
                key_3des = key[:16] + key[:8]
                cipher = DES3.new(key_3des, DES3.MODE_ECB)
                decrypted = cipher.decrypt(data)
                if decrypted.startswith(b'<?xml') or decrypted.startswith(b'<'):
                    return decrypted
                
        except Exception:
            pass
        
        return None
    
    def _try_xor_decrypt(self, data: bytes, key: bytes) -> Optional[bytes]:
        """Intentar desencriptar con XOR simple"""
        try:
            decrypted = bytearray()
            key_len = len(key)
            
            for i, byte in enumerate(data):
                decrypted.append(byte ^ key[i % key_len])
            
            decrypted = bytes(decrypted)
            if decrypted.startswith(b'<?xml') or decrypted.startswith(b'<'):
                return decrypted
                
        except Exception:
            pass
        
        return None
    
    def decrypt_file(self, input_path: str, output_path: str = None) -> bool:
        """
        Desencriptar archivo .exml
        
        Args:
            input_path: Ruta al archivo .exml encriptado
            output_path: Ruta para guardar el XML desencriptado (opcional)
        
        Returns:
            True si se desencriptó exitosamente
        """
        if not os.path.exists(input_path):
            self._print(f"❌ Archivo no encontrado: {input_path}")
            return False
        
        # Leer archivo encriptado
        with open(input_path, 'rb') as f:
            encrypted_data = f.read()
        
        self._print(f"Desencriptando: {os.path.basename(input_path)}", "🔐")
        self._print(f"Tamaño: {len(encrypted_data)} bytes")
        
        # Intentar diferentes métodos de desencriptación
        decrypted = None
        method_used = None
        
        # 1. Intentar AES con todas las combinaciones
        for key_name, key in self.KEYS.items():
            for iv in self.IVS:
                result = self._try_aes_decrypt(encrypted_data, key, iv)
                if result:
                    decrypted = result
                    method_used = f"AES (key={key_name})"
                    break
            if decrypted:
                break
        
        # 2. Intentar DES/3DES
        if not decrypted:
            for key_name, key in self.KEYS.items():
                result = self._try_des_decrypt(encrypted_data, key)
                if result:
                    decrypted = result
                    method_used = f"DES/3DES (key={key_name})"
                    break
        
        # 3. Intentar XOR simple
        if not decrypted:
            for key_name, key in self.KEYS.items():
                result = self._try_xor_decrypt(encrypted_data, key)
                if result:
                    decrypted = result
                    method_used = f"XOR (key={key_name})"
                    break
        
        if not decrypted:
            self._print("❌ No se pudo desencriptar con ningún método conocido")
            self.failed_count += 1
            return False
        
        # Guardar archivo desencriptado
        if not output_path:
            output_path = input_path.replace('.exml', '.xml')
        
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(decrypted)
        
        self._print(f"✅ Desencriptado con {method_used}")
        self._print(f"💾 Guardado en: {output_path}")
        self._print(f"📏 Tamaño desencriptado: {len(decrypted)} bytes")
        
        # Mostrar primeras líneas
        try:
            preview = decrypted.decode('utf-8').split('\n')[:3]
            self._print("📄 Vista previa:")
            for line in preview:
                print(f"    {line}")
        except:
            pass
        
        self.decrypted_count += 1
        return True
    
    def decrypt_directory(self, input_dir: str, output_dir: str = None, recursive: bool = True):
        """
        Desencriptar todos los archivos .exml en un directorio
        
        Args:
            input_dir: Directorio con archivos .exml
            output_dir: Directorio de salida (opcional)
            recursive: Buscar recursivamente en subdirectorios
        """
        if not output_dir:
            output_dir = input_dir + "_decrypted"
        
        self._print(f"Buscando archivos .exml en: {input_dir}", "🔍")
        
        # Encontrar todos los archivos .exml
        if recursive:
            exml_files = list(Path(input_dir).rglob('*.exml'))
        else:
            exml_files = list(Path(input_dir).glob('*.exml'))
        
        if not exml_files:
            self._print("❌ No se encontraron archivos .exml")
            return
        
        self._print(f"Encontrados {len(exml_files)} archivos .exml")
        print("\n" + "="*70)
        
        for exml_file in exml_files:
            # Mantener estructura de directorios
            rel_path = exml_file.relative_to(input_dir)
            output_path = os.path.join(output_dir, str(rel_path).replace('.exml', '.xml'))
            
            self.decrypt_file(str(exml_file), output_path)
            print("-"*70)
        
        print("\n" + "="*70)
        self._print(f"✅ Desencriptados: {self.decrypted_count}", "📊")
        self._print(f"❌ Fallidos: {self.failed_count}", "📊")
        print("="*70 + "\n")


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Samsung FotaAgent EXML Decryptor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Desencriptar un archivo .exml
  python3 %(prog)s -f assets/profile/mformtest2020/mformtest2020_DDF_FUMO.exml

  # Desencriptar todos los .exml en un directorio
  python3 %(prog)s -d /tmp/fotaagent/assets/profile

  # Especificar directorio de salida
  python3 %(prog)s -d assets/profile -o ./decrypted

Claves usadas (extraídas de libdprw.so):
  - 2cbmvps5z4
  - j5p7ll8g33
  - 5763D0052DC1462E13751F753384E9A9
  - AF87056C54E8BFD81142D235F4F8E552
  - dkaghghkehlsvkdlsmld

Métodos de desencriptación probados:
  - AES-128/256 CBC
  - DES/3DES ECB
  - XOR simple
        """
    )
    
    parser.add_argument('-f', '--file',
                        help='Archivo .exml a desencriptar')
    parser.add_argument('-d', '--directory',
                        help='Directorio con archivos .exml')
    parser.add_argument('-o', '--output',
                        help='Archivo o directorio de salida')
    parser.add_argument('--no-recursive', action='store_true',
                        help='No buscar recursivamente en subdirectorios')
    
    args = parser.parse_args()
    
    if not args.file and not args.directory:
        parser.print_help()
        sys.exit(1)
    
    decryptor = EXMLDecryptor()
    
    if args.file:
        success = decryptor.decrypt_file(args.file, args.output)
        sys.exit(0 if success else 1)
    
    if args.directory:
        decryptor.decrypt_directory(
            args.directory,
            args.output,
            recursive=not args.no_recursive
        )
        sys.exit(0 if decryptor.decrypted_count > 0 else 1)


if __name__ == '__main__':
    main()
