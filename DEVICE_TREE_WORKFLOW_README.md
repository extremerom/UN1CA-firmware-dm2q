# Workflow de Archivos del Device Tree

## 📋 Descripción

Este workflow busca y sube como artifacts los archivos del device tree especificados en la lista `tree_output.txt` del repositorio de referencia:
https://github.com/Eduardob3677/android_device_samsung_pa1q

## 🚀 Cómo Usar

### Ejecución Manual

1. Ve a la pestaña **Actions** en GitHub
2. Selecciona **Upload Device Tree Files from Expected List**
3. Haz clic en **Run workflow**
4. Selecciona la rama `main`
5. Haz clic en **Run workflow**

### Ejecución Automática

El workflow se ejecuta automáticamente cuando:
- Se hace push a `main` que modifique archivos en: `recovery/`, `system/`, `vendor/`, `prebuilt/`
- Se crea un pull request que modifique esas rutas

## 📦 Qué Busca el Workflow

El workflow descarga la lista de archivos esperados y busca:

| Tipo de Archivo | Cantidad Esperada | Descripción |
|-----------------|-------------------|-------------|
| Módulos kernel (.ko) | 414 | Módulos del kernel de Linux |
| Bibliotecas (.so) | 84 | Bibliotecas compartidas |
| Archivos RC (.rc) | 16 | Scripts de inicialización |
| Archivos XML (.xml) | 10 | Configuraciones XML |
| Build files (.mk, .bp) | 6 | Archivos de compilación Android |
| Scripts shell (.sh) | 4 | Scripts shell |
| Binarios | 7 | Ejecutables binarios |

**Total: 553 archivos**

## 🔍 Búsqueda Exhaustiva

El workflow:
1. Busca cada archivo en **TODO el repositorio** (no solo ubicaciones específicas)
2. Detecta archivos en múltiples ubicaciones
3. Copia la primera instancia encontrada
4. Documenta TODAS las ubicaciones alternativas

## 📊 Documentación Generada

Cada ejecución genera documentación completa:

### 1. README.md
Descripción general del paquete de archivos

### 2. ESTADISTICAS.md
Estadísticas completas con:
- Archivos esperados vs encontrados
- Porcentaje de éxito por tipo
- Resumen en tabla

### 3. ARCHIVOS_FALTANTES.md
Lista detallada de archivos que **NO** se encontraron, organizada por tipo

### 4. VERSIONES_ALTERNATIVAS.md
Archivos encontrados en **múltiples ubicaciones** con todas las rutas documentadas

### 5. ARCHIVOS_ENCONTRADOS.md
Lista completa de archivos encontrados con sus rutas exactas

### 6. MANIFEST.txt
Listado de todos los archivos incluidos en el artifact

## 📁 Estructura del Artifact

```
artifact_output/
├── found_files/
│   ├── modules/          # Módulos del kernel (.ko)
│   ├── libraries/        # Bibliotecas compartidas (.so)
│   ├── binaries/         # Archivos binarios
│   ├── scripts/          # Scripts shell (.sh)
│   ├── configs/          # Archivos XML y RC
│   └── build_files/      # Archivos .mk y .bp
├── docs/                  # Documentación
│   ├── ESTADISTICAS.md
│   ├── ARCHIVOS_FALTANTES.md
│   ├── VERSIONES_ALTERNATIVAS.md
│   └── ARCHIVOS_ENCONTRADOS.md
├── MANIFEST.txt
└── README.md
```

## ⬇️ Descargar Artifacts

Después de la ejecución:

1. Ve a la ejecución del workflow en **Actions**
2. Desplázate hasta la sección **Artifacts**
3. Descarga: `device-tree-files-from-list-[commit-sha]`

Los artifacts se mantienen por **90 días**.

## 🔄 Versiones Alternativas

Cuando un archivo se encuentra en múltiples ubicaciones:
- Se usa la **primera ubicación** encontrada
- **TODAS** las ubicaciones se documentan en `docs/VERSIONES_ALTERNATIVAS.md`
- Esto permite identificar si hay versiones más nuevas en otras ubicaciones

## 📈 Ejemplo de Salida

### Tabla de Estadísticas

| Tipo | Esperados | Encontrados | Faltantes | % Éxito |
|------|-----------|-------------|-----------|---------|
| Módulos (.ko) | 414 | 380 | 34 | 91.8% |
| Bibliotecas (.so) | 84 | 75 | 9 | 89.3% |
| Scripts (.sh) | 4 | 4 | 0 | 100.0% |
| ...

### Archivo con Múltiples Ubicaciones

```
=== abc.ko (found in 3 locations) ===
./recovery/root/lib/modules/abc.ko
./system/system/lib/modules/abc.ko
./vendor/lib/modules/abc.ko
```

## ⚠️ Notas Importantes

1. **Búsqueda exhaustiva**: El workflow busca en TODO el repositorio, no solo en ubicaciones tradicionales
2. **Primera instancia**: Cuando hay múltiples ubicaciones, se usa la primera encontrada
3. **Documentación completa**: Todas las alternativas se documentan para referencia
4. **Sin duplicados**: Cada archivo se incluye una sola vez en el artifact

## 🆘 Troubleshooting

### El workflow falla

- Verifica que el repositorio de referencia esté accesible
- Revisa los logs del workflow para errores específicos

### Archivos esperados no encontrados

- Consulta `docs/ARCHIVOS_FALTANTES.md` en el artifact
- Verifica si el archivo existe con otro nombre o extensión
- Busca manualmente en el repositorio

### Necesito una versión específica

- Consulta `docs/VERSIONES_ALTERNATIVAS.md`
- Identifica todas las ubicaciones del archivo
- Modifica el workflow si necesitas una ubicación específica

## 📝 Personalización

Para buscar archivos adicionales, edita:
```yaml
.github/workflows/upload-device-tree-artifacts.yml
```

Y agrega los archivos a la lista de búsqueda en el paso correspondiente.

## 📞 Soporte

Si encuentras problemas o necesitas ayuda:
1. Revisa la documentación generada en el artifact
2. Consulta los logs del workflow en Actions
3. Crea un issue en el repositorio
