# UN1CA Firmware DM2Q - Security XML Documentation

## Quick Start / Inicio Rápido

This repository contains documentation for the security XML files in the UN1CA firmware for Samsung Galaxy dm2q devices.

Este repositorio contiene documentación para los archivos XML de seguridad en el firmware UN1CA para dispositivos Samsung Galaxy dm2q.

---

## 📚 Documentation Files / Archivos de Documentación

### 1. **GUIA_ARCHIVOS_XML_SEGURIDAD.md** (Spanish)
Guía completa en español sobre los archivos XML de seguridad.
- Explicación detallada de cada archivo
- Ejemplos prácticos
- Advertencias y mejores prácticas
- Solución de problemas

### 2. **SECURITY_XML_FILES_GUIDE.md** (English & Spanish)
Bilingual comprehensive guide for security XML files.
- Detailed explanation of each file
- Valid options and modifications
- Examples and use cases
- Warnings and best practices

### 3. **security_xml_reference.json**
Machine-readable reference in JSON format.
- Complete file structures
- Valid options for each field
- Modification guidelines
- Warnings and impact levels

---

## 🔐 Security XML Files Covered / Archivos XML Cubiertos

| File / Archivo | Purpose / Propósito |
|----------------|---------------------|
| **ADP.xml** | Application Data Protection |
| **ASKSB.xml** | Application Blacklist / Lista Negra |
| **ASKSC.xml** | Certificate List / Lista de Certificados |
| **ASKSHB.xml** | Hidden Blacklist / Lista Negra Oculta |
| **ASKSP.xml** | Special Package List / Paquetes Especiales |
| **ASKSRNEW.xml** | Restricted Applications / Aplicaciones Restringidas |
| **ASKSTS.xml** | Trusted Store / Almacén de Confianza |
| **ASKSW.xml** | Application Whitelist / Lista Blanca |
| **PAICheck.xml** | Package Authenticity Check / Verificación de Autenticidad |

---

## ⚠️ Important Warnings / Advertencias Importantes

### English:
- **Root access required** to modify these files
- **Make backups** before any modification
- Modifications may **void Knox warranty**
- Invalid XML can **prevent device from booting**
- Samsung Pay and banking apps may stop working

### Español:
- Se requiere **acceso root** para modificar estos archivos
- **Haga copias de seguridad** antes de cualquier modificación
- Las modificaciones pueden **anular la garantía Knox**
- XML inválido puede **impedir que el dispositivo arranque**
- Samsung Pay y apps bancarias pueden dejar de funcionar

---

## 🛠️ How to Use / Cómo Usar

### For Users / Para Usuarios:
1. Read the appropriate guide (Spanish or English)
2. Understand what each file does
3. Make backups before modifying
4. Follow the examples provided
5. Validate your changes

### For Developers / Para Desarrolladores:
1. Use `security_xml_reference.json` for programmatic access
2. Parse the JSON to understand file structures
3. Validate modifications against the schema
4. Implement proper error handling

---

## 📖 File Locations / Ubicaciones de Archivos

All XML files are located in: `/system/etc/`

Todos los archivos XML están ubicados en: `/system/etc/`

```
/system/etc/ADP.xml
/system/etc/ASKSB.xml
/system/etc/ASKSC.xml
/system/etc/ASKSHB.xml
/system/etc/ASKSP.xml
/system/etc/ASKSRNEW.xml
/system/etc/ASKSTS.xml
/system/etc/ASKSW.xml
/system/etc/PAICheck.xml
```

---

## 🔧 Common Operations / Operaciones Comunes

### Backup a file / Hacer copia de un archivo:
```bash
adb pull /system/etc/ADP.xml ADP.xml.backup
```

### Get SHA256 hash of an APK / Obtener hash SHA256 de un APK:
```bash
sha256sum app.apk
```

### Validate XML syntax / Validar sintaxis XML:
```bash
xmllint --noout file.xml
```

### Push modified file / Enviar archivo modificado:
```bash
adb root
adb remount
adb push ADP.xml /system/etc/
adb reboot
```

---

## 🎯 Use Cases / Casos de Uso

### Block an application / Bloquear una aplicación:
Edit `ASKSB.xml` to add the application hash to the blacklist.

Editar `ASKSB.xml` para agregar el hash de la aplicación a la lista negra.

### Allow a custom app / Permitir una aplicación personalizada:
Edit `ASKSW.xml` to add the application hash to the whitelist.

Editar `ASKSW.xml` para agregar el hash de la aplicación a la lista blanca.

### Mark an app as trusted / Marcar una app como confiable:
Edit `ASKSTS.xml` to add the application to the trusted store.

Editar `ASKSTS.xml` para agregar la aplicación al almacén de confianza.

---

## 🤝 Contributing / Contribuciones

Found an error or want to add more information?

¿Encontraste un error o quieres agregar más información?

1. Fork this repository
2. Make your changes
3. Submit a pull request

---

## 📱 Device Compatibility / Compatibilidad de Dispositivos

- **Target Device:** Samsung Galaxy (dm2q variant)
- **Firmware:** UN1CA-firmware-dm2q
- **Android Version:** Check device specifications
- **Knox Version:** Samsung Knox enabled devices

---

## 📞 Support / Soporte

For questions or issues:
Para preguntas o problemas:

- Open an issue in this repository
- Check XDA Developers forums
- Consult Samsung Knox documentation

---

## 📜 License / Licencia

This documentation is provided as-is for educational purposes.

Esta documentación se proporciona tal cual con fines educativos.

**Disclaimer / Descargo de responsabilidad:**
- Modifying system files is at your own risk
- We are not responsible for bricked devices
- Always maintain proper backups

- Modificar archivos del sistema es bajo tu propio riesgo
- No somos responsables de dispositivos dañados
- Siempre mantén copias de seguridad adecuadas

---

## 🔄 Version History / Historial de Versiones

### v1.0.0 (2025-12-28)
- Initial documentation release
- Complete guide for all 9 security XML files
- JSON reference added
- Bilingual support (English/Spanish)

---

## 🌟 Credits / Créditos

Documentation created for the UN1CA firmware project.

Documentación creada para el proyecto de firmware UN1CA.

**Last Updated / Última Actualización:** 2025-12-28
