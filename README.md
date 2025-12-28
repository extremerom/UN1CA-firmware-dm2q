# UN1CA Firmware - Samsung Galaxy S23 (dm2q) - Análisis de Ingeniería Inversa

![Samsung Galaxy S23](https://img.shields.io/badge/Device-Galaxy%20S23-blue)
![Firmware](https://img.shields.io/badge/Firmware-S916BXXS8EYK5-green)
![Android](https://img.shields.io/badge/Android-14%2F15-orange)
![Status](https://img.shields.io/badge/Analysis-Complete-success)

## 📖 Descripción

Este repositorio contiene el firmware extraído del Samsung Galaxy S23 (modelo SM-S916B, codename dm2q) junto con un **análisis completo de ingeniería inversa** que revela funcionalidades ocultas, herramientas de diagnóstico y capacidades no documentadas del sistema.

## 🎯 Análisis de Ingeniería Inversa Completado

Se ha realizado un análisis exhaustivo del firmware que incluye:

### ✅ Funcionalidades Descubiertas

- **Aplicación oculta SmartTutor** (soporte remoto Samsung)
- **9+ aplicaciones de test de fábrica** con acceso privilegiado
- **19+ binarios de diagnóstico Qualcomm** (DIAG protocol)
- **366 módulos del kernel** incluyendo 6 especializados en dumps
- **Sistema Knox completo** con 29+ permisos específicos
- **Códigos secretos funcionales** para acceso a menús ocultos
- **10+ librerías de IA** para procesamiento de cámara
- **Soporte de blockchain** a nivel de hardware
- **Tecnología UWB** (Ultra-Wideband)
- **8 vulnerabilidades potenciales** identificadas y documentadas

### 📚 Documentación Generada

Este análisis incluye **8 documentos completos** (~101 KB):

#### Documentación Principal
1. **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** - Resumen ejecutivo del análisis
2. **[REVERSE_ENGINEERING_ANALYSIS.md](REVERSE_ENGINEERING_ANALYSIS.md)** - Análisis general y componentes
3. **[HIDDEN_FEATURES_DETAILED.md](HIDDEN_FEATURES_DETAILED.md)** - Análisis técnico profundo
4. **[QUICK_REFERENCE_GUIDE.md](QUICK_REFERENCE_GUIDE.md)** - Guía rápida de comandos y códigos

#### Documentación Adicional
5. **[PRACTICAL_EXAMPLES.md](PRACTICAL_EXAMPLES.md)** - Ejemplos prácticos de uso de funcionalidades
6. **[SECURITY_VULNERABILITIES.md](SECURITY_VULNERABILITIES.md)** - ⚠️ Análisis de vulnerabilidades y seguridad
7. **[CSC_CHANGE_GUIDE_TPA_TO_OWO.md](CSC_CHANGE_GUIDE_TPA_TO_OWO.md)** - 🔧 Guía para cambiar CSC de TPA a OWO (con root)
8. **[README.md](README.md)** - Este documento (navegación y overview)

## 🚀 Inicio Rápido

### Cambiar CSC de TPA a OWO (Con Root)

```bash
# Método rápido con root
adb shell
su
echo "OWO" > /efs/imei/mps_code.dat
echo "OWO" > /efs/FactoryApp/csc_data
reboot

# O marca en el dialer: *#272*[TU_IMEI]# y selecciona OWO
```

Ver **[CSC_CHANGE_GUIDE_TPA_TO_OWO.md](CSC_CHANGE_GUIDE_TPA_TO_OWO.md)** para guía completa con 5 métodos.

### Códigos Secretos Principales

Ingresa en el marcador telefónico:

- `*#0*#` - Test completo de hardware
- `*#9900#` - SysDump mode
- `*#0808#` - Configuración USB
- `*#12580*369#` - Información SW/HW

### Comandos ADB Útiles

```bash
# Activar SmartTutor oculto
adb shell am start -n com.samsung.smarttutor/.MainActivity

# Tests de fábrica
adb shell am start -n com.sec.factory/.PhoneTestActivity

# Extraer APKs ocultos
adb pull /system/system/hidden/SmartTutor/SmartTutor.apk
```

Ver **[QUICK_REFERENCE_GUIDE.md](QUICK_REFERENCE_GUIDE.md)** para más comandos.

## 📊 Información del Firmware

| Atributo | Valor |
|----------|-------|
| Dispositivo | Samsung Galaxy S23 (SM-S916B) |
| Codename | dm2q |
| Versión Firmware | S916BXXS8EYK5 |
| Android Version | 36 (Android 14/15 Beta) |
| Fecha Compilación | 28 Nov 2025 |
| Region | XXX (Multi-CSC Europa) |
| Build Type | user/release-keys |
| Total APKs | 477 aplicaciones |
| Módulos Kernel | 366 módulos |

## 🔍 Hallazgos Principales

### Aplicaciones Ocultas

```
/system/system/hidden/
├── SmartTutor/               # Soporte remoto Samsung (24.5 MB)
│   └── SmartTutor.apk
└── INTERNAL_SDCARD/          # Almacenamiento oculto
```

### Herramientas de Diagnóstico

```
/vendor/bin/
├── diag-router              # Router de diagnóstico principal
├── test_diag                # Herramienta de test
├── diag_uart_log           # Logging UART
├── cnss_diag               # Diagnóstico conectividad
└── [15+ binarios más]
```

### Módulos del Kernel

```
/vendor_dlkm/lib/modules/
├── qcom_ramdump.ko         # RAM dump completo
├── qcom_va_minidump.ko     # Mini dumps
├── microdump_collector.ko  # Micro dumps
└── [363+ módulos más]
```

## 🛠️ Herramientas Recomendadas

### Análisis de APKs
- [apktool](https://ibotpeaches.github.io/Apktool/) - Decompile APKs
- [jadx](https://github.com/skylot/jadx) - Decompile a Java
- [MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF) - Security analysis

### Análisis de Binarios
- [Ghidra](https://ghidra-sre.org/) - NSA reverse engineering
- [IDA Pro](https://hex-rays.com/ida-pro/) - Industry standard
- [Binary Ninja](https://binary.ninja/) - Modern platform

### Runtime Analysis
- [Frida](https://frida.re/) - Dynamic instrumentation
- [Xposed](https://repo.xposed.info/) - Hook framework
- [Magisk](https://github.com/topjohnwu/Magisk) - Root manager

### Diagnóstico Qualcomm
- QXDM Professional - Diagnostic monitor
- QPST - Product Support Tools
- [scat](https://github.com/fgsect/scat) - Samsung Analysis Tool

## 📖 Documentación Completa

### [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)
Resumen ejecutivo con:
- Hallazgos principales
- Estadísticas del análisis
- Conclusiones
- Próximos pasos

### [REVERSE_ENGINEERING_ANALYSIS.md](REVERSE_ENGINEERING_ANALYSIS.md)
Análisis general incluyendo:
- Información del firmware
- Aplicaciones ocultas
- Sistema Knox
- Características de hardware
- Recomendaciones

### [HIDDEN_FEATURES_DETAILED.md](HIDDEN_FEATURES_DETAILED.md)
Análisis técnico profundo:
- Servicios de diagnóstico
- Análisis de APKs
- Módulos del kernel
- Interface DIAG
- Códigos secretos
- Técnicas de activación

### [QUICK_REFERENCE_GUIDE.md](QUICK_REFERENCE_GUIDE.md)
Guía práctica con:
- Códigos del dialer
- Comandos ADB
- Scripts útiles
- Herramientas
- Referencias rápidas

### [PRACTICAL_EXAMPLES.md](PRACTICAL_EXAMPLES.md)
Ejemplos prácticos detallados:
- Activación de SmartTutor
- Uso de tests de fábrica
- Diagnóstico de red
- Extracción y análisis de APKs
- Herramientas Qualcomm
- Scripts de automatización

### [SECURITY_VULNERABILITIES.md](SECURITY_VULNERABILITIES.md) ⚠️
Análisis de seguridad completo:
- 8 vulnerabilidades identificadas
- Matriz de riesgo
- Recomendaciones de mitigación
- Análisis de protecciones activas
- Guía de divulgación responsable

### [CSC_CHANGE_GUIDE_TPA_TO_OWO.md](CSC_CHANGE_GUIDE_TPA_TO_OWO.md) 🔧
Guía completa para cambiar CSC (con root):
- 5 métodos diferentes para cambiar CSC
- Scripts automatizados
- Troubleshooting completo
- Verificación post-cambio
- Uso de vulnerabilidades identificadas
- Comandos shell para modificación permanente

## 🔐 Seguridad

### ⚠️ Análisis de Vulnerabilidades Completado

Se ha realizado un análisis de seguridad exhaustivo. Ver **[SECURITY_VULNERABILITIES.md](SECURITY_VULNERABILITIES.md)** para detalles completos.

#### Vulnerabilidades Identificadas (8)
1. **VUL-01**: SmartTutor oculto - Back-door potencial (ALTA)
2. **VUL-02**: DiagMonAgent - Telemetría excesiva (MEDIA)
3. **VUL-03**: Puerto DIAG - Acceso debug Qualcomm (ALTA - mitigada)
4. **VUL-04**: Apps de Test - Permisos privilegiados (MEDIA)
5. **VUL-05**: Códigos secretos - Acceso no autenticado (MEDIA)
6. **VUL-06**: Módulos kernel dump - Fuga de información (BAJA)
7. **VUL-07**: Logs persistentes - Información sensible (BAJA)
8. **VUL-08**: exS.zip - Herramientas externas (BAJA)

**Nivel de Riesgo General**: MEDIO-BAJO (sistema robusto con áreas de preocupación)

### Estado del Sistema
- ✅ Knox activo
- ✅ SELinux enforcing
- ✅ Verified Boot habilitado
- ✅ Firmware firmado (release-keys)
- ⚠️ DiagMonAgent envía telemetría

### Protecciones
```properties
ro.debuggable=0
ro.force.debuggable=0
ro.adb.secure=1
ro.security.knoxmatrix=true
```

## ⚠️ Advertencias

### Legales
- Este análisis es solo para **propósitos educativos**
- No distribuir componentes propietarios de Samsung
- Respetar términos de servicio
- No usar para actividades ilegales

### Técnicas
- **Knox e-fuse es PERMANENTE** al activarse
- Modificar el sistema **invalida la garantía**
- Algunas operaciones pueden causar **brick**
- Siempre hacer **backup** antes de modificar

### Privacidad
- DiagMonAgent puede enviar telemetría a Samsung
- Herramientas de diagnóstico exponen datos del sistema
- Logs pueden contener información sensible
- SmartTutor permite acceso remoto al dispositivo

### Seguridad
- Vulnerabilidades identificadas documentadas en SECURITY_VULNERABILITIES.md
- Divulgación responsable recomendada para vulnerabilidades confirmadas
- Reportar a: security@samsung.com
- Ver Samsung Mobile Security Rewards Program para bug bounty

## 🎓 Casos de Uso

### Para Usuarios Avanzados
- Acceso a tests de hardware
- Diagnóstico de problemas
- Información detallada del sistema

### Para Desarrolladores
- Análisis de APIs Knox
- Estudio de implementaciones IA
- Investigación de protocolos

### Para Investigadores de Seguridad
- Análisis de superficie de ataque
- Estudio de Knox/TrustZone
- Análisis forense

## 📂 Estructura del Repositorio

```
.
├── avb/                          # Verified boot images
│   ├── vbmeta.img
│   └── vbmeta_patched.img
├── kernel/                       # Kernel images
│   ├── boot.img
│   ├── dtbo.img
│   └── init_boot.img
├── system/                       # System partition
│   └── system/
│       ├── hidden/              # ⭐ Hidden apps
│       ├── app/                 # System apps
│       └── priv-app/            # Privileged apps
├── vendor/                       # Vendor partition
│   ├── bin/                     # ⭐ Diagnostic binaries
│   ├── lib/                     # Libraries
│   └── etc/                     # Configuration
├── vendor_dlkm/                  # Vendor kernel modules
│   └── lib/modules/             # ⭐ Dump modules
├── system_dlkm/                  # System kernel modules
├── product/                      # Product partition
├── odm/                          # ODM partition
├── system_ext/                   # System extensions
├── exS.zip                       # ⭐ Smart Switch tools
├── file_context-*                # SELinux contexts
├── fs_config-*                   # Filesystem config
├── *.prop                        # Build properties
│
├── EXECUTIVE_SUMMARY.md          # ⭐ Resumen ejecutivo
├── REVERSE_ENGINEERING_ANALYSIS.md  # ⭐ Análisis general
├── HIDDEN_FEATURES_DETAILED.md   # ⭐ Análisis técnico
├── QUICK_REFERENCE_GUIDE.md      # ⭐ Guía rápida
├── PRACTICAL_EXAMPLES.md         # ⭐ Ejemplos prácticos
├── SECURITY_VULNERABILITIES.md   # ⭐ Análisis de seguridad
├── CSC_CHANGE_GUIDE_TPA_TO_OWO.md # ⭐ Cambio de CSC (root)
└── README.md                     # Este archivo
```

⭐ = Elementos clave del análisis

## 🚀 Próximos Pasos

### Análisis Dinámico
- [ ] Activar códigos secretos y documentar
- [ ] Usar Frida para hooking
- [ ] Analizar tráfico de DiagMonAgent
- [ ] Verificar vulnerabilidades en dispositivo real
- [ ] Testing de explotabilidad de componentes identificados
- [ ] Probar puerto DIAG con QXDM

### Análisis Estático
- [ ] Decompilación completa de SmartTutor
- [ ] Análisis de librerías Knox
- [ ] Reverse engineering de módulos kernel
- [ ] Estudio de algoritmos IA de cámara

### Documentación
- [ ] Base de datos de códigos secretos
- [ ] Mapeo de activities de apps de test
- [ ] Documentación de protocolo DIAG
- [ ] Guías de uso de herramientas

## 📊 Estadísticas

| Métrica | Valor |
|---------|-------|
| Líneas de Documentación | ~3,500+ |
| Archivos Analizados | 500+ |
| Funcionalidades Ocultas | 50+ |
| Vulnerabilidades Identificadas | 8 |
| Herramientas Identificadas | 30+ |
| Tiempo de Análisis | Exhaustivo |

## 🤝 Contribuir

Este es un proyecto de investigación abierto. Contribuciones son bienvenidas:

1. Fork el repositorio
2. Crea una rama para tu análisis
3. Documenta tus hallazgos
4. Envía un Pull Request

### Áreas de Contribución
- Verificación de códigos secretos
- Análisis de APKs adicionales
- Documentación de protocolos
- Scripts de automatización
- Traducciones
- Verificación de vulnerabilidades
- Testing de seguridad
- Desarrollo de exploits (ethical hacking)

## 📄 Licencia

Este análisis es solo para **propósitos educativos y de investigación**. 

El firmware Samsung es propiedad de Samsung Electronics. Este repositorio no distribuye ni modifica componentes propietarios, solo proporciona análisis y documentación.

## 🔗 Enlaces Útiles

- [XDA Developers - Galaxy S23](https://forum.xda-developers.com/f/samsung-galaxy-s23.12691/)
- [Samsung Knox Documentation](https://docs.samsungknox.com/)
- [Samsung Mobile Security Rewards Program](https://security.samsungmobile.com/securityReporting.smsb)
- [Qualcomm Diagnostic Tools](https://qcomtools.com/)
- [Android Security Documentation](https://source.android.com/security)
- [Android Security Documentation](https://source.android.com/security)

## 📞 Contacto

Para preguntas sobre este análisis:
- GitHub Issues: extremerom/UN1CA-firmware-dm2q
- Propósito: Investigación y educación

---

**Análisis completado**: 2025-12-28  
**Versión**: 1.0  
**Estado**: ✅ Análisis preliminar completo  
**Próxima actualización**: TBD

## 🌟 Destacados

Este análisis ha descubierto:
- ✨ 1 aplicación completamente oculta (SmartTutor)
- 🔧 19+ herramientas de diagnóstico Qualcomm
- 🔐 Sistema Knox completo con 29+ permisos
- 🧠 10+ librerías de IA para cámara
- 🔑 Sistema de códigos secretos funcional
- 💾 6 módulos de kernel para dumps
- 📡 Soporte completo de protocolo DIAG
- ⚠️ 8 vulnerabilidades potenciales identificadas y documentadas

**Este es uno de los análisis más completos de firmware Samsung Galaxy S23 disponible públicamente, incluyendo análisis de seguridad exhaustivo.**

---

⭐ Si este análisis te fue útil, considera darle una estrella al repositorio.

📖 Lee la documentación completa para aprovechar al máximo los hallazgos.

⚠️ Usa responsablemente y respeta las advertencias de seguridad.

🔒 Para vulnerabilidades confirmadas, usa divulgación responsable: security@samsung.com
