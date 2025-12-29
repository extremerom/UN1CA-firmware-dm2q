# 📱 Análisis de Firmware UN1CA - Samsung Galaxy S23

## 🎯 Objetivo del Análisis

Este repositorio contiene el análisis completo del firmware UN1CA para el Samsung Galaxy S23 (SM-S916B / dm2q), con especial énfasis en la identificación y documentación de menús de ingeniería y códigos secretos.

## 📋 Dispositivo Analizado

- **Modelo**: Samsung Galaxy S23
- **Número de Modelo**: SM-S916B
- **Nombre de Código**: dm2q / dm2qxxx
- **Versión de Android**: 16 (SDK 36)
- **Build**: BP2A.250605.031.A3
- **Versión de Firmware**: S916BXXS8EYK5
- **Firmware Base**: UN1CA
- **Fecha de compilación del firmware**: 28 de Noviembre de 2024 (KST)

## 📚 Documentación Generada

### 1. [ENGINEERING_MENUS_GUIDE.md](ENGINEERING_MENUS_GUIDE.md)
**Guía completa de menús de ingeniería**

Esta guía exhaustiva incluye:

#### 📱 Aplicaciones de Ingeniería Identificadas (12+)
- ModemServiceMode (Modo de servicio del módem)
- SecFactoryPhoneTest (Pruebas de teléfono de fábrica)
- DiagMonAgent95 (Agente de monitoreo)
- DeviceDiagnostics (Diagnóstico del dispositivo)
- NetworkDiagnostic (Diagnóstico de red)
- SEMFactoryApp (Aplicación de fábrica)
- SmartEpdgTestApp (Pruebas ePDG)
- FactoryTestProvider (Proveedor de pruebas)
- FactoryCameraFB (Cámara de fábrica)
- FactoryAirCommandManager (Gestor Air Command)
- UwbTest (Pruebas UWB)
- WlanTest (Pruebas WLAN)

#### 🔢 Códigos Secretos Documentados (20+)
- `*#0*#` - Menú completo de pruebas de hardware
- `*#*#4636#*#*` - Información del teléfono
- `*#06#` - Información IMEI
- `*#1234#` - Versión de firmware
- `*#12580*369#` - Info hardware/software
- `*#9900#` - SysDump
- `*#0228#` - Estado de batería
- `*#0011#` - Estado de servicio GSM
- Y muchos más...

#### 🛠️ Incluye
- Instrucciones detalladas de acceso
- Precauciones y advertencias
- Casos de uso comunes
- Comandos ADB útiles
- Consideraciones de seguridad

### 2. [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
**Guía rápida de referencia**

Tarjeta de referencia rápida con:
- Tabla de códigos más usados
- Indicadores de nivel de peligro
- Lista de apps de ingeniería
- Tips y trucos rápidos
- Reglas de oro de seguridad

## 🔍 Metodología del Análisis

El análisis del firmware se realizó mediante:

1. **Exploración de estructura de archivos**
   - Identificación de particiones del sistema
   - Mapeo de directorios clave

2. **Búsqueda de aplicaciones de ingeniería**
   - Análisis de `/system/priv-app/`
   - Análisis de `/system/app/`
   - Identificación de APKs de prueba y diagnóstico

3. **Análisis de permisos**
   - Revisión de archivos XML de permisos
   - Identificación de capacidades privilegiadas

4. **Búsqueda de patrones conocidos**
   - Referencias a "ServiceMode"
   - Referencias a "Factory"
   - Referencias a "Test" y "Diagnostic"

5. **Documentación de códigos secretos**
   - Códigos conocidos de Samsung
   - Variantes específicas del modelo
   - Códigos de la serie Galaxy S

## 📊 Estructura del Firmware

```
/
├── system/
│   ├── system/
│   │   ├── priv-app/          # Apps privilegiadas del sistema
│   │   │   ├── ModemServiceMode/
│   │   │   ├── SecFactoryPhoneTest/
│   │   │   ├── DiagMonAgent95/
│   │   │   ├── DeviceDiagnostics/
│   │   │   ├── NetworkDiagnostic/
│   │   │   └── SEMFactoryApp/
│   │   ├── app/               # Apps del sistema
│   │   │   ├── FactoryCameraFB/
│   │   │   ├── UwbTest/
│   │   │   └── WlanTest/
│   │   └── etc/
│   │       └── permissions/   # Definiciones de permisos
├── vendor/                     # Firmware del fabricante
├── product/                    # Apps y configuraciones de producto
├── system_ext/                 # Extensiones del sistema
└── odm/                        # Módulos específicos del dispositivo
```

## 🔐 Aplicaciones con Permisos Especiales

### ModemServiceMode (`com.sec.android.RilServiceModeApp`)

**Permisos privilegiados**:
- `ACCESS_CHECKIN_PROPERTIES` - Propiedades del sistema
- `CHANGE_CONFIGURATION` - Modificar configuración
- `MODIFY_PHONE_STATE` - Modificar estado telefónico
- `MOUNT_UNMOUNT_FILESYSTEMS` - Montar/desmontar FS
- `WRITE_APN_SETTINGS` - Escribir APN
- `READ_PRIVILEGED_PHONE_STATE` - Estado privilegiado
- `ACCESS_FINE_LOCATION` - Ubicación precisa
- `SET_DEBUG_APP` - Depuración

**Tamaño**: 2.7MB
**Ubicación**: `/system/priv-app/ModemServiceMode/ModemServiceMode.apk`

## ⚠️ Advertencias Importantes

### 🔴 Uso Responsable
- Estos menús están diseñados para técnicos y personal de fábrica
- El uso incorrecto puede causar problemas en el dispositivo
- Algunos cambios pueden ser permanentes
- Puede invalidar la garantía

### 🔒 Seguridad
- No compartas screenshots con información sensible (IMEI, SN)
- Algunos menús muestran datos privados
- Usa los códigos en un entorno privado

### 📱 Compatibilidad
- Algunos códigos pueden estar deshabilitados por operadores
- Variaciones regionales pueden afectar funcionalidad
- Versiones de firmware diferentes pueden comportarse distinto

## 🎓 Casos de Uso Educativos

### Para estudiantes y técnicos:
- Aprender sobre arquitectura de Android
- Comprender estructura de firmware Samsung
- Estudiar permisos y seguridad en Android

### Para usuarios avanzados:
- Diagnosticar problemas de hardware
- Verificar autenticidad del dispositivo
- Realizar pruebas antes de comprar usado

### Para desarrolladores:
- Comprender capacidades del hardware
- Acceder a información de diagnóstico
- Depurar problemas de conectividad

## 📖 Recursos Adicionales

### Documentación Relacionada
- [Documentación oficial de Samsung](https://developer.samsung.com/)
- [Android Developer Documentation](https://developer.android.com/)
- [XDA Developers Forums](https://forum.xda-developers.com/)

### Herramientas Útiles
- **ADB (Android Debug Bridge)**: Para comandos avanzados
- **Device Info HW**: App para ver información de hardware
- **CPU-Z**: Información detallada del sistema
- **Phone INFO ★SAM★**: Información específica de Samsung

## 🔄 Actualizaciones

Este análisis se basa en:
- **Fecha de Análisis**: Diciembre 2024
- **Firmware**: UN1CA (S916BXXS8EYK5)
- **Versión de Guía**: 1.0

### Próximas actualizaciones pueden incluir:
- Análisis de nuevas versiones de firmware
- Códigos adicionales descubiertos
- Actualizaciones de compatibilidad
- Nuevas aplicaciones de diagnóstico

## 🤝 Contribuciones

Si encuentras:
- Códigos adicionales que funcionen
- Errores en la documentación
- Nuevas aplicaciones de ingeniería
- Mejoras en las instrucciones

Por favor, considera contribuir al proyecto.

## ⚖️ Disclaimer Legal

Esta documentación se proporciona **SOLO CON FINES EDUCATIVOS E INFORMATIVOS**.

**El autor NO se hace responsable de**:
- Daños al dispositivo
- Pérdida de datos
- Pérdida de garantía
- Problemas de conectividad
- Mal funcionamiento del dispositivo
- Cualquier otro problema derivado del uso de esta información

**USA BAJO TU PROPIO RIESGO**

Este análisis no promueve:
- Violación de garantías
- Modificación no autorizada
- Acceso no autorizado a funciones
- Cualquier actividad ilegal

## 📄 Licencia

Esta documentación se proporciona tal cual, sin garantías de ningún tipo.
Es responsabilidad del usuario usar esta información de manera responsable y legal.

## 👤 Autor

Análisis realizado mediante ingeniería inversa no invasiva del firmware público UN1CA-firmware-dm2q.

## 🌟 Agradecimientos

- Samsung por proporcionar firmware actualizado
- Comunidad XDA Developers por información sobre códigos
- Comunidad Android por herramientas de análisis

---

**Última actualización**: Diciembre 2024
**Versión del Documento**: 1.0

---

## 📞 Contacto

Para preguntas, correcciones o sugerencias, por favor abre un issue en este repositorio.

---

⚠️ **Recuerda**: Usa estos menús de manera responsable. El conocimiento es poder, pero también trae responsabilidad.

---

**Made with 🔍 by analyzing UN1CA firmware for Samsung Galaxy S23**
