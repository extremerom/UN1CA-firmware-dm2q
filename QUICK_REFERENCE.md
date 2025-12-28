# Quick Reference Card - Security XML Files
# Tarjeta de Referencia Rápida - Archivos XML de Seguridad

## ADP.xml - Application Data Protection
📍 /system/etc/ADP.xml
🔑 Validates app integrity with SHA256
✏️ Add: <HASHVALUE name="SHA256"><pattern value="regex"><hashCode value="123"/></pattern></HASHVALUE>

## ASKSB.xml - Blacklist / Lista Negra
📍 /system/etc/ASKSB.xml
🔑 Blocks unwanted apps / Bloquea apps no deseadas
✏️ Add: <HASHVALUE name="SHA256"><HASH value="ALL"/></HASHVALUE>

## ASKSC.xml - Certificates / Certificados
📍 /system/etc/ASKSC.xml
🔑 Certificate validation / Validación de certificados
✏️ Add: <CERT name="cert_name"><HASH value="SHA256"/></CERT>
⚠️ Currently empty / Actualmente vacío

## ASKSHB.xml - Hidden Blacklist / Lista Negra Oculta
📍 /system/etc/ASKSHB.xml
🔑 Silent app blocking / Bloqueo silencioso
✏️ Same as ASKSB / Igual que ASKSB
⚠️ Currently empty / Actualmente vacío

## ASKSP.xml - Special Packages / Paquetes Especiales
📍 /system/etc/ASKSP.xml
🔑 Apps needing special permissions / Apps con permisos especiales
✏️ Add: <HASHVALUE name="com.package.name"><UID name="NONE"/></HASHVALUE>
📋 Current: com.sec.android.easyMover, com.rsupport.rs.activity.rsupport.aas2

## ASKSRNEW.xml - Restricted / Restringidas
📍 /system/etc/ASKSRNEW.xml
🔑 Apps with limited access / Apps con acceso limitado
✏️ Add: <PACKAGE name="pkg"><RESTRICTION type="type"/></PACKAGE>
⚠️ Currently empty / Actualmente vacío

## ASKSTS.xml - Trusted Store / Almacén de Confianza
📍 /system/etc/ASKSTS.xml
🔑 Trusted apps with special perms / Apps confiables con permisos especiales
✏️ Add: <STORE name="AppName"><DUMMY value="0"/></STORE>
📋 Current: PrePackageInstaller

## ASKSW.xml - Whitelist / Lista Blanca
📍 /system/etc/ASKSW.xml
🔑 Explicitly allowed apps / Apps explícitamente permitidas
✏️ Add: <HASHVALUE name="SHA256"><HASH value="signature_hash"/></HASHVALUE>

## PAICheck.xml - Package Authenticity
📍 /system/etc/PAICheck.xml
🔑 Additional integrity check / Verificación adicional de integridad
⚠️ Currently empty / Actualmente vacío

---

## 🔓 HOW TO DISABLE SECURITY / CÓMO DESACTIVAR SEGURIDAD

### ⚠️ CRITICAL: Read full docs before disabling!
### ⚠️ CRÍTICO: ¡Lee la documentación completa antes de desactivar!

### Quick Disable Methods / Métodos Rápidos de Desactivación:

#### 1️⃣ Empty Lists (Safest) / Vaciar Listas (Más Seguro)
```xml
<VERSION value="20251228"/>
<LIST></LIST>  <!-- For ASKSB, ASKSHB, ASKSW -->
```

#### 2️⃣ Remove Specific Entry / Eliminar Entrada Específica
Delete or comment out the HASHVALUE block for specific app
Eliminar o comentar el bloque HASHVALUE para app específica

#### 3️⃣ Move to Whitelist / Mover a Lista Blanca
Remove from ASKSB.xml → Add to ASKSW.xml
Eliminar de ASKSB.xml → Agregar a ASKSW.xml

#### 4️⃣ Disable ADP (DANGEROUS!) / Desactivar ADP (¡PELIGROSO!)
```xml
<VERSION value="20251228"/>
<ADP version="3.1"></ADP>  <!-- System may break! -->
```

### 🚨 Risks / Riesgos:
- 🔴 Malware can install / Malware puede instalarse
- 🔴 System instability / Inestabilidad del sistema
- 🔴 Knox warranty void / Garantía Knox anulada
- 🔴 Banking apps fail / Apps bancarias fallan

### ✅ Safer Alternative / Alternativa Más Segura:
**Don't disable - Add exceptions!**
**¡No desactives - Agrega excepciones!**

Use ASKSW.xml to whitelist your apps instead
Usa ASKSW.xml para permitir tus apps en su lugar

---

## Common Commands / Comandos Comunes

### Backup / Copia de Seguridad
```bash
adb pull /system/etc/[file].xml backup_[file].xml
```

### Get APK Hash / Obtener Hash de APK
```bash
sha256sum app.apk
```

### Get Certificate Hash / Obtener Hash de Certificado
```bash
unzip -p app.apk META-INF/*.RSA | keytool -printcert | grep SHA256
```

### Validate XML / Validar XML
```bash
xmllint --noout file.xml
```

### Push File / Enviar Archivo
```bash
adb root
adb remount
adb push [file].xml /system/etc/
adb reboot
```

---

## Warning Symbols / Símbolos de Advertencia

🔴 **CRITICAL** - May prevent boot / Puede impedir arranque
🟡 **CAUTION** - May affect features / Puede afectar funciones
🟢 **SAFE** - Minor impact / Impacto menor

⚠️ Root required / Requiere root
🔓 Knox warranty void / Anula garantía Knox
💳 Banking apps affected / Apps bancarias afectadas
📱 Samsung Pay affected / Samsung Pay afectado

---

## File Status Legend / Leyenda de Estado

📋 Has entries / Tiene entradas
⚠️ Empty file / Archivo vacío
✏️ Can be modified / Puede modificarse
🔒 Protected by Knox / Protegido por Knox
📍 Location / Ubicación
🔑 Purpose / Propósito

---

## Modification Risk Levels / Niveles de Riesgo

| File | Risk | Impact |
|------|------|--------|
| ADP.xml | 🔴 HIGH | Boot/System apps |
| ASKSB.xml | 🟡 MED | App blocking |
| ASKSC.xml | 🟡 MED | Certificates |
| ASKSHB.xml | 🟡 MED | App blocking |
| ASKSP.xml | 🟡 MED | Permissions |
| ASKSRNEW.xml | 🟡 MED | Access control |
| ASKSTS.xml | 🔴 HIGH | Trusted apps |
| ASKSW.xml | 🟡 MED | App allowing |
| PAICheck.xml | 🟢 LOW | Unknown (empty) |

---

## Quick Syntax / Sintaxis Rápida

### VERSION (All files / Todos los archivos)
```xml
<VERSION value="20251228"/>
```

### HASHVALUE with ALL
```xml
<HASHVALUE name="64_char_sha256_hash">
  <HASH value="ALL"/>
</HASHVALUE>
```

### HASHVALUE with specific hash
```xml
<HASHVALUE name="64_char_sha256_hash">
  <HASH value="64_char_signature_hash"/>
</HASHVALUE>
```

### Package with UID
```xml
<HASHVALUE name="com.package.name">
  <UID name="NONE"/>
</HASHVALUE>
```

### Trusted Store Entry
```xml
<STORE name="ApplicationName">
  <DUMMY value="0"/>
</STORE>
```

### ADP Pattern
```xml
<HASHVALUE name="64_char_sha256_hash">
  <pattern value="[0-9]+">
    <hashCode value="123456789" />
    <versionType value="1" />
    <format value="([0-9]+)" />
  </pattern>
</HASHVALUE>
```

---

## Emergency Recovery / Recuperación de Emergencia

### If device won't boot / Si el dispositivo no arranca:
1. Boot to recovery mode / Arrancar en modo recovery
2. Mount /system
3. Restore backup files / Restaurar archivos de respaldo
4. Reboot / Reiniciar

### If system apps crash / Si las apps del sistema fallan:
1. Check XML syntax / Verificar sintaxis XML
2. Verify hashes are correct / Verificar que los hashes sean correctos
3. Restore original file / Restaurar archivo original
4. Clear cache and dalvik / Limpiar cache y dalvik

---

## Support Resources / Recursos de Soporte

📚 Full Documentation:
- README_SECURITY_XML.md
- SECURITY_XML_FILES_GUIDE.md (EN/ES)
- GUIA_ARCHIVOS_XML_SEGURIDAD.md (ES)
- security_xml_reference.json (JSON)

🌐 Online:
- Samsung Knox Docs: https://docs.samsungknox.com/
- XDA Forums: https://forum.xda-developers.com/
- Android Security: https://source.android.com/security

---

**Version:** 1.0.0
**Date:** 2025-12-28
**Firmware:** UN1CA-firmware-dm2q
**Device:** Samsung Galaxy dm2q

⚠️ ALWAYS BACKUP BEFORE MODIFYING / SIEMPRE RESPALDE ANTES DE MODIFICAR
