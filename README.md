# Samsung Firmware Downloader

Script en Python para descargar firmware oficial de Samsung directamente desde los servidores FOTA de Samsung.

## 🔍 Análisis Realizado

Este script fue creado mediante ingeniería inversa y análisis de múltiples componentes del firmware Samsung:

### APKs Analizadas:
- **FotaAgent.apk** - Agente principal FOTA (Firmware Over The Air)
- **KnoxCore.apk** - Framework de seguridad Knox
- **KnoxGuard.apk** - Servicio de bloqueo remoto
- **KnoxPushManager.apk** - Gestión de notificaciones Knox
- **SmartSwitchAssistant.apk** - Asistente de Smart Switch
- **SecDownloadProvider.apk** - Proveedor de descargas seguras
- **AppUpdateCenter.apk** - Centro de actualizaciones

### Binarios Analizados:
- **libdprw.so** - Biblioteca nativa con funciones de encriptación y claves

### Información Extraída:
- Servidores FOTA de Samsung
- Endpoints de API
- Protocolo de autenticación (HMAC-SHA1)
- Headers HTTP necesarios
- Parámetros del dispositivo
- Formato de respuestas XML

Ver [ANALISIS_FIRMWARE.md](ANALISIS_FIRMWARE.md) para análisis completo.

## 📋 Requisitos

- Python 3.6 o superior
- **NO requiere bibliotecas externas** (solo stdlib de Python)

## 🚀 Uso

### Verificar Última Versión Disponible

```bash
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM --check-only
```

### Descargar Firmware

```bash
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM -o ./descargas
```

### Con IMEI Específico

```bash
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM -i 123456789012345
```

## 📱 Modelos Samsung Soportados

| Modelo | Dispositivo |
|--------|-------------|
| SM-S916B | Galaxy S23 (Internacional) |
| SM-S918B | Galaxy S23 Ultra |
| SM-S911B | Galaxy S23+ |
| SM-G990B | Galaxy S21 FE |
| SM-A536B | Galaxy A53 5G |
| SM-A546B | Galaxy A54 5G |
| SM-S901B | Galaxy S22 |
| SM-N986B | Galaxy Note 20 Ultra |

## 🌍 Códigos CSC Comunes

| Código | Región/País |
|--------|-------------|
| OXM | Europa Open (Multi-CSC) |
| DBT | Alemania (Deutschland) |
| BTU | Reino Unido |
| XAA | USA Desbloqueado |
| XEF | Francia |
| XSP | Singapur |
| TPA | Taiwán |
| KOO | Corea |

## 🔐 Protocolo FUS (Firmware Update Server)

El script implementa el protocolo FUS de Samsung:

1. **getNonce** - Obtiene nonce de autenticación
2. **getVersionLists** - Lista versiones disponibles
3. **getBinaryInform** - Info del binario (tamaño, ruta, CRC)
4. **getBinaryFile** - Descarga el archivo de firmware

### Autenticación

```python
# Datos de autenticación
auth_data = IMEI + MODEL + CSC

# Token de autenticación
auth_token = HMAC-SHA1(nonce, auth_data)
```

## 📦 Archivos de Firmware

Los archivos descargados suelen estar encriptados (.enc2 o .enc4) y contienen:

- **AP** - Application Processor (ROM principal)
- **BL** - Bootloader
- **CP** - Modem/Radio
- **CSC** - Consumer Software Customization
- **HOME_CSC** - CSC sin borrar datos

## 🔓 Desencriptación

Los archivos descargados están encriptados con claves propietarias de Samsung.

Para desencriptar, use:
- **Samsung Smart Switch** (Windows/Mac)
- **SamFirm** (Herramienta comunitaria)
- **Samloader** (Python, herramienta comunitaria)

## 📖 Parámetros

```
-m, --model MODEL         Código de modelo (ej: SM-S916B)
-r, --region REGION       Código CSC (ej: OXM, DBT)
-i, --imei IMEI          IMEI de 15 dígitos (opcional)
-o, --output-dir DIR     Directorio de salida
-c, --check-only         Solo verificar, no descargar
-v, --verbose            Salida detallada
```

## 🛠️ Flasheo del Firmware

1. Descargar el firmware con este script
2. Desencriptar usando Smart Switch o SamFirm
3. Extraer el archivo .zip
4. Usar **Odin** (Windows) para flashear:
   - Cargar AP, BL, CP, CSC en Odin
   - Iniciar dispositivo en Download Mode (Vol- + Vol+ + USB)
   - Conectar y presionar "Start"

## ⚠️ Advertencias

- Los firmwares son archivos grandes (4-6 GB típicamente)
- La descarga puede tomar mucho tiempo
- Los servidores pueden limitar descargas frecuentes
- Algunos firmwares requieren IMEI válido del modelo correcto
- El flasheo incorrecto puede dañar el dispositivo

## 🔬 Servidores Descubiertos

- `fus2.shop.v-cdn.net` - Servidor FUS principal
- `fota-cloud-dn.ospserver.net` - Servidor de descarga
- `fota-secure-dn.ospserver.net` - Servidor seguro
- `cloud-neofussvr.sslcs.cdngc.net` - Servidor alternativo

## 📄 Estructura del Repositorio

```
.
├── samsung_firmware_downloader.py  # Script principal
├── ANALISIS_FIRMWARE.md           # Análisis detallado
├── README.md                      # Este archivo
└── [firmware files]               # Firmware extraído
```

## 🤝 Contribuciones

Este es un proyecto de análisis educativo. El firmware es propiedad de Samsung.

## ⚖️ Disclaimer

Este script es solo para fines educativos y de investigación. Los firmwares son propiedad de Samsung Electronics. Use bajo su propio riesgo.

---

**Fecha de Creación:** Diciembre 2024  
**Firmware Analizado:** SM-S916B (Galaxy S23) - S916BXXS8EYK5
