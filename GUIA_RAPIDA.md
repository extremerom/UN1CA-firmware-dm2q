# Guía Rápida - Samsung Firmware Downloader

## Instalación Rápida

```bash
# Instalar dependencias
pip install requests

# Dar permisos de ejecución
chmod +x samsung_firmware_downloader.py
```

## Uso Básico

### 1. Para el dispositivo actual (Galaxy S23+ / dm2q)

```bash
# Verificar firmware disponible
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM --check-only

# Descargar firmware
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM
```

### 2. Otros modelos comunes

```bash
# Galaxy S23 Ultra
python3 samsung_firmware_downloader.py -m SM-S918B -r OXM

# Galaxy S23
python3 samsung_firmware_downloader.py -m SM-S911B -r OXM

# Galaxy S24+
python3 samsung_firmware_downloader.py -m SM-S926B -r OXM

# Galaxy S24 Ultra
python3 samsung_firmware_downloader.py -m SM-S928B -r OXM
```

### 3. Regiones específicas

```bash
# Reino Unido (BTU)
python3 samsung_firmware_downloader.py -m SM-S916B -r BTU

# Alemania (DBT)
python3 samsung_firmware_downloader.py -m SM-S916B -r DBT

# Francia (XEF)
python3 samsung_firmware_downloader.py -m SM-S916B -r XEF

# España (PHE)
python3 samsung_firmware_downloader.py -m SM-S916B -r PHE
```

## Datos del Dispositivo Actual

Basado en el firmware extraído en este repositorio:

| Campo | Valor |
|-------|-------|
| **Modelo** | SM-S916B |
| **Nombre** | Galaxy S23+ (dm2q) |
| **PDA** | S916BXXS8EYK5 |
| **CSC** | S916BOXM8EYK5 (OXM) |
| **MODEM** | S916BXXU8EYI5 |
| **Android** | 16 (Baklava) |
| **Build** | BP2A.250605.031.A3 |
| **Parche** | 2025-12-01 |

## Comando para este firmware específico

```bash
# Descargar exactamente esta versión
python3 samsung_firmware_downloader.py \
  -m SM-S916B \
  -r OXM \
  -v S916BXXS8EYK5 \
  -o ./downloads
```

## Parámetros Requeridos

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `-m MODEL` | Modelo del dispositivo | SM-S916B |
| `-r REGION` | Código CSC de región | OXM |

## Parámetros Opcionales

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `-i IMEI` | IMEI del dispositivo | 359999001234567 |
| `-v VERSION` | Versión específica | S916BXXS8EYK5 |
| `-o OUTPUT` | Directorio de salida | ./downloads |
| `--check-only` | Solo verificar, no descargar | - |

## Códigos CSC Principales

### Europa
- **OXM** - Open Europe (Multi-CSC) ⭐ Recomendado
- **BTU** - United Kingdom
- **DBT** - Germany
- **XEF** - France
- **PHE** - Spain
- **ITV** - Italy

### América
- **XAR** - USA AT&T
- **TMB** - USA T-Mobile
- **VZW** - USA Verizon
- **ZTO** - Brazil

### Asia
- **INS** - India
- **SIN** - Singapore
- **THL** - Thailand

## Solución de Problemas Rápida

### Error: "Module 'requests' not found"
```bash
pip install requests
```

### Error: "No firmware found"
```bash
# Verificar modelo y región
python3 samsung_firmware_downloader.py -m SM-S916B -r OXM --check-only

# Intentar con CSC diferente
python3 samsung_firmware_downloader.py -m SM-S916B -r BTU --check-only
```

### Error: "Permission denied"
```bash
chmod +x samsung_firmware_downloader.py
```

### Verificar que el script funciona
```bash
python3 samsung_firmware_downloader.py --help
```

## Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| `samsung_firmware_downloader.py` | Script principal |
| `README_FIRMWARE_DOWNLOADER.md` | Documentación completa |
| `ANALISIS_TECNICO.md` | Análisis técnico detallado |
| `GUIA_RAPIDA.md` | Esta guía rápida |
| `examples.sh` | Script con ejemplos |
| `requirements.txt` | Dependencias Python |

## Flujo de Trabajo Típico

```
1. Verificar firmware disponible
   ↓
2. Anotar versión y tamaño
   ↓
3. Descargar firmware
   ↓
4. Verificar descarga completa
   ↓
5. (Opcional) Extraer y flashear con Odin/Heimdall
```

## Ejemplo Completo

```bash
# Paso 1: Crear directorio para descargas
mkdir -p firmwares

# Paso 2: Verificar firmware disponible
python3 samsung_firmware_downloader.py \
  -m SM-S916B \
  -r OXM \
  --check-only

# Paso 3: Descargar firmware
python3 samsung_firmware_downloader.py \
  -m SM-S916B \
  -r OXM \
  -o ./firmwares

# Paso 4: Verificar descarga
ls -lh firmwares/
```

## Información Adicional

### Tamaño típico de firmware
- Galaxy S: 4-6 GB
- Galaxy S+: 5-7 GB
- Galaxy S Ultra: 6-8 GB

### Tiempo de descarga estimado
- Conexión rápida (100 Mbps): 10-15 minutos
- Conexión media (50 Mbps): 20-30 minutos
- Conexión lenta (10 Mbps): 1-2 horas

### Requisitos de sistema
- Python 3.6 o superior
- Conexión a Internet estable
- 10-15 GB de espacio libre (para el archivo descargado)

## Enlaces Útiles

- **Odin**: Herramienta para flashear firmware Samsung (Windows)
- **Heimdall**: Alternativa de código abierto (Linux/Mac)
- **SamMobile**: Base de datos de firmware Samsung
- **XDA Developers**: Foro de desarrollo Android

## Soporte

Para problemas o preguntas:
1. Revisar `README_FIRMWARE_DOWNLOADER.md`
2. Revisar `ANALISIS_TECNICO.md`
3. Abrir un issue en GitHub con:
   - Modelo del dispositivo
   - Región CSC
   - Mensaje de error completo
   - Versión de Python

---

**Nota**: Este script descarga firmware oficial de Samsung. No modifica ni hackea nada, simplemente automatiza el proceso de descarga oficial.
