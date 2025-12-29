# 📚 Índice de Documentación - Análisis de Menús de Ingeniería

## 🎯 Navegación Rápida

Este repositorio contiene el análisis completo del firmware UN1CA para Samsung Galaxy S23 (SM-S916B / dm2q), con documentación exhaustiva sobre menús de ingeniería y códigos secretos.

---

## 📖 Documentos Disponibles

### 🚀 [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
**Guía de Inicio Rápido** - Comienza aquí si necesitas información inmediata
- ⏱️ Lectura: 3 minutos
- 📄 Tamaño: 3.4 KB
- 🎯 Contenido:
  - Tabla de códigos más usados
  - Indicadores de nivel de peligro (🟢🟡🔴)
  - Tips rápidos para diagnóstico
  - Reglas de oro de seguridad
  - Lista resumida de apps de ingeniería

**Ideal para**: Consulta rápida de códigos

---

### 📱 [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md)
**Guía Completa de Menús de Ingeniería** - Documentación detallada
- ⏱️ Lectura: 30-45 minutos
- 📄 Tamaño: 18 KB
- 🎯 Contenido:
  - **12 aplicaciones de ingeniería** identificadas y documentadas
  - **20+ códigos secretos** con instrucciones paso a paso
  - Información detallada del dispositivo
  - Permisos especiales de ModemServiceMode
  - Casos de uso comunes
  - Comandos ADB útiles
  - Procedimientos de troubleshooting
  - Advertencias de seguridad extensas
  - Disclaimer legal completo

**Ideal para**: Consulta detallada y aprendizaje

---

### 🔬 [DEEP_TECHNICAL_ANALYSIS.md](DEEP_TECHNICAL_ANALYSIS.md) **NUEVO**
**Análisis Técnico Profundo** - Decompilación y análisis de código fuente
- ⏱️ Lectura: 45-60 minutos
- 📄 Tamaño: 26 KB
- 🎯 Contenido:
  - **Decompilación de APKs** con apktool y jadx
  - **Análisis de código fuente Java** (1,402 clases extraídas)
  - Estructura interna de ServiceModeApp
  - SecKeyStringBroadcastReceiver analizado
  - **Comandos AT identificados**
  - **Scripts de activación con root**
  - Mecanismos de seguridad encontrados
  - Arquitectura del sistema RIL
  - Matriz de permisos detallada
  - Casos de uso avanzados

**Ideal para**: Desarrolladores e investigadores técnicos

---

### 📊 [DIAGRAMS_AND_WORKFLOWS.md](DIAGRAMS_AND_WORKFLOWS.md) **NUEVO**
**Diagramas y Flujos de Trabajo** - Visualización del sistema
- ⏱️ Lectura: 30-40 minutos
- 📄 Tamaño: 68 KB
- 🎯 Contenido:
  - **7 diagramas técnicos detallados**:
    1. Flujo de activación de códigos secretos
    2. Arquitectura del sistema RIL (Radio Interface Layer)
    3. Proceso de comunicación con modem
    4. Flujo de permisos y seguridad
    5. Diagrama de estados de ServiceModeApp
    6. Flujo de logging y diagnóstico
    7. Interacción entre componentes
  - Diagramas ASCII art profesionales
  - Secuencias de comandos AT
  - Pipeline de logging completo

**Ideal para**: Comprender el flujo del sistema visualmente

---

### 🔍 [EXTENDED_AT_COMMANDS_ANALYSIS.md](EXTENDED_AT_COMMANDS_ANALYSIS.md) **NUEVO**
**Análisis Extendido de Comandos AT** - Decompilación completa y comandos AT
- ⏱️ Lectura: 40-50 minutos
- 📄 Tamaño: 19 KB
- 🎯 Contenido:
  - **Análisis de 6+ APKs adicionales**:
    - SecFactoryPhoneTest, TelephonyUI, PhoneErrService
    - EpdgService, PhoneNumberService
  - **50+ Frameworks identificados** (Qualcomm IMS, Data, Satellite)
  - **30+ Binarios del sistema** analizados
  - **30+ APEX modules** catalogados
  - **7 comandos AT únicos** extraídos del firmware:
    - AT+ANTENA=, AT+CFUN=0, AT+OEMHWID=
    - AT+RSSI=3, AT+STACKMODE=10, AT+ENGMODES=
  - **30+ comandos AT estándar** documentados
  - **Métodos de acceso**: ADB, código nativo, Java/Kotlin
  - **Ejemplos de código** para enviar comandos AT
  - Arquitectura RIL completa identificada
  - Análisis de libsec-ril.so
  - Recomendaciones para análisis dinámico

**Ideal para**: Investigadores avanzados y desarrollo con modem

---

### 🔧 [AT_COMMANDS_EXECUTION_GUIDE.md](AT_COMMANDS_EXECUTION_GUIDE.md) **NUEVO**
**Guía Práctica de Ejecución de Comandos AT** - Cómo ejecutar desde celular con root
- ⏱️ Lectura: 35-45 minutos
- 📄 Tamaño: 18 KB
- 🎯 Contenido:
  - **130+ comandos AT únicos** extraídos del modem firmware
  - **6 métodos de ejecución** documentados:
    1. Via ADB desde PC (recomendado)
    2. Script automatizado ADB
    3. Directamente en dispositivo (Termux)
    4. Script Bash en dispositivo
    5. Aplicación Android con root (código Java completo)
    6. Código nativo C/C++ (con ejemplo compilable)
  - **Comandos propietarios Samsung** categorizados:
    - Prueba y diagnóstico (AT+TESTMODE, AT+GPSSTEST, etc.)
    - Configuración de red (AT+BANSELCT, AT+NETMODEC, etc.)
    - Seguridad y bloqueo (AT+LVOFLOCK, AT+SIMLOCKU, etc.)
    - IMEI y certificación (AT+IMEISIGN, AT+IMEICERT, etc.)
    - Calibración RF (AT+READRSSI, AT+MAXPOWER, etc.)
  - **Comandos estándar 3GPP**: AT+CFUN, AT+COPS, AT+CGATT, etc.
  - **Ejemplos prácticos** con salidas esperadas
  - **Precauciones críticas** y comandos peligrosos
  - **Backup de EFS/NVRAM** antes de experimentar
  - **Troubleshooting** completo
  - **Monitoreo de comandos AT** del sistema

**Ideal para**: Usuarios con root que quieren ejecutar comandos AT

---

### 🔧 [TROUBLESHOOTING_RIL_SOCKET.md](TROUBLESHOOTING_RIL_SOCKET.md) **NUEVO**
**Troubleshooting: Socket RIL No Encontrado** - Soluciones alternativas
- ⏱️ Lectura: 25-35 minutos
- 📄 Tamaño: 11 KB
- 🎯 Contenido:
  - **Diagnóstico del problema**: Por qué /dev/socket/rild no existe
  - **Identificar socket correcto** en tu dispositivo
  - **5 métodos alternativos** para ejecutar comandos AT:
    1. Via QMI (Qualcomm MSM Interface)
    2. Via Service Call (Telephony Manager)
    3. Via ATFWD-daemon
    4. Via ModemServiceMode app
    5. Via Content Provider
  - **Herramientas QMI**: Instalación de libqmi y qmicli
  - **Knox bloqueando acceso**: Verificación y soluciones
  - **Script de búsqueda automática** de sockets RIL
  - **Solución específica para dispositivos Qualcomm**
  - **Crear socket RIL manualmente** (avanzado, peligroso)
  - **Métodos de diagnóstico alternativos**: USSD/MMI codes
  - **Bypass de Knox** para acceso a sockets
  - **Plan B y C** si métodos principales fallan

**Ideal para**: Usuarios que no encuentran /dev/socket/rild

---

### 🔐 [KNOX_ANALYSIS.md](KNOX_ANALYSIS.md) **NUEVO**
**Análisis de Samsung Knox** - Ingeniería inversa y bypass
- ⏱️ Lectura: 40-50 minutos
- 📄 Tamaño: 13 KB
- 🎯 Contenido:
  - **Arquitectura completa de Knox**:
    - TrustZone (ARM Trusted Execution Environment)
    - TIMA (Integrity Measurement Architecture)
    - RKP (Real-time Kernel Protection)
    - Secure Boot, DM-Verity, Knox Container
  - **Apps Knox identificadas** en firmware
  - **Análisis de componentes**:
    - Knox Bootloader y verificación
    - Knox TrustZone (Normal vs Secure World)
    - Knox TIMA (PKM, Defex, LKMAUTH)
    - Knox RKP (protección de kernel)
    - Knox DM-Verity (verificación de particiones)
  - **Ingeniería inversa de apps Knox**:
    - Decompilación con jadx
    - Análisis de librerías nativas
    - Interceptación con Frida
    - Scripts de hooking incluidos
  - **5 métodos de bypass de Knox** (educativo):
    1. Desactivar Knox Counter (pre-root)
    2. Ocultar root de Knox (Magisk)
    3. Desactivar servicios Knox
    4. Parchear Knox en ROM custom
    5. SELinux Permissive
  - **Análisis de apps específicas**:
    - Knox Analytics Uploader
    - Knox Attestation Agent
    - Knox Container Agent
  - **Protecciones anti-RE**: Ofuscación, native code, anti-debugging
  - **Herramientas de análisis**: jadx, Ghidra, Frida, strace
  - **Comparación**: Knox vs Root
  - **Script de análisis de Knox** incluido

**Ideal para**: Investigadores de seguridad y bypass de Knox

---

### 📊 [README_ANALYSIS.md](README_ANALYSIS.md)
**Documentación del Análisis** - Metodología y contexto
- ⏱️ Lectura: 15-20 minutos
- 📄 Tamaño: 8.1 KB
- 🎯 Contenido:
  - Información del dispositivo analizado
  - Metodología de análisis utilizada
  - Estructura del firmware
  - Tabla de permisos especiales
  - Casos de uso educativos
  - Recursos adicionales
  - Disclaimer legal y advertencias
  - Información sobre contribuciones

**Ideal para**: Entender el contexto y metodología

---

### ✅ [ANALYSIS_SUMMARY.md](ANALYSIS_SUMMARY.md)
**Resumen Ejecutivo** - Resultados y estadísticas
- ⏱️ Lectura: 10 minutos
- 📄 Tamaño: 8.3 KB
- 🎯 Contenido:
  - Resumen de resultados del análisis
  - Estadísticas del proyecto
  - Lista de objetivos cumplidos
  - Características de seguridad
  - Valor educativo
  - Consideraciones legales
  - Próximos pasos recomendados

**Ideal para**: Vista general del proyecto

---

## 🎯 Rutas de Lectura Recomendadas

### 👤 Para Usuarios Novatos:
1. **Comenzar**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. **Continuar**: Secciones básicas de [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md)
3. **Leer**: Advertencias en todos los documentos

### 🔧 Para Técnicos:
1. **Comenzar**: [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md)
2. **Referencia**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
3. **Contexto**: [README_ANALYSIS.md](README_ANALYSIS.md)

### 👨‍💻 Para Desarrolladores:
1. **Comenzar**: [README_ANALYSIS.md](README_ANALYSIS.md)
2. **Profundizar**: [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md)
3. **Referencia**: [ANALYSIS_SUMMARY.md](ANALYSIS_SUMMARY.md)

### 📊 Para Gestores/Managers:
1. **Comenzar**: [ANALYSIS_SUMMARY.md](ANALYSIS_SUMMARY.md)
2. **Vista general**: [README_ANALYSIS.md](README_ANALYSIS.md)
3. **Detalles opcionales**: [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md)

---

## 🔍 Búsqueda Rápida

### Buscas información sobre...

#### 📱 Códigos Específicos:
- **Todos los códigos**: [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md#-códigos-secretos-de-samsung)
- **Tabla rápida**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md#-códigos-más-usados)

#### 🛠️ Aplicaciones de Ingeniería:
- **Lista completa**: [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md#-aplicaciones-de-ingeniería-encontradas)
- **Resumen**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md#-apps-de-ingeniería-en-el-firmware)
- **Estadísticas**: [ANALYSIS_SUMMARY.md](ANALYSIS_SUMMARY.md#-resultados-del-análisis)

#### ⚠️ Seguridad y Advertencias:
- **Advertencias generales**: Sección en [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md#️-advertencias-importantes)
- **Por código**: Cada código en [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md)
- **Reglas de oro**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md#️-reglas-de-oro)

#### 🔧 Diagnóstico:
- **Códigos de diagnóstico**: [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md#códigos-de-servicio-y-diagnóstico)
- **ADB Commands**: [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md#-acceso-mediante-adb-android-debug-bridge)
- **Troubleshooting**: [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md#-si-algo-sale-mal)

#### 📊 Información Técnica:
- **Dispositivo**: [README_ANALYSIS.md](README_ANALYSIS.md#-dispositivo-analizado)
- **Firmware**: [README_ANALYSIS.md](README_ANALYSIS.md#-estructura-del-firmware)
- **Permisos**: [README_ANALYSIS.md](README_ANALYSIS.md#-aplicaciones-con-permisos-especiales)

---

## 📊 Resumen del Contenido

### Aplicaciones Identificadas: **12**

| Tipo | Cantidad | Ubicación |
|------|----------|-----------|
| Privilegiadas | 8 | `/system/priv-app/` |
| Sistema | 4 | `/system/app/` |

**Destacada**: ModemServiceMode (2.7MB) con 8 permisos privilegiados

### Códigos Documentados: **20+**

| Categoría | Cantidad | Peligro |
|-----------|----------|---------|
| Información | 7 | 🟢 Seguro |
| Diagnóstico | 8 | 🟢 Seguro |
| Configuración | 2 | 🔴 Peligro |
| Reset | 1 | 🔴🔴🔴 Extremo |
| Otros | 2+ | 🟡 Cuidado |

---

## 📱 Información del Dispositivo

```
Modelo:        Samsung Galaxy S23
Número:        SM-S916B
Código:        dm2q / dm2qxxx
Android:       16 (SDK 36)
Build:         BP2A.250605.031.A3
Firmware:      S916BXXS8EYK5
Base:          UN1CA
Fecha:         Noviembre 2024
Procesador:    Qualcomm Snapdragon (kalama)
```

---

## ⚠️ ADVERTENCIA IMPORTANTE

**LEE ESTO ANTES DE USAR CUALQUIER CÓDIGO:**

- ❌ Los menús de ingeniería pueden modificar configuraciones críticas
- ❌ El uso incorrecto puede causar mal funcionamiento del dispositivo
- ❌ Algunos cambios pueden ser permanentes
- ❌ Puede invalidar la garantía
- ✅ Siempre haz backup antes de experimentar
- ✅ Si no entiendes un menú, NO lo uses
- ✅ Lee todas las advertencias en cada documento

**USA BAJO TU PROPIO RIESGO**

---

## 🎯 Casos de Uso

### ✅ Usos Apropiados:
- ✔️ Verificar hardware al comprar usado
- ✔️ Diagnosticar problemas de conectividad
- ✔️ Ver información del sistema
- ✔️ Probar funcionalidad de componentes
- ✔️ Aprendizaje y educación técnica

### ❌ Usos NO Recomendados:
- ✖️ Modificar bandas de red sin conocimiento
- ✖️ Actualizar firmware desde menús de servicio
- ✖️ Cambiar configuraciones sin entenderlas
- ✖️ Usar códigos de reset sin backup
- ✖️ Experimentar sin leer advertencias

---

## 📞 Soporte y Ayuda

### Si tienes problemas:
1. Lee la sección de troubleshooting en [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md)
2. Revisa las advertencias específicas del código usado
3. Reinicia el dispositivo
4. Restablece configuración de red si es necesario
5. Como último recurso, restablecimiento de fábrica (con backup)

### Para preguntas o reportes:
- Abre un issue en el repositorio de GitHub
- Incluye qué código/menú usaste
- Describe el problema detalladamente
- Menciona si hiciste backup

---

## 🔄 Actualizaciones

**Última actualización**: Diciembre 2024

### Historial de Versiones:
- **v1.0** (Diciembre 2024)
  - Análisis inicial completado
  - 4 documentos principales creados
  - 12 aplicaciones documentadas
  - 20+ códigos documentados

### Futuras actualizaciones:
- Análisis de nuevas versiones de firmware
- Códigos adicionales descubiertos
- Correcciones y mejoras
- Feedback de la comunidad

---

## 📚 Recursos Adicionales

### Externos:
- [Documentación Samsung Developer](https://developer.samsung.com/)
- [Android Developer Documentation](https://developer.android.com/)
- [XDA Developers Forums](https://forum.xda-developers.com/)
- [Reddit r/GalaxyS23](https://www.reddit.com/r/GalaxyS23/)

### Herramientas Útiles:
- **ADB (Android Debug Bridge)**: Para comandos avanzados
- **Samsung Members**: Diagnóstico oficial
- **Device Info HW**: Información de hardware
- **CPU-Z**: Información del sistema

---

## ⚖️ Legal

### Disclaimer:
Esta documentación se proporciona **SOLO CON FINES EDUCATIVOS E INFORMATIVOS**.

**El autor NO se hace responsable de**:
- Daños al dispositivo
- Pérdida de datos
- Pérdida de garantía
- Problemas de funcionamiento
- Cualquier otro problema derivado del uso

**Todo el uso es bajo tu propio riesgo.**

### Propiedad Intelectual:
- Samsung y Galaxy S23 son marcas registradas de Samsung Electronics
- Android es marca registrada de Google LLC
- Este análisis es independiente y no oficial

---

## 🤝 Contribuciones

¿Encontraste algo nuevo? ¿Tienes correcciones?
- Abre un issue en GitHub
- Propón cambios mediante pull request
- Comparte responsablemente

---

## 📧 Contacto

Para preguntas o correcciones, abre un issue en el repositorio de GitHub.

---

## 🌟 Agradecimientos

- Samsung por proporcionar firmware actualizado
- Comunidad XDA por documentación de códigos
- Comunidad Android por herramientas de análisis
- Todos los que usen esta documentación responsablemente

---

**Creado con 🔍 mediante análisis del firmware UN1CA-firmware-dm2q**

---

*Última actualización: Diciembre 2024*
