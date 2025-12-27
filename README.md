# UN1CA Firmware - Samsung Galaxy S23+ (dm2q)

Este repositorio contiene el firmware extraído de un Samsung Galaxy S23+ (modelo SM-S916B) y un script para descargar firmware oficial de Samsung desde sus servidores FOTA.

## 📱 Información del Firmware

| Especificación | Valor |
|----------------|-------|
| **Dispositivo** | Samsung Galaxy S23+ (dm2q) |
| **Modelo** | SM-S916B |
| **Android** | 16 (Baklava) |
| **One UI** | 7.0 |
| **Build** | BP2A.250605.031.A3 |
| **PDA** | S916BXXS8EYK5 |
| **CSC** | S916BOXM8EYK5 (OXM - Open Europe) |
| **MODEM** | S916BXXU8EYI5 |
| **Parche de Seguridad** | 2025-12-01 |
| **Fecha de Build** | Fri Nov 28 11:27:08 KST 2025 |

## 🚀 Samsung Firmware Downloader

Este repositorio incluye un **script completo en Python** para descargar firmware oficial de Samsung directamente desde los servidores FOTA de Samsung.

### Características

✅ Descarga firmware oficial de Samsung  
✅ Soporta todos los modelos Galaxy recientes  
✅ Múltiples regiones CSC  
✅ Generación automática de IMEI  
✅ Verificación de integridad  
✅ Interfaz de línea de comandos fácil de usar  
✅ Documentación completa en español  

### Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/extremerom/UN1CA-firmware-dm2q.git
cd UN1CA-firmware-dm2q

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el script
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM --check-only
```

### Uso Básico

```bash
# Descargar firmware para Galaxy S23+ (Europa)
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM

# Solo verificar firmware disponible
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM --check-only

# Descargar con IMEI personalizado
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM -i 359999001234567

# Descargar a directorio específico
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM -o ./downloads
```

## 📚 Documentación

El repositorio incluye documentación completa:

| Documento | Descripción |
|-----------|-------------|
| [**GUIA_RAPIDA.md**](GUIA_RAPIDA.md) | Guía de inicio rápido |
| [**README_FIRMWARE_DOWNLOADER.md**](README_FIRMWARE_DOWNLOADER.md) | Manual completo del downloader |
| [**ANALISIS_TECNICO.md**](ANALISIS_TECNICO.md) | Análisis técnico del protocolo FOTA |
| [**examples.sh**](examples.sh) | Script con ejemplos de uso |

## 🔧 Requisitos

- **Python 3.6+**
- **Librería requests** (`pip install requests`)
- **Conexión a Internet estable**
- **5-10 GB de espacio libre** (para firmware descargado)

## 📦 Contenido del Repositorio

```
UN1CA-firmware-dm2q/
├── samsung_firmware_downloader.py  # Script principal
├── README.md                       # Este archivo
├── GUIA_RAPIDA.md                 # Guía rápida
├── README_FIRMWARE_DOWNLOADER.md  # Documentación completa
├── ANALISIS_TECNICO.md            # Análisis técnico
├── examples.sh                     # Ejemplos de uso
├── requirements.txt                # Dependencias Python
├── .gitignore                      # Archivos ignorados
│
├── system/                         # Partición system extraída
├── vendor/                         # Partición vendor extraída
├── product/                        # Partición product extraída
├── odm/                           # Partición odm extraída
├── system_ext/                    # Extensiones del sistema
├── system_dlkm/                   # Módulos del kernel
├── vendor_dlkm/                   # Módulos del vendor
├── kernel/                        # Kernel y configuración
├── avb/                          # Android Verified Boot
│
└── Archivos de metadatos (build.prop, file_context, etc.)
```

## 🎯 Modelos Soportados

El script soporta todos los modelos Samsung que usan el protocolo FOTA:

### Serie Galaxy S
- SM-S911B/U/N - Galaxy S23
- **SM-S916B/U/N - Galaxy S23+** ⭐ (Este dispositivo)
- SM-S918B/U/N - Galaxy S23 Ultra
- SM-S921B/U/N - Galaxy S24
- SM-S926B/U/N - Galaxy S24+
- SM-S928B/U/N - Galaxy S24 Ultra

### Serie Galaxy A
- SM-A546B/U - Galaxy A54
- SM-A556B/U - Galaxy A55
- SM-A346B/U - Galaxy A34

### Serie Galaxy Z
- SM-F936B/U - Galaxy Z Fold 4
- SM-F946B/U - Galaxy Z Fold 5
- SM-F731B/U - Galaxy Z Flip 5

Y muchos más...

## 🌍 Códigos CSC Soportados

### Europa
- **OXM** - Open Europe (Multi-CSC) ⭐ Recomendado
- BTU - United Kingdom
- DBT - Germany
- XEF - France
- PHE - Spain
- ITV - Italy

### América
- XAR - USA AT&T
- TMB - USA T-Mobile
- VZW - USA Verizon
- ZTO - Brazil

### Asia & Oceanía
- INS - India
- SIN - Singapore
- XSA - Australia

Ver lista completa en [README_FIRMWARE_DOWNLOADER.md](README_FIRMWARE_DOWNLOADER.md)

## 🔍 Análisis del Firmware

Este repositorio es el resultado del análisis completo del firmware Samsung, incluyendo:

### Componentes Analizados

1. **FotaAgent.apk** - Aplicación de actualización OTA
2. **Build.prop** - Propiedades del sistema
3. **APKs del sistema** - Aplicaciones preinstaladas
4. **Librerías nativas (.so)** - Binarios del sistema
5. **Kernel y módulos** - Núcleo del sistema operativo

### Protocolo FOTA Reverse Engineering

El script implementa el protocolo oficial de Samsung FOTA basado en:

- ✅ Análisis de tráfico de red
- ✅ Decompilación de APKs
- ✅ Análisis de binarios
- ✅ Ingeniería inversa del protocolo de autenticación

Ver detalles completos en [ANALISIS_TECNICO.md](ANALISIS_TECNICO.md)

## 💡 Casos de Uso

### 1. Desarrollo de ROMs personalizadas
```bash
# Descargar firmware stock para extraer componentes
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM -o ./stock
```

### 2. Restaurar firmware stock
```bash
# Descargar firmware oficial para restauración
python3 samsung_firmware_downloader.py -m SM-S916B -r BTU
```

### 3. Actualización manual
```bash
# Descargar última actualización disponible
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM --check-only
```

### 4. Análisis de seguridad
```bash
# Descargar múltiples versiones para comparación
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM -v S916BXXS8EYK5
```

## 🛠️ Herramientas Relacionadas

### Para Flashear Firmware
- **Odin** (Windows) - Herramienta oficial de Samsung
- **Heimdall** (Linux/Mac) - Alternativa de código abierto

### Para Análisis
- **APKTool** - Decompilación de APKs
- **jadx** - Análisis de código Java
- **Wireshark** - Análisis de tráfico de red

## 📊 Especificaciones Técnicas

### Hardware (Galaxy S23+)
- **Procesador**: Snapdragon 8 Gen 2 for Galaxy (SM8550-AC)
- **RAM**: 8 GB
- **Almacenamiento**: 256/512 GB
- **Pantalla**: 6.6" Dynamic AMOLED 2X, 120Hz
- **Cámara**: 50MP + 12MP + 10MP

### Software
- **Android**: 16 (Baklava)
- **One UI**: 7.0
- **Kernel**: Linux 6.1
- **SELinux**: Enforcing

## 🔒 Seguridad

Este script:
- ✅ Usa el protocolo oficial de Samsung
- ✅ No modifica ni hackea ningún sistema
- ✅ Descarga firmware firmado oficialmente
- ✅ No requiere root ni permisos especiales
- ✅ Código fuente completamente abierto

## ⚠️ Disclaimer

Este proyecto es solo para propósitos educativos y de desarrollo. El firmware descargado es oficial de Samsung y está firmado digitalmente. Asegúrate de entender lo que estás haciendo antes de flashear cualquier firmware.

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

MIT License - Ver LICENSE para más detalles

## 🙏 Agradecimientos

- Samsung por el protocolo FOTA abierto
- Comunidad XDA Developers
- Todos los desarrolladores de herramientas de análisis de Android

## 📞 Soporte

Si encuentras algún problema:

1. Revisa la documentación completa
2. Busca en issues existentes
3. Abre un nuevo issue con:
   - Modelo del dispositivo
   - Región CSC
   - Mensaje de error completo
   - Versión de Python y SO

## 🔗 Enlaces Útiles

- [XDA Developers Forum](https://forum.xda-developers.com/)
- [SamMobile Firmware Database](https://www.sammobile.com/)
- [Android Source](https://source.android.com/)

---

**Desarrollado con ❤️ para la comunidad de desarrollo Android**

**Última actualización**: Basado en firmware S916BXXS8EYK5 (Android 16, Diciembre 2025)
