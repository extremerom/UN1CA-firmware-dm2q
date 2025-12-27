# Scripts de Descarga de Firmware y Archivos Samsung

Colección completa de scripts para descargar firmware, APKs y archivos desde servidores Samsung oficiales, basados en análisis exhaustivo de ingeniería inversa.

## 📚 Scripts Disponibles

### 1. samsung_neofus_downloader.py ⭐
**Protocolo NeoFUS completo** (servidor real de Smart Switch Mac)

```bash
# Verificar firmware disponible
python3 samsung_neofus_downloader.py -m SM-S916B -r TPA --check-only

# Descargar firmware
python3 samsung_neofus_downloader.py -m SM-S916B -r TPA -i 352496803361546 -o ./firmware
```

**Servidor:** `neofussvr.sslcs.cdngc.net`  
**Estado:** ⚠️ Requiere endpoints exactos (aún en investigación)

### 2. samsung_file_downloader.py ✅
**Descargas funcionales** de imágenes, APKs y actualizaciones

```bash
# Descargar imagen de dispositivo (funciona)
python3 samsung_file_downloader.py --image -m SM-S916B -r TPA

# Descargar Easy Mover APK
python3 samsung_file_downloader.py --easymover -r TPA

# Listar archivos disponibles
python3 samsung_file_downloader.py --list -m SM-S916B -r TPA
```

**Servidor:** `update.kies.samsung.com`, `vas.samsungapps.com`  
**Estado:** ✅ Funcional

### 3. samsung_smartswitch_downloader.py
**Método Smart Switch Mac** (REST API)

```bash
python3 samsung_smartswitch_downloader.py -m SM-S916B -r TPA --check-only
```

**Servidor:** `update.kies.samsung.com`  
**Estado:** ✅ Funcional (solo imágenes PNG, no firmware)

### 4. samsung_downloader_full.py
**Método Android FOTA** con dependencias externas

```bash
python3 samsung_downloader_full.py -m SM-S916B -r TPA \
    -i 352496803361546 \
    --boot-id 8df0c594-9852-48ff-a649-4d6824eb9fbb \
    --ufs-un CE0523757243B468157E
```

**Servidor:** `fota-cloud-dn.ospserver.net`  
**Estado:** ❌ Bloqueado por Akamai CDN (403)

### 5. samsung_firmware_downloader.py
**Método Windows FUS** (sin dependencias)

```bash
python3 samsung_firmware_downloader.py -m SM-S916B -r TPA --check-only
```

**Servidor:** `fus2.shop.v-cdn.net`  
**Estado:** ⚠️ DNS no resuelve

### 6. samsung_ota_downloader.py
**Método Android OTA** (sin dependencias)

```bash
python3 samsung_ota_downloader.py -m SM-S916B -r TPA --check-only
```

**Servidor:** `fota-cloud-dn.ospserver.net`  
**Estado:** ⚠️ Similar a método Android FOTA

## 🎯 Scripts Recomendados

### Para descargar IMÁGENES de dispositivos: ✅
```bash
python3 samsung_file_downloader.py --image -m SM-S916B -r TPA
```
**Resultado:** Descarga imagen PNG del dispositivo (funciona al 100%)

### Para descargar APKs: ✅
```bash
python3 samsung_file_downloader.py --easymover -r TPA
```
**Resultado:** Descarga Easy Mover APK (funciona)

### Para descargar FIRMWARE completo: ⚠️
```bash
python3 samsung_neofus_downloader.py -m SM-S916B -r TPA --check-only
```
**Resultado:** Intenta protocolo NeoFUS (requiere endpoints exactos)

**Recomendación:** Para firmware completo, usar **Smart Switch oficial** hasta completar ingeniería inversa del protocolo NeoFUS.

## 📋 Requisitos

### Scripts sin dependencias externas:
- samsung_firmware_downloader.py
- samsung_ota_downloader.py
- samsung_smartswitch_downloader.py

**Requisitos:** Python 3.6+

### Scripts con dependencias externas:
- samsung_downloader_full.py
- samsung_neofus_downloader.py
- samsung_file_downloader.py

**Instalación:**
```bash
pip install -r requirements.txt
```

**Dependencias:**
- requests>=2.31.0
- cryptography>=41.0.0
- lxml>=4.9.0

## 🌍 Códigos CSC Comunes

```
TPA - Taiwán
XAC - Reino Unido
DBT - Alemania
BTU - Reino Unido
TMB - T-Mobile USA
EUR - Europa
CHN - China
KOR - Corea
USA - Estados Unidos
```

## 📱 Modelos Comunes

```
SM-S916B  - Galaxy S23+
SM-G998B  - Galaxy S21 Ultra
SM-G991B  - Galaxy S21
SM-A525F  - Galaxy A52
SM-N986B  - Galaxy Note20 Ultra
```

## 🔍 Servidores Descubiertos

### Producción
```
https://neofussvr.sslcs.cdngc.net          - NeoFUS (firmware)
https://update.kies.samsung.com            - Kies Update (imágenes, metadatos)
https://vas.samsungapps.com                - VAS (APKs)
https://fota-cloud-dn.ospserver.net        - FOTA Android (Akamai)
http://fus2.shop.v-cdn.net                 - FUS Windows
https://api.sec-smartswitch.com            - Smart Switch API
https://sspc.sec-smartswitch.com           - Smart Switch Content
```

### Staging/Test
```
https://neofusstgsvr.samsungmobile.com     - NeoFUS Staging
```

### Regional
```
https://cnfussvr.sslcs.cdngc.net           - NeoFUS China
```

## 🛠️ Ejemplos de Uso Completos

### Ejemplo 1: Descargar imagen de Galaxy S23+
```bash
python3 samsung_file_downloader.py --image -m SM-S916B -r TPA -o ./descargas
```

**Salida esperada:**
```
✅ Archivo descargado: ./descargas/SM-S916B2023020253340.png
🔐 MD5: 7bb3f5b45b6bd97dc0a7630a747ae435
```

### Ejemplo 2: Verificar firmware con NeoFUS
```bash
python3 samsung_neofus_downloader.py -m SM-S916B -r TPA -i 352496803361546 --check-only
```

**Salida esperada:**
```
⚠️ El servidor NeoFUS requiere endpoints exactos
💡 Recomendación: Usar Smart Switch oficial o capturar tráfico real
```

### Ejemplo 3: Listar archivos disponibles
```bash
python3 samsung_file_downloader.py --list -m SM-S916B -r TPA
```

**Salida esperada:**
```
1. Imagen de dispositivo
   Servidor: update.kies.samsung.com
   ✅ Funcional
   
2. Easy Mover APK
   Servidor: vas.samsungapps.com
   ✅ Funcional
   
3. Firmware completo
   Servidor: neofussvr.sslcs.cdngc.net
   ⚠️ En desarrollo
```

## 📊 Estado de Funcionalidad

| Script | Servidor | Estado | Descarga |
|--------|----------|--------|----------|
| samsung_file_downloader.py | update.kies.samsung.com | ✅ Funcional | Imágenes PNG |
| samsung_file_downloader.py | vas.samsungapps.com | ✅ Funcional | APKs |
| samsung_neofus_downloader.py | neofussvr.sslcs.cdngc.net | ⚠️ Parcial | Firmware (en desarrollo) |
| samsung_smartswitch_downloader.py | update.kies.samsung.com | ✅ Funcional | Imágenes PNG |
| samsung_downloader_full.py | fota-cloud-dn.ospserver.net | ❌ Bloqueado | Firmware (Akamai) |
| samsung_firmware_downloader.py | fus2.shop.v-cdn.net | ❌ DNS | Firmware |
| samsung_ota_downloader.py | fota-cloud-dn.ospserver.net | ⚠️ Limitado | OTA |

## 🔐 Información de Dispositivo Requerida

### Básica (todos los scripts):
- **Modelo:** SM-S916B
- **CSC:** TPA

### Avanzada (scripts FUS):
- **IMEI:** 352496803361546
- **Boot ID:** 8df0c594-9852-48ff-a649-4d6824eb9fbb
- **UFS UN:** CE0523757243B468157E

**Cómo obtener en Android:**
```bash
# Modelo
getprop ro.product.model

# CSC
getprop ro.csc.sales_code

# IMEI
service call iphonesubinfo 1

# Boot ID
cat /proc/sys/kernel/random/boot_id

# UFS UN
cat /sys/class/sec/ufs/un
```

## 🚀 Próximos Pasos

### Para completar descarga de firmware:

1. **Capturar tráfico de Smart Switch real:**
```bash
sudo tcpdump -i any 'host neofussvr.sslcs.cdngc.net' -w neofus.pcap
# Usar Smart Switch oficial para descargar
# Analizar .pcap con Wireshark
```

2. **Usar mitmproxy para interceptar:**
```bash
mitmproxy --ssl-insecure
# Configurar Mac para usar proxy
# Capturar requests/responses
```

3. **Actualizar samsung_neofus_downloader.py:**
- Agregar endpoints exactos descubiertos
- Corregir formato XML del protocolo
- Implementar autenticación completa

## 📖 Documentación Completa

Ver archivos de análisis para información detallada:

- **ANALISIS_FIRMWARE.md** - 477 APKs Android analizadas
- **ANALISIS_SOAGENT.md** - SOAgent76 (Android)
- **ANALISIS_SMARTSWITCH.md** - Smart Switch Windows
- **ANALISIS_SMARTSWITCH_MAC.md** - Smart Switch Mac (básico)
- **ANALISIS_PROFUNDO_SMARTSWITCH_MAC.md** - Análisis exhaustivo Mac
- **ANALISIS_AUTENTICACION.md** - Protección Akamai CDN
- **GUIA_USO_REAL.md** - Guía para dispositivo SM-S916B TPA

## ⚠️ Advertencias

1. **Uso responsable:** Estos scripts son para investigación y uso personal.
2. **Términos de servicio:** Respetar los TOS de Samsung.
3. **Firmware oficial:** Para actualizaciones críticas, usar Smart Switch oficial.
4. **Backup:** Siempre hacer backup antes de flashear firmware.
5. **Garantía:** Flashear firmware puede anular la garantía.

## 🏆 Créditos

Scripts basados en análisis exhaustivo de:
- 477 APKs Android
- Smart Switch Windows (113 MB)
- Smart Switch Mac (150 MB)
- Binarios nativos (.so, .dylib)
- Más de 1 GB de código Samsung analizado

**Fecha:** Diciembre 2025  
**Versiones analizadas:**
- Smart Switch Mac 5.0.43.1
- Smart Switch Windows 5.0.33.0
- FotaAgent Android
- SOAgent76 Android

## 📞 Soporte

Para problemas o preguntas:
1. Revisar documentación en archivos ANALISIS_*.md
2. Verificar que modelo y CSC sean correctos
3. Probar con diferentes servidores
4. Capturar tráfico real para depuración

## 🔄 Actualizaciones

El proyecto está en desarrollo activo. El protocolo NeoFUS está siendo investigado para completar la funcionalidad de descarga de firmware.

**Estado actual:**
- ✅ Descarga de imágenes: Funcional
- ✅ Descarga de APKs: Funcional  
- ⚠️ Descarga de firmware: En desarrollo (requiere protocolo NeoFUS completo)

---

**Última actualización:** 27 de diciembre de 2025
