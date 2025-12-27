# Samsung FOTA Checker - Sin Dependencias Externas

## Descripción

Script en Python PURO (sin dependencias externas) que verifica el firmware disponible para dispositivos Samsung directamente desde los servidores oficiales de FOTA.

**✅ VENTAJAS:**
- **Sin dependencias externas** - Solo usa librerías estándar de Python 3
- **Sin requests** - Usa urllib (incluido en Python)
- **Sin cryptography** - No requiere pycryptodome
- Funciona directamente después de clonar el repositorio

## Análisis Realizado

### Binarios y APKs Analizados

1. **FotaAgent.apk** (`system/system/priv-app/FotaAgent/`)
   - Extraídos endpoints: `https://fota-cloud-dn.ospserver.net/firmware/`
   - Protocolo: HTTP/XML simple sin encriptación compleja

2. **OMCAgent5.apk** (`system/system/priv-app/OMCAgent5/`)
   - Agente de actualización OTA/OMC
   - Usa mismo protocolo FOTA

3. **Información del Dispositivo Real:**
   ```
   Model: SM-S916B
   CSC: TPA (Caribbean - Flow/Digicel)
   Serial (UN): CE0523757243B468157E
   Boot ID: 8df0c594-9852-48ff-a649-4d6824eb9fbb
   ```

### Protocolo FOTA Descubierto

Samsung usa un protocolo simple HTTP/XML para consulta de firmware:

```
URL: https://fota-cloud-dn.ospserver.net/firmware/{CSC}/{MODEL}/version.xml
Método: GET
Headers: User-Agent: FOTA UA
Respuesta: XML con información de firmware disponible
```

**No requiere:**
- ❌ Autenticación compleja
- ❌ Encriptación AES
- ❌ NONCE/Signature
- ❌ IMEI verificado

**Sí requiere:**
- ✅ Modelo correcto (ej: SM-S916B)
- ✅ Código CSC válido (ej: TPA, OXM, BTU)

## Instalación

```bash
# NO requiere instalación de dependencias
# Solo Python 3.6+ (ya incluido en la mayoría de sistemas)

# Clonar repositorio
git clone https://github.com/extremerom/UN1CA-firmware-dm2q.git
cd UN1CA-firmware-dm2q

# Dar permisos de ejecución
chmod +x samsung_fota_checker.py

# Ejecutar directamente
python3 samsung_fota_checker.py -m SM-S916B -r TPA
```

## Uso

### Verificar Firmware para tu Dispositivo (TPA Region)

```bash
python3 samsung_fota_checker.py -m SM-S916B -r TPA
```

**Salida:**
```
======================================================================
Samsung FOTA Firmware Checker
Pure Python Implementation - No External Dependencies
======================================================================
Model: SM-S916B
Region: TPA
Output: .
======================================================================

[*] Checking firmware for SM-S916B (TPA)...
[*] URL: https://fota-cloud-dn.ospserver.net/firmware/TPA/SM-S916B/version.xml

[+] Firmware found!
======================================================================
[*] Firmware download information:
    Version: S916BXXS8EYK5/S916BOWO8EYK5/S916BXXU8EYI5
    Android: 16
    PDA: S916BXXS8EYK5
    CSC: S916BOWO8EYK5
    Modem: S916BXXU8EYI5

[+] Firmware information saved to: ./SM-S916B_TPA_firmware_info.txt
[+] Operation completed successfully!
```

### Otras Regiones

```bash
# Europa (Multi-CSC)
python3 samsung_fota_checker.py -m SM-S916B -r OXM

# Reino Unido
python3 samsung_fota_checker.py -m SM-S916B -r BTU

# Alemania
python3 samsung_fota_checker.py -m SM-S916B -r DBT

# España
python3 samsung_fota_checker.py -m SM-S916B -r PHE
```

### Otros Modelos Galaxy

```bash
# Galaxy S23 Ultra
python3 samsung_fota_checker.py -m SM-S918B -r TPA

# Galaxy S23
python3 samsung_fota_checker.py -m SM-S911B -r TPA

# Galaxy S24+
python3 samsung_fota_checker.py -m SM-S926B -r TPA
```

## Parámetros

| Parámetro | Descripción | Requerido | Ejemplo |
|-----------|-------------|-----------|---------|
| `-m, --model` | Modelo del dispositivo | Sí | `SM-S916B` |
| `-r, --region` | Código CSC/Región | Sí | `TPA` |
| `-o, --output` | Directorio de salida | No | `./downloads` |

## Códigos CSC Comunes

### Caribe y América Latina
- **TPA** - Caribbean (Flow, Digicel, Cable & Wireless) ⭐ **Tu región**
- **TTT** - Trinidad and Tobago
- **TGT** - Guatemala
- **CHO** - Chile
- **ZTO** - Brazil

### Europa
- **OXM** - Open Europe (Multi-CSC)
- **BTU** - United Kingdom
- **DBT** - Germany (Deutschland)
- **XEF** - France
- **PHE** - Spain
- **ITV** - Italy

### América del Norte
- **XAR** - USA (AT&T)
- **TMB** - USA (T-Mobile)
- **VZW** - USA (Verizon)
- **SPR** - USA (Sprint)

## Archivo de Salida

El script genera un archivo de texto con la información del firmware:

**Nombre:** `{MODELO}_{REGION}_firmware_info.txt`

**Ejemplo:** `SM-S916B_TPA_firmware_info.txt`

**Contenido:**
```
Samsung Firmware Information
==================================================

Model: SM-S916B
Region (CSC): TPA
Firmware Version: S916BXXS8EYK5/S916BOWO8EYK5/S916BXXU8EYI5
Android Version: 16
PDA: S916BXXS8EYK5
CSC: S916BOWO8EYK5
Modem: S916BXXU8EYI5

==================================================
Download this firmware using:
- Samsung Smart Switch
- Samsung Kies
- OTA update on device
```

## Información Técnica

### Estructura del XML de Respuesta

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<versioninfo>
    <url>https://fota-cloud-dn.ospserver.net/firmware/</url>
    <firmware>
        <model>SM-S916B</model>
        <cc>TPA</cc>
        <version>
            <latest o="16">S916BXXS8EYK5/S916BOWO8EYK5/S916BXXU8EYI5</latest>
            <upgrade>
                <value rcount='9' fwsize='446960038'>...</value>
                <!-- Más versiones disponibles -->
            </upgrade>
        </version>
    </firmware>
</versioninfo>
```

### Campos del Firmware

- **PDA**: Versión del software del sistema (Android, aplicaciones)
- **CSC**: Versión de configuración regional (idioma, apps específicas)
- **MODEM**: Versión del firmware del módem/radio
- **Android (o)**: Versión de Android (16 = Android Baklava)

### Formato de Versión

```
Formato: [PDA]/[CSC]/[MODEM]
Ejemplo: S916BXXS8EYK5/S916BOWO8EYK5/S916BXXU8EYI5

Desglose PDA: S916BXXS8EYK5
  S916B - Modelo (Galaxy S23+)
  XX - Región (XX = Multi-región)
  S - Año (S = 2024/2025)
  8 - Trimestre
  EY - Build interno
  K - Revisión mayor
  5 - Revisión menor
```

## Diferencias con Script Anterior

| Característica | samsung_firmware_downloader.py | samsung_fota_checker.py |
|----------------|-------------------------------|------------------------|
| Dependencias | requests, pycryptodome | **Ninguna** ✅ |
| Instalación | `pip install -r requirements.txt` | **No requiere** ✅ |
| Complejidad | Alta (AES, NONCE, Auth) | Baja (HTTP/XML simple) ✅ |
| Velocidad | Media | **Rápida** ✅ |
| Funciona con TPA | ❌ No (error 404) | ✅ Sí |
| Descarga binario | Intenta (falla) | No (solo info) |
| Verificación | ✅ Sí | ✅ Sí |

## Limitaciones

1. **Solo verifica firmware disponible** - No descarga el binario directamente
2. **Descarga real requiere**:
   - Samsung Smart Switch (PC)
   - Samsung Kies
   - OTA en el dispositivo
3. **Algunos modelos/regiones** pueden no estar en el servidor FOTA público

## Ventajas

✅ **Sin dependencias externas** - Funciona con Python estándar  
✅ **Rápido y simple** - No requiere autenticación compleja  
✅ **Información precisa** - Obtiene datos directos de Samsung  
✅ **Funciona con TPA** - Probado con región Caribbean  
✅ **Código limpio** - Fácil de entender y modificar  
✅ **Sin instalación** - Solo clonar y ejecutar  

## Solución de Problemas

### Error: "Firmware not found (404)"

**Causa:** Modelo o región incorrectos

**Solución:**
```bash
# Verificar modelo exacto
cat /system/build.prop | grep ro.product.model

# Verificar CSC
getprop ro.csc.sales_code

# Probar con región alternativa
python3 samsung_fota_checker.py -m SM-S916B -r OXM
```

### Error: "URL Error"

**Causa:** Sin conexión a Internet

**Solución:**
```bash
# Verificar conectividad
ping fota-cloud-dn.ospserver.net

# Verificar DNS
nslookup fota-cloud-dn.ospserver.net
```

## Uso desde Termux (Android)

```bash
# En Termux
pkg install python
cd ~/storage/downloads
git clone https://github.com/extremerom/UN1CA-firmware-dm2q.git
cd UN1CA-firmware-dm2q

# Ejecutar con información de tu dispositivo
python samsung_fota_checker.py -m SM-S916B -r TPA
```

## Información del Dispositivo Analizado

```
Dispositivo: Samsung Galaxy S23+ (dm2q)
Modelo: SM-S916B
Región: TPA (Caribbean)
Serial (UN): CE0523757243B468157E
Boot ID: 8df0c594-9852-48ff-a649-4d6824eb9fbb

Firmware Actual:
PDA: S916BXXS8EYK5
CSC: S916BOXM8EYK5 (extraído del repositorio)
Modem: S916BXXU8EYI5
Android: 16 (Baklava)
Build: BP2A.250605.031.A3
Parche: 2025-12-01
```

## Próximos Pasos

Para descargar el firmware encontrado:

1. **Samsung Smart Switch (Recomendado)**
   - Descargar de: https://www.samsung.com/smart-switch/
   - Conectar dispositivo
   - Seleccionar "Actualizar" o "Restaurar"

2. **Samsung Kies**
   - Para modelos más antiguos
   - Descarga similar a Smart Switch

3. **OTA en Dispositivo**
   - Configuración → Actualización de software
   - Descargar e instalar

## Referencias

- Código fuente: `samsung_fota_checker.py`
- Análisis binario: FotaAgent.apk, OMCAgent5.apk
- Servidor FOTA: https://fota-cloud-dn.ospserver.net
- Documentación técnica: `ANALISIS_TECNICO.md`

## Licencia

MIT License - Uso libre con fines educativos y personales

## Autor

Generado mediante análisis de:
- Firmware Samsung Galaxy S23+ (dm2q)
- APKs del sistema (FotaAgent, OMCAgent)
- Información del dispositivo real
- Protocolo FOTA de Samsung

---

**✅ Script probado y funcional con región TPA (Caribbean)**
