# Guía de Menús de Ingeniería - Samsung Galaxy S23 (SM-S916B)

## 📱 Información del Dispositivo
- **Modelo**: Samsung Galaxy S23 (SM-S916B)
- **Nombre de código**: dm2q / dm2qxxx
- **Versión Android**: 16 (SDK 36)
- **Build**: BP2A.250605.031.A3 / S916BXXS8EYK5
- **Firmware**: UN1CA

## ⚠️ ADVERTENCIAS IMPORTANTES

**ANTES DE USAR ESTOS MENÚS, LEE ESTO:**
- Los menús de ingeniería están diseñados para uso técnico y pruebas de fábrica
- Modificar configuraciones incorrectas puede causar mal funcionamiento del dispositivo
- Algunos cambios pueden ser permanentes y requerir restauración de fábrica
- NO modifiques valores si no entiendes su función
- Algunos menús pueden mostrar información sensible (IMEI, números de serie, etc.)
- El uso incorrecto puede invalidar la garantía
- Realiza una copia de seguridad antes de experimentar

## 📋 Aplicaciones de Ingeniería Encontradas

### 1. ModemServiceMode (Modo de Servicio del Módem)
**Ubicación**: `/system/priv-app/ModemServiceMode/ModemServiceMode.apk`
**Tamaño**: 2.7MB
**Tipo**: Aplicación privilegiada del sistema
**Paquete**: `com.sec.android.RilServiceModeApp`

**Permisos especiales**:
- `ACCESS_CHECKIN_PROPERTIES` - Acceso a propiedades del sistema
- `CHANGE_CONFIGURATION` - Modificar configuración del dispositivo
- `MODIFY_PHONE_STATE` - Modificar estado del teléfono
- `MOUNT_UNMOUNT_FILESYSTEMS` - Montar/desmontar sistemas de archivos
- `WRITE_APN_SETTINGS` - Escribir configuración APN
- `READ_PRIVILEGED_PHONE_STATE` - Leer estado privilegiado del teléfono
- `ACCESS_FINE_LOCATION` - Acceso a ubicación precisa
- `SET_DEBUG_APP` - Establecer aplicación de depuración

### 2. SecFactoryPhoneTest (Prueba de Teléfono de Fábrica)
**Ubicación**: `/system/priv-app/SecFactoryPhoneTest/SecFactoryPhoneTest.apk`
**Tipo**: Aplicación privilegiada del sistema

### 3. DiagMonAgent95 (Agente de Monitoreo de Diagnóstico)
**Ubicación**: `/system/priv-app/DiagMonAgent95/DiagMonAgent95.apk`
**Tipo**: Aplicación privilegiada del sistema

### 4. DeviceDiagnostics (Diagnóstico de Dispositivo)
**Ubicación**: `/system/priv-app/DeviceDiagnostics/DeviceDiagnostics.apk`
**Tipo**: Aplicación privilegiada del sistema

### 5. NetworkDiagnostic (Diagnóstico de Red)
**Ubicación**: `/system/priv-app/NetworkDiagnostic/NetworkDiagnostic.apk`
**Tipo**: Aplicación privilegiada del sistema

### 6. SEMFactoryApp (Aplicación de Fábrica SEM)
**Ubicación**: `/system/priv-app/SEMFactoryApp/SEMFactoryApp.apk`
**Tipo**: Aplicación privilegiada del sistema

### 7. SmartEpdgTestApp (Aplicación de Prueba Smart ePDG)
**Ubicación**: `/system/priv-app/SmartEpdgTestApp/SmartEpdgTestApp.apk`
**Tipo**: Aplicación privilegiada del sistema

### 8. FactoryTestProvider (Proveedor de Pruebas de Fábrica)
**Ubicación**: `/system/priv-app/FactoryTestProvider/FactoryTestProvider.apk`
**Tipo**: Aplicación privilegiada del sistema

### 9. FactoryCameraFB (Cámara de Fábrica)
**Ubicación**: `/system/app/FactoryCameraFB/FactoryCameraFB.apk`
**Tipo**: Aplicación del sistema

### 10. FactoryAirCommandManager (Gestor de Air Command de Fábrica)
**Ubicación**: `/system/app/FactoryAirCommandManager/FactoryAirCommandManager.apk`
**Tipo**: Aplicación del sistema

### 11. UwbTest (Prueba UWB)
**Ubicación**: `/system/app/UwbTest/UwbTest.apk`
**Tipo**: Aplicación del sistema

### 12. WlanTest (Prueba WLAN)
**Ubicación**: `/system/app/WlanTest/WlanTest.apk`
**Tipo**: Aplicación del sistema

## 🔢 Códigos Secretos de Samsung

### Códigos de Información del Sistema

#### `*#0*#` - Menú de Prueba de Hardware
**Funcionalidad**: Menú completo de pruebas de hardware
**Pruebas disponibles**:
- **Red** (Red): Prueba de colores rojo
- **Green** (Verde): Prueba de colores verde
- **Blue** (Azul): Prueba de colores azul
- **Receiver** (Auricular): Prueba de auricular
- **Vibration** (Vibración): Prueba de motor de vibración
- **Dimming**: Prueba de atenuación de pantalla
- **Mega Cam** (Cámara principal): Prueba de cámara trasera
- **Sensor**: Prueba de sensores
- **Touch** (Táctil): Prueba de pantalla táctil
- **Sleep** (Suspensión): Modo de suspensión
- **Speaker** (Altavoz): Prueba de altavoz
- **Sub Key** (Teclas secundarias): Prueba de botones
- **Front Cam** (Cámara frontal): Prueba de cámara frontal
- **LED**: Prueba de LED de notificación
- **Low Frequency**: Prueba de baja frecuencia
- **Black** (Negro): Prueba de pantalla negra
- **Grip Sensor**: Prueba de sensor de agarre
- **Barometer**: Prueba de barómetro
- **Magnetic Sensor**: Prueba de sensor magnético

**Cómo acceder**: 
1. Abre la aplicación Teléfono
2. Marca `*#0*#`
3. El menú se abrirá automáticamente

#### `*#*#4636#*#*` - Menú de Información y Pruebas
**Funcionalidad**: Menú de información del teléfono y pruebas
**Información disponible**:
- Información del teléfono (IMEI, número de teléfono, red actual, etc.)
- Información de la batería (nivel, salud, temperatura, voltaje)
- Historial de batería
- Estadísticas de uso
- Información de Wi-Fi (dirección MAC, estado de conexión)

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#*#4636#*#*`
3. Se abrirá el menú "Testing" o "Información del teléfono"

#### `*#06#` - Información IMEI
**Funcionalidad**: Muestra el número IMEI del dispositivo
**Información mostrada**:
- IMEI del dispositivo
- Número de serie
- Información de la tarjeta SIM

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#06#`
3. Se mostrará automáticamente

#### `*#1234#` - Versión de Firmware
**Funcionalidad**: Muestra información de la versión del software
**Información mostrada**:
- AP (Application Processor) versión
- CP (Communication Processor) versión
- CSC (Consumer Software Customization) versión
- Build date

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#1234#`
3. Se mostrará automáticamente

#### `*#12580*369#` - Información de Hardware y Software
**Funcionalidad**: Menú completo de información del dispositivo
**Información disponible**:
- SW Version (Versión de software)
- HW Version (Versión de hardware)
- RF CAL Date (Fecha de calibración RF)
- Información de cámara

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#12580*369#`
3. Se abrirá el menú de información

### Códigos de Servicio y Diagnóstico

#### `*#9900#` - SysDump / Modo de Registro del Sistema
**Funcionalidad**: Menú de volcado del sistema y registro
**Opciones disponibles**:
- SysDump: Crear volcado del sistema
- Delete dumpstate/logcat: Eliminar registros
- Copy to sdcard: Copiar registros a SD
- Run dumpstate/logcat: Ejecutar volcado de estado
- Debug level: Nivel de depuración
- Low battery dump: Volcado de batería baja

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#9900#`
3. Se abrirá el menú SysDump

**⚠️ Precaución**: No borres registros si estás solucionando problemas

#### `*#0228#` - Estado de la Batería
**Funcionalidad**: Información detallada de la batería
**Información mostrada**:
- Voltaje de la batería
- Temperatura de la batería
- Estado de carga
- Ciclos de carga

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#0228#`
3. Se mostrará la información de la batería

#### `*#0011#` - Estado del Servicio / Modo de Servicio GSM
**Funcionalidad**: Información de la red móvil y señal
**Información disponible**:
- Estado de la red
- Información de la célula
- Información de frecuencia
- Potencia de señal
- Información del canal

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#0011#`
3. Se abrirá el menú de estado del servicio

**Botones disponibles**:
- **Menu > Key Input**: Permite ingresar comandos AT
- **Menu > Back**: Volver

#### `*#0283#` - Loopback de Audio
**Funcionalidad**: Prueba de bucle de audio (micrófono → altavoz)
**Uso**: Para probar el micrófono y altavoz simultáneamente

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#0283#`
3. Habla por el micrófono y escucharás tu voz por el altavoz

#### `*#2663#` - Versión de Pantalla Táctil
**Funcionalidad**: Información de la pantalla táctil
**Información mostrada**:
- Versión del firmware del panel táctil
- Versión del controlador táctil

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#2663#`
3. Se mostrará la información

#### `*#2683662#` - Editor de Pantalla de Servicio
**Funcionalidad**: Menú de servicio avanzado
**Opciones disponibles**:
- TSP Firmware Update
- TSP Phone OFF
- TSP Phone ON

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#2683662#`
3. Se abrirá el menú del editor

**⚠️ Precaución**: NO actualices el firmware táctil a menos que sepas lo que haces

#### `*#7353#` - Menú de Prueba Rápida
**Funcionalidad**: Menú de prueba rápida de funciones
**Pruebas disponibles**:
- Melody test (Prueba de melodía)
- Vibration test (Prueba de vibración)
- Speaker test (Prueba de altavoz)
- Sub Key test (Prueba de teclas)
- Proximity sensor test (Prueba de sensor de proximidad)

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#7353#`
3. Selecciona la prueba deseada

### Códigos de Configuración

#### `*#197328640#` - Modo de Servicio Principal
**Funcionalidad**: Menú de servicio completo (puede variar según región)
**Opciones disponibles**:
- [1] UMTS
- [2] Debug Screen
- [3] Phone Control
- [4] Common

**Submenu UMTS**:
- [1] UMTS RRC Status
- [2] UMTS Band Selection
- [3] UMTS RF NV Rebuild

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#197328640#`
3. Navega por las opciones con los números

**⚠️ ADVERTENCIA**: Este es un menú MUY avanzado. NO cambies configuraciones de banda o RF sin conocimiento técnico. Puedes perder conectividad de red.

#### `*#7465625#` - Estado de Bloqueo del Teléfono
**Funcionalidad**: Ver estado de bloqueo SIM
**Información mostrada**:
- Network Lock (Bloqueo de red)
- Subset Lock (Bloqueo de subconjunto)
- SP Lock (Bloqueo de proveedor)
- CP Lock (Bloqueo corporativo)

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#7465625#`
3. Se mostrará el estado de bloqueo

### Códigos de Cámara

#### `*#34971539#` - Información de la Cámara
**Funcionalidad**: Información detallada de la cámara
**Información disponible**:
- Versión del firmware de la cámara
- Fecha de actualización
- Información del sensor

**Opciones**:
- [1] Release Camera Firmware
- [2] Update Camera Firmware
- [3] Get Camera Firmware Version

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#34971539#`
3. Selecciona la opción deseada

**⚠️ Precaución**: NO actualices el firmware de la cámara desde aquí

### Códigos de Reset y Calibración

#### `*2767*3855#` - Reset Completo (FORMATEO TOTAL)
**Funcionalidad**: Formateo completo del dispositivo
**⚠️ PELIGRO**: Este código BORRA TODOS LOS DATOS del dispositivo incluyendo:
- Todas las aplicaciones instaladas
- Configuraciones
- Archivos personales
- Datos de usuario

**NO USES ESTE CÓDIGO A MENOS QUE QUIERAS BORRAR TODO**

#### `*#0*#` - Calibración de Sensores LCD
**Funcionalidad**: Ya descrito arriba en el menú de pruebas
**Incluye calibración de**:
- Pantalla
- Sensores
- Táctil

### Códigos de GPS

#### `*#*#1472365#*#*` - Test de GPS
**Funcionalidad**: Prueba del sistema GPS
**Información mostrada**:
- Estado de los satélites GPS
- Precisión de ubicación
- Velocidad
- Altitud

**Cómo acceder**:
1. Asegúrate de estar al aire libre o cerca de una ventana
2. Abre la aplicación Teléfono
3. Marca `*#*#1472365#*#*`
4. El menú de prueba GPS se abrirá automáticamente

### Códigos de Audio

#### `*#*#0673#*#*` o `*#*#0289#*#*` - Test de Audio
**Funcionalidad**: Prueba de funcionalidad de audio
**Pruebas incluidas**:
- Micrófono
- Altavoz
- Auricular
- Audio Bluetooth

**Cómo acceder**:
1. Abre la aplicación Teléfono
2. Marca `*#*#0673#*#*` o `*#*#0289#*#*`
3. Sigue las instrucciones en pantalla

## 🛠️ Acceso mediante ADB (Android Debug Bridge)

Si tienes ADB habilitado, puedes acceder a algunas funciones de servicio mediante comandos:

### Comandos útiles de ADB para diagnóstico:

```bash
# Obtener información del sistema
adb shell getprop | grep ro.build

# Ver información de la batería
adb shell dumpsys battery

# Ver información de telefonía
adb shell dumpsys telephony.registry

# Ver información de sensores
adb shell dumpsys sensorservice

# Iniciar actividades de servicio (requiere conocer el nombre del componente exacto)
adb shell am start -n com.sec.android.RilServiceModeApp/.MainActivity

# Ver registros del sistema
adb logcat

# Crear un bugreport
adb bugreport
```

### Comandos service.call

Algunos códigos secretos funcionan mediante `service.call`. Ejemplo:

```bash
# Obtener IMEI (código 1 para el servicio de teléfono)
adb shell service call iphonesubinfo 1

# Nota: Los números de servicio pueden variar según la versión de Android
```

## 📱 Acceso desde Configuración Normal

Algunas opciones de desarrollador y diagnóstico están disponibles en el sistema sin códigos secretos:

### Opciones de Desarrollador
1. Ve a **Configuración** > **Acerca del teléfono**
2. Toca **Número de compilación** 7 veces
3. Vuelve a Configuración
4. Ve a **Opciones de desarrollador**

Opciones útiles de diagnóstico:
- **Depuración USB**: Permite comandos ADB
- **Informe de errores**: Captura registros del sistema
- **Estadísticas de procesos**: Ver uso de recursos
- **Estadísticas de GPU**: Rendimiento gráfico
- **Registro de búfer**: Ver logs en tiempo real

### Samsung Members (Diagnóstico)
1. Abre la aplicación **Samsung Members**
2. Ve a **Asistencia** > **Diagnóstico**
3. Ejecuta pruebas de:
   - Pantalla
   - Altavoz
   - Micrófono
   - Conectividad
   - Sensores
   - Botones

## 🔍 Archivos de Configuración de Servicio

El firmware contiene varios archivos de configuración de servicio:

- `/vendor/etc/init/hw/init.target.rc` - Scripts de inicialización
- `/vendor/etc/init/hw/init.samsung.rc` - Inicialización específica de Samsung
- `/vendor/etc/init/hw/init.dm2q.rc` - Inicialización específica del dispositivo dm2q
- `/system/etc/permissions/privapp-permissions-com.sec.android.RilServiceModeApp.xml` - Permisos del modo de servicio

## 📊 Aplicaciones de Monitoreo de Sistema

El firmware incluye varias aplicaciones de monitoreo que se ejecutan en segundo plano:

1. **DiagMonAgent95**: Agente de monitoreo de diagnóstico
2. **DeviceDiagnostics**: Diagnóstico continuo del dispositivo
3. **NetworkDiagnostic**: Monitoreo de red
4. **PhoneErrService**: Servicio de errores telefónicos

## 🔐 Consideraciones de Seguridad

1. **Datos Sensibles**: Muchos menús muestran información sensible (IMEI, números de serie, etc.)
2. **No Compartas Screenshots**: Si capturas pantallas de estos menús, borra información sensible antes de compartir
3. **Bloqueo de Operador**: Algunos códigos pueden mostrar si tu dispositivo está bloqueado a un operador
4. **Garantía**: El uso de estos menús generalmente NO invalida la garantía, pero hacer cambios sí puede hacerlo

## 📝 Notas Adicionales

### Códigos que pueden no funcionar:
Algunos códigos pueden estar deshabilitados por:
- Restricciones del operador
- Región del dispositivo
- Versión de firmware
- Políticas de Samsung

### Si un código no funciona:
1. Verifica que estés usando la aplicación Teléfono de Samsung (no Google Phone)
2. Asegúrate de marcar el código completo exactamente como se muestra
3. Algunos códigos requieren SIM instalada
4. Algunos códigos solo funcionan en versiones específicas de firmware

### Logging y Diagnóstico Avanzado:
Para depuración avanzada, puedes habilitar:
- **Modem logging**: `*#9900#` > Enable Low battery dump
- **Radio logging**: Via opciones de desarrollador
- **Kernel logging**: Via ADB logcat

## ⚡ Menús de Fábrica - Acceso Directo

Algunos dispositivos Samsung permiten acceder a menús de fábrica al apagar:
1. Apaga el dispositivo
2. Mantén presionados: **Volumen Abajo + Bixby + Power** (puede variar)
3. O: **Volumen Arriba + Volumen Abajo + Power**

**Nota**: Estos métodos pueden no funcionar en todos los dispositivos o pueden estar deshabilitados en producción.

## 🎯 Casos de Uso Comunes

### Verificar señal de red:
- Usa `*#0011#` para ver información detallada de señal

### Probar hardware antes de comprar usado:
- Usa `*#0*#` para probar todos los componentes

### Verificar batería degradada:
- Usa `*#0228#` para ver ciclos de carga

### Verificar si el teléfono es original:
- Usa `*#06#` para verificar IMEI
- Compara con el IMEI de la caja

### Diagnóstico de problemas de conectividad:
- Usa `*#0011#` para ver estado de red
- Usa `*#*#4636#*#*` para información detallada

## 📚 Recursos Adicionales

- **Documentación de Qualcomm**: Para información sobre el chip Snapdragon
- **XDA Developers**: Foros con información adicional sobre códigos
- **Samsung Developer**: Documentación oficial de Samsung

## 🆘 Soporte

Si encuentras problemas después de usar estos menús:
1. Reinicia el dispositivo
2. Si el problema persiste, realiza un restablecimiento de configuración de red
3. Como último recurso, realiza un restablecimiento de fábrica (copia de seguridad primero)

## ⚖️ Disclaimer Legal

Esta guía se proporciona solo con fines informativos y educativos. El autor no se hace responsable de:
- Daños al dispositivo
- Pérdida de datos
- Pérdida de garantía
- Problemas de conectividad
- Cualquier otro problema derivado del uso de estos códigos

**USA BAJO TU PROPIO RIESGO**

---

**Última actualización**: Diciembre 2024
**Firmware analizado**: UN1CA-firmware-dm2q (SM-S916B) - Build S916BXXS8EYK5
**Versión de la guía**: 1.0

---

## 🔄 Historial de Cambios

### v1.0 (Diciembre 2024)
- Guía inicial creada
- Análisis completo del firmware UN1CA
- Documentación de todas las aplicaciones de ingeniería encontradas
- Recopilación de códigos secretos conocidos de Samsung
- Instrucciones de acceso y precauciones

---

*Esta guía fue generada mediante análisis del firmware UN1CA-firmware-dm2q para el dispositivo Samsung Galaxy S23 (SM-S916B).*
