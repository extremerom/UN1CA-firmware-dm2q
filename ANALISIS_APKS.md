# Análisis Completo de APKs de Samsung FOTA

## APKs Analizados

### 1. FotaAgent.apk (8.8 MB)
**Ubicación**: `system/system/priv-app/FotaAgent/FotaAgent.apk`

**Servidores Encontrados**:
- `https://fota-cloud-dn.ospserver.net/firmware/` ✅ Principal
- `https://dc.di.atlas.samsung.com` (Knox Enterprise)
- `https://regi.di.atlas.samsung.com` (Knox Registration)

**Archivos Descargados**:
- `/fota/update.zip` - Archivo OTA principal
- `/data/fota/` - Directorio de trabajo
- `/cache/fota/fota.status` - Estado de actualización

**Assets Encontrados**:
- `eternalPolicy.json` - Políticas de configuración
- `SettingsBnRDTD*.xml` - DTDs de backup/restore

### 2. OMCAgent5.apk (6.5 MB)
**Ubicación**: `system/system/priv-app/OMCAgent5/OMCAgent5.apk`

**Servidores Encontrados**:
- `https://vas.samsungapps.com` ✅ Apps/Resources
- `https://vas.samsungapps.com/stub/omcAppCheck.as?hashValue=`
- `https://vas.samsungapps.com/stub/omcAppDownload.as?stduk=`
- `https://vas.samsungapps.com/stub/omcResDownload.as?resourceId=`
- `https://appreport.dev.gras.samsungdm.com` (Dev)
- `https://appreport.stg.gras.samsungdm.com` (Staging)

**Función**: Gestión de CSC (Consumer Software Customization) y apps regionales

### 3. AppUpdateCenter.apk
**Ubicación**: `system/system/priv-app/AppUpdateCenter/AppUpdateCenter.apk`

**Servidores Encontrados**:
- `https://dc.di.atlas.samsung.com`
- `https://regi.di.atlas.samsung.com`

**Función**: Centro de actualizaciones de aplicaciones Samsung

### 4. SOAgent76.apk
**Ubicación**: `system/system/priv-app/SOAgent76/SOAgent76.apk`

**Autenticación Encontrada**:
- `auth_type="sha-256_v2"` ✅
- Usa attestation keys con KeyMint/KeyStore
- Genera nonces con hardware security

**Assets**:
- `SamsungRootCA.crt` - Certificado raíz de Samsung

## Protocolo de Descarga Identificado

### Para Dispositivos Individuales (NO Enterprise)

```
1. Verificación de Firmware:
   URL: https://fota-cloud-dn.ospserver.net/firmware/{CSC}/{MODEL}/version.xml
   Método: GET
   Headers: User-Agent: FOTA UA
   Respuesta: XML con versión disponible

2. Descarga OTA:
   Archivo: /fota/update.zip
   Ubicación: Almacenamiento interno del dispositivo
   Instalación: Via recovery (adb sideload)
```

### Para Enterprise (Knox E-FOTA)

```
1. Registro:
   URL: https://regi.di.atlas.samsung.com
   Requiere: Licencia Knox

2. Check-in/Download:
   URL: https://dc.di.atlas.samsung.com
   Requiere: Autenticación enterprise
```

## Campos de Dispositivo Requeridos

Encontrados en el código:

```java
- IMEI (get36BasedIMEI, getIMEI)
- CSC (getCSC, readCSCVersion, SALESCODE_CSC, VERSION_CSC)
- DevModel (Modelo del dispositivo)
- FotaClientVer (Versión del cliente FOTA)
```

## Autenticación

### Método 1: FOTA Cloud (Usado actualmente) ✅
- **No requiere autenticación compleja**
- Solo verifica modelo y CSC válidos
- Devuelve información de firmware disponible
- **Limitación**: No descarga el binario completo directamente

### Método 2: Samsung Knox FUS (Enterprise)
- Requiere NONCE generation
- Usa AES encryption con claves específicas
- Autenticación basada en attestation
- **Limitación**: Requiere licencia Knox para descarga masiva

### Método 3: Smart Switch (Recomendado para usuarios)
- Descarga completa de firmware
- Interfaz gráfica
- Verificación automática de dispositivo
- https://www.samsung.com/global/download/smartswitchwin/

## Información del Dispositivo Real

Del sistema analizado:

```
Modelo: SM-S916B (Galaxy S23+)
Región: TPA (Caribbean - Flow/Digicel)
Serial: CE0523757243B468157E
Boot ID: 8df0c594-9852-48ff-a649-4d6824eb9fbb

Firmware Actual:
PDA: S916BXXS8EYK5
CSC: S916BOXM8EYK5
Modem: S916BXXU8EYI5
Android: 16 (Baklava)
Build: BP2A.250605.031.A3
```

## Conclusiones del Análisis

### Hallazgos Clave

1. **Servidor Principal**: `fota-cloud-dn.ospserver.net` es el servidor público accesible
2. **Archivo OTA**: `/fota/update.zip` es el archivo que se instala via recovery
3. **Sin Claves Hardcoded**: Las claves FUS no están en los APKs, probablemente en servidor
4. **Autenticación Mínima**: El endpoint público solo requiere modelo/CSC válidos
5. **Knox Enterprise**: Los endpoints atlas.samsung.com requieren licencia enterprise

### Limitaciones Descubiertas

1. **Descarga Directa**: Los servidores FUS pueden bloquear descarga masiva
2. **Autenticación Enterprise**: Knox E-FOTA requiere registro y licencia
3. **Verificación de Dispositivo**: Algunos firmwares verifican IMEI real

### Soluciones Implementadas

✅ **Script Actual** (`samsung_firmware_downloader.py`):
- Usa FOTA cloud para verificación
- Implementa protocolo FUS con fallback
- Funciona con región TPA
- Muestra información de firmware disponible

✅ **Script Alternativo** (`samsung_fota_checker.py`):
- Sin dependencias externas
- Solo verificación (no descarga)
- Más rápido y simple

### Recomendaciones

Para **descargar firmware OTA completo**:

1. **Opción 1 - Smart Switch** (Recomendado):
   ```bash
   # Descargar desde: https://www.samsung.com/smart-switch/
   # Conectar dispositivo y usar "Actualizar" o "Restaurar"
   ```

2. **Opción 2 - Script con información**:
   ```bash
   python3 samsung_firmware_downloader.py -m SM-S916B -r TPA
   # Usa la información para descargar manualmente
   ```

3. **Opción 3 - OTA en dispositivo**:
   ```bash
   # Configuración → Actualización de software
   # Descargar e instalar
   ```

## Archivos del Análisis

```
/tmp/apk_analysis/     - FotaAgent extraído
/tmp/omc_analysis/     - OMCAgent extraído
/tmp/so_analysis/      - SOAgent extraído

classes.dex            - Código compilado
assets/               - Recursos
META-INF/             - Manifiestos y firmas
```

## Referencias Técnicas

- FotaAgent: Gestión de actualizaciones OTA
- OMCAgent: Gestión de CSC y apps regionales
- SOAgent: Seguridad y attestation
- Knox E-FOTA: Solución enterprise (no analizada en detalle)

---

**Análisis completado**: 2025-12-27
**Herramientas usadas**: unzip, strings, grep
**Firmware base**: S916BXXS8EYK5 (Android 16)
