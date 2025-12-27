#!/bin/bash
#
# Ejemplos de uso del Samsung Firmware Downloader
# Este script muestra varios casos de uso comunes
#

echo "===================================================================="
echo "Samsung Firmware Downloader - Ejemplos de Uso"
echo "===================================================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar ejemplo
show_example() {
    echo -e "${GREEN}Ejemplo $1:${NC} $2"
    echo -e "${YELLOW}Comando:${NC}"
    echo "  $3"
    echo ""
}

# Ejemplo 1: Verificar firmware disponible para Galaxy S23+ Europa
show_example "1" \
    "Verificar firmware disponible para Galaxy S23+ (Europa - OXM)" \
    "python3 samsung_firmware_downloader.py -m SM-S916B -r OXM --check-only"

# Ejemplo 2: Descargar firmware para Galaxy S23+ UK
show_example "2" \
    "Descargar última versión de firmware para Galaxy S23+ (UK - BTU)" \
    "python3 samsung_firmware_downloader.py -m SM-S916B -r BTU -o ./downloads"

# Ejemplo 3: Descargar firmware con IMEI específico
show_example "3" \
    "Descargar firmware con IMEI personalizado" \
    "python3 samsung_firmware_downloader.py -m SM-S916B -r OXM -i 359999001234567"

# Ejemplo 4: Verificar firmware para Galaxy S23 Ultra
show_example "4" \
    "Verificar firmware para Galaxy S23 Ultra (Alemania - DBT)" \
    "python3 samsung_firmware_downloader.py -m SM-S918B -r DBT --check-only"

# Ejemplo 5: Descargar versión específica
show_example "5" \
    "Descargar versión específica de firmware" \
    "python3 samsung_firmware_downloader.py -m SM-S916B -r OXM -v S916BXXS8EYK5"

# Ejemplo 6: Descargar firmware para Galaxy S24+
show_example "6" \
    "Descargar firmware para Galaxy S24+ (Multi-región)" \
    "python3 samsung_firmware_downloader.py -m SM-S926B -r OXM -o ./firmwares"

echo "===================================================================="
echo "Para ejecutar cualquiera de estos ejemplos, copia el comando"
echo "y ejecútalo en tu terminal."
echo ""
echo "Nota: Asegúrate de tener instaladas las dependencias:"
echo "  pip install -r requirements.txt"
echo "===================================================================="
echo ""

# Preguntar si desea ejecutar una prueba
read -p "¿Desea ejecutar una prueba de verificación (solo check)? [s/N]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[SsYy]$ ]]
then
    echo ""
    echo -e "${GREEN}Ejecutando prueba de verificación...${NC}"
    echo "Modelo: SM-S916B (Galaxy S23+)"
    echo "Región: OXM (Open Europe)"
    echo ""
    python3 samsung_firmware_downloader.py -m SM-S916B -r OXM --check-only
else
    echo "No se ejecutará la prueba."
fi

echo ""
echo "Para más información, consulta README_FIRMWARE_DOWNLOADER.md"
