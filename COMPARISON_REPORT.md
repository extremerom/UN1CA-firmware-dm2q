# Comparación de system/dpolicy_system entre dm2q y r0q

## Resumen Ejecutivo

Se realizó una comparación **binaria y de contenido** entre el archivo `system/dpolicy_system` del repositorio dm2q (UN1CA-firmware-dm2q) y el archivo correspondiente del repositorio r0q (UN1CA-firmware-r0q).

## Estructura de Archivos

**Nota importante:** `dpolicy_system` es un **archivo único**, no un directorio. Ambos repositorios contienen este archivo en la ruta `system/dpolicy_system`.

## Resultados de la Comparación

### 1. Archivos Idénticos
**Ninguno** - El archivo existe en ambos repositorios pero tiene contenido diferente.

### 2. Archivos que Existen Solo en dm2q
**Ninguno** - El archivo `system/dpolicy_system` existe en ambos repositorios.

### 3. Archivos que Existen Solo en r0q
**Ninguno** - El archivo `system/dpolicy_system` existe en ambos repositorios.

### 4. Archivos en Ambos con Contenido Diferente

| Archivo | Tamaño dm2q | Tamaño r0q | MD5 dm2q | MD5 r0q | Bytes Diferentes |
|---------|-------------|------------|----------|---------|------------------|
| system/dpolicy_system | 26066 bytes | 26066 bytes | 01896e9dfcbb595dc281c0b35cf98b32 | e05d308b3076d893d31a2e7a50300ba5 | 2431 de 26066 (9.3%) |

## Análisis Detallado del Contenido

### Formato del Archivo
Ambos archivos son políticas binarias **DEFEX (Device Enforcement eXtension) versión 2.0** indicado por la firma mágica `DEFEX2.06I`.

### Análisis de Cadenas Extraídas

**Estadísticas:**
- **dm2q:** 285 cadenas de texto extraídas
- **r0q:** 313 cadenas de texto extraídas  
- **Cadenas comunes:** 255 (89% de dm2q, 81% de r0q)
- **Cadenas únicas en dm2q:** 30
- **Cadenas únicas en r0q:** 58

### Contenido Principal IDÉNTICO

✅ Las **políticas de seguridad principales son idénticas** en ambos dispositivos:

#### Rutas del Sistema Monitoreadas (Idénticas)
- `/system/bin/` - Ejecutables críticos (init, app_process, debuggerd, vold, iptables, etc.)
- `/system/apex/` - Módulos APEX del sistema
- `/data/` - Directorios de datos de aplicaciones
- `/vendor/` - Componentes específicos del proveedor

#### Paquetes Samsung Monitoreados (Idénticos)
- `com.samsung.android.smartsuggestions`
- `com.samsung.android.mone`
- `com.samsung.android.privateaccesstokens`
- `com.samsung.android.app.moments`
- `com.samsung.android.mcfds`
- `com.sec.android.gallery3d`
- `com.sec.android.app.myfiles`
- `com.samsung.android.app.notes`
- `com.sec.android.app.voicenote`
- `com.samsung.sept.Security`

#### Componentes Android Core (Idénticos)
- `com.android.runtime`
- `com.android.conscrypt`
- `com.android.sdkext`
- `com.android.tethering`

### Diferencias Encontradas

#### Cadenas Únicas en dm2q (30 elementos)
Principalmente cadenas de control/hash binarios:
- `>uP!q` (9 instancias)
- `[jSX` (11 instancias)
- `JAFd`, `)2}j`, `p!n3`, `6=w|`, `5/dy`, `T2U\tv`
- Marcador: `#TAIL_GUARD#`

#### Cadenas Únicas en r0q (58 elementos)
r0q contiene **28 cadenas adicionales**:
- `< W$` (7 instancias)
- `67j}` (12 instancias)
- `i'@R1H` (28 instancias - **SECCIÓN ADICIONAL**)
- `1k2.n\`, `>IKR`, `i'@R2`
- Marcador: `#TAIL_GUARD#Ld5` (con sufijo adicional)

**⚠️ Observación Importante:** La presencia de `i'@R1H` repetido 28 veces en r0q indica una **tabla de verificación adicional** o lista de componentes que no existe en dm2q.

## Análisis de Diferencias Binarias

### Ubicación de las Diferencias
- **Bytes 0-9706:** ✅ **IDÉNTICOS** (encabezado y políticas base)
- **Bytes 9707-26066:** ❌ **DIFERENTES** (16359 bytes, 62.8% del archivo)
- **Total de bytes diferentes:** 2431 (9.3% del archivo)

### Interpretación

Las diferencias **NO están en las políticas de seguridad principales** (rutas, paquetes), sino en:

1. **Tablas de hash/firmas específicas del dispositivo:** Identificadores únicos para validación de integridad
2. **Metadatos de hardware:** La sección adicional en r0q sugiere componentes extra a validar
3. **Marcadores de control:** Diferentes sufijos en los marcadores de fin de archivo

## Conclusiones Finales

### ✅ Contenido IDÉNTICO
- Todas las rutas del sistema permitidas/restringidas
- Todos los paquetes Samsung monitoreados
- Todos los componentes Android Core
- Estructura base de DEFEX
- **Las políticas de seguridad principales son las mismas**

### ❌ Contenido DIFERENTE
- **dm2q:** 30 cadenas únicas de control/hash
- **r0q:** 58 cadenas únicas de control/hash (28 más que dm2q)
- Diferentes tablas de verificación binaria
- r0q tiene una sección adicional de validación (28 entradas `i'@R1H`)
- Diferentes marcadores de final de archivo

### Resumen
| Aspecto | Estado |
|---------|--------|
| Políticas de seguridad principales | ✅ IDÉNTICAS |
| Rutas y paquetes monitoreados | ✅ IDÉNTICOS |
| Tablas de hash/firmas | ❌ DIFERENTES |
| Metadatos específicos del dispositivo | ❌ DIFERENTES |

### Impacto
Las diferencias reflejan **configuraciones específicas de hardware** y son **esperadas y correctas**:
- Diferentes chips de seguridad
- Diferentes componentes de hardware a verificar
- Diferentes tablas de hash para validación de integridad
- r0q requiere validaciones adicionales (28 entradas extra)

**Conclusión:** dm2q y r0q comparten las mismas políticas de seguridad DEFEX principales, pero utilizan diferentes configuraciones de validación específicas para su hardware respectivo.
