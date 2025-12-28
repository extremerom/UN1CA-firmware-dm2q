# Security XML Files Guide

## Guía de Archivos XML de Seguridad / Security XML Files Guide

Esta guía explica qué hacen estos archivos XML de seguridad y cuáles son las opciones válidas para modificarlos.

This guide explains what these security XML files do and what are the valid options for modifying them.

---

## ADP.xml (Application Data Protection)

**Ubicación / Location:** `/system/etc/ADP.xml`

**Propósito / Purpose:** 
Sistema de protección de aplicaciones que define reglas de hashing y validación para aplicaciones del sistema. Utilizado por Samsung Knox para verificar la integridad de aplicaciones.

Application protection system that defines hashing and validation rules for system applications. Used by Samsung Knox to verify application integrity.

**Estructura / Structure:**
```xml
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<VERSION value="YYYYMMDD"/>
<ADP version="3.1">
    <HASHVALUE name="hash_sha256">
        <pattern value="regex_pattern">
            <hashCode value="numeric_code"/>
            <versionType value="type_number"/>
            <format value="format_string"/>
        </pattern>
    </HASHVALUE>
</ADP>
```

**Opciones Válidas / Valid Options:**

1. **VERSION value**: Fecha en formato YYYYMMDD (ej: "20250902")
   - Date in YYYYMMDD format (e.g., "20250902")

2. **ADP version**: Versión del esquema ADP (ej: "3.1")
   - ADP schema version (e.g., "3.1")

3. **HASHVALUE name**: Hash SHA256 de la aplicación
   - SHA256 hash of the application

4. **pattern value**: Expresión regular para validar versiones
   - Regular expression to validate versions
   - Ejemplos / Examples:
     - `^\d{9}\z` - Exactly 9 digits
     - `^\d{10}\z` - Exactly 10 digits
     - `[0-9]+` - One or more digits
     - `^\d{4}00\d{3}\z` - Specific pattern (4 digits + "00" + 3 digits)

5. **hashCode value**: Código hash numérico único
   - Unique numeric hash code
   - Debe ser un número entero / Must be an integer

6. **versionType value**: Tipo de versión
   - Version type
   - Valores comunes / Common values: 1, 2, 3, 5, 1703114115

7. **format value**: Formato de captura regex (opcional)
   - Regex capture format (optional)
   - Ejemplo / Example: `([0-9]+)`

**Ejemplo de Modificación / Modification Example:**
```xml
<HASHVALUE name="new_app_hash_here">
    <pattern value="[0-9]+">
        <hashCode value="123456789" />
        <versionType value="1703114115" />
        <format value="([0-9]+)" />
    </pattern>
</HASHVALUE>
```

---

## ASKSB.xml (ASKS Blacklist)

**Ubicación / Location:** `/system/etc/ASKSB.xml`

**Propósito / Purpose:**
Lista negra de aplicaciones. Contiene hashes de aplicaciones bloqueadas o no permitidas en el sistema.

Application blacklist. Contains hashes of blocked or disallowed applications on the system.

**Estructura / Structure:**
```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<VERSION value="YYYYMMDD"/>
<LIST>
  <HASHVALUE name="app_hash">
    <HASH value="signature_hash"/>
  </HASHVALUE>
</LIST>
```

**Opciones Válidas / Valid Options:**

1. **VERSION value**: Fecha en formato YYYYMMDD
   - Date in YYYYMMDD format

2. **HASHVALUE name**: Hash SHA256 del paquete de la aplicación
   - SHA256 hash of the application package

3. **HASH value**: 
   - `"ALL"` - Bloquear todas las versiones / Block all versions
   - Hash SHA256 específico - Bloquear versión específica / Block specific version

**Ejemplo de Modificación / Modification Example:**
```xml
<HASHVALUE name="suspicious_app_hash_here">
  <HASH value="ALL"/>
</HASHVALUE>
```

---

## ASKSC.xml (ASKS Certificate List)

**Ubicación / Location:** `/system/etc/ASKSC.xml`

**Propósito / Purpose:**
Lista de certificados. Actualmente vacía en esta configuración. Usado para validación de certificados de aplicaciones.

Certificate list. Currently empty in this configuration. Used for application certificate validation.

**Estructura / Structure:**
```xml
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<VERSION value="YYYYMMDD"/>
<CLIST>
</CLIST>
```

**Opciones Válidas / Valid Options:**

1. **VERSION value**: Fecha en formato YYYYMMDD
   - Date in YYYYMMDD format

2. **Dentro de CLIST se pueden agregar / Inside CLIST you can add:**
```xml
<CERT name="certificate_name">
  <HASH value="certificate_hash"/>
</CERT>
```

---

## ASKSHB.xml (ASKS Hidden Blacklist)

**Ubicación / Location:** `/system/etc/ASKSHB.xml`

**Propósito / Purpose:**
Lista negra oculta. Similar a ASKSB pero para aplicaciones que deben bloquearse de forma silenciosa.

Hidden blacklist. Similar to ASKSB but for applications that must be blocked silently.

**Estructura / Structure:**
```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<VERSION value="YYYYMMDD"/>
<LIST>
</LIST>
```

**Opciones Válidas / Valid Options:**
Mismas que ASKSB.xml / Same as ASKSB.xml

---

## ASKSP.xml (ASKS Package List)

**Ubicación / Location:** `/system/etc/ASKSP.xml`

**Propósito / Purpose:**
Lista de paquetes especiales que requieren manejo especial de permisos o validación.

List of special packages that require special permission handling or validation.

**Estructura / Structure:**
```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<VERSION value="YYYYMMDD"/>
<LIST>
  <HASHVALUE name="package_name">
    <UID name="user_id"/>
  </HASHVALUE>
</LIST>
```

**Opciones Válidas / Valid Options:**

1. **VERSION value**: Fecha en formato YYYYMMDD
   - Date in YYYYMMDD format

2. **HASHVALUE name**: Nombre del paquete (ej: "com.example.app")
   - Package name (e.g., "com.example.app")

3. **UID name**: 
   - `"NONE"` - Sin UID específico / No specific UID
   - Número de UID / UID number

**Ejemplo / Example:**
```xml
<HASHVALUE name="com.samsung.android.easyMover">
  <UID name="NONE"/>
</HASHVALUE>
```

---

## ASKSRNEW.xml (ASKS Restricted New)

**Ubicación / Location:** `/system/etc/ASKSRNEW.xml`

**Propósito / Purpose:**
Lista de aplicaciones con restricciones. Define aplicaciones que tienen acceso limitado o restringido.

List of restricted applications. Defines applications that have limited or restricted access.

**Estructura / Structure:**
```xml
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<VERSION value="YYYYMMDD"/>
<RESTRICTED>
</RESTRICTED>
```

**Opciones Válidas / Valid Options:**

1. **VERSION value**: Fecha en formato YYYYMMDD
   - Date in YYYYMMDD format

2. **Dentro de RESTRICTED se pueden agregar / Inside RESTRICTED you can add:**
```xml
<PACKAGE name="package_name">
  <RESTRICTION type="restriction_type"/>
</PACKAGE>
```

---

## ASKSTS.xml (ASKS Trusted Store)

**Ubicación / Location:** `/system/etc/ASKSTS.xml`

**Propósito / Purpose:**
Almacén de confianza. Define aplicaciones y servicios de confianza que tienen permisos especiales.

Trusted store. Defines trusted applications and services that have special permissions.

**Estructura / Structure:**
```xml
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<VERSION value="YYYYMMDD"/>
<TRUSTEDSTORE>
    <STORE name="store_name">
        <DUMMY value="0"/>
    </STORE>
</TRUSTEDSTORE>
```

**Opciones Válidas / Valid Options:**

1. **VERSION value**: Fecha en formato YYYYMMDD
   - Date in YYYYMMDD format

2. **STORE name**: Nombre del almacén de confianza
   - Name of the trusted store
   - Ejemplo / Example: "PrePackageInstaller"

3. **DUMMY value**: Valor dummy (usualmente "0" o "1")
   - Dummy value (usually "0" or "1")

**Ejemplo de Modificación / Modification Example:**
```xml
<STORE name="CustomTrustedApp">
    <DUMMY value="0"/>
</STORE>
```

---

## ASKSW.xml (ASKS Whitelist)

**Ubicación / Location:** `/system/etc/ASKSW.xml`

**Propósito / Purpose:**
Lista blanca de aplicaciones. Contiene hashes de aplicaciones permitidas explícitamente.

Application whitelist. Contains hashes of explicitly allowed applications.

**Estructura / Structure:**
```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<VERSION value="YYYYMMDD"/>
<LIST>
    <HASHVALUE name="app_hash">
        <HASH value="signature_hash"/>
    </HASHVALUE>
</LIST>
```

**Opciones Válidas / Valid Options:**
Mismas que ASKSB.xml pero para permitir aplicaciones / Same as ASKSB.xml but to allow applications

**Ejemplo / Example:**
```xml
<HASHVALUE name="5f2a1c280e6efb603b4ddc46b5d3a97d7dd4624b4d4bd3e53b6f4c13e1a5b88f">
    <HASH value="dc9cf540b947d24e47998c22d3094ca25506face2c7ffe91fc019af4afd05b35"/>
    <HASH value="2e3ec9eeae4cbf87bce5b79c4395bfaefc23a41e75f43d500fbb05c3318c467a"/>
</HASHVALUE>
```

---

## PAICheck.xml (Package Authenticity Check)

**Ubicación / Location:** `/system/etc/PAICheck.xml`

**Propósito / Purpose:**
Verificación de autenticidad de paquetes. Actualmente vacío - usado para validación adicional de integridad.

Package authenticity check. Currently empty - used for additional integrity validation.

**Estructura / Structure:**
```xml
(Currently empty file)
```

**Opciones Válidas / Valid Options:**
Este archivo está actualmente vacío. Si se necesita agregar contenido, debe seguir un esquema XML válido.

This file is currently empty. If content needs to be added, it must follow a valid XML schema.

---

## Precauciones Importantes / Important Precautions

⚠️ **ADVERTENCIA / WARNING:**

1. **No elimine estos archivos** - Son parte del sistema de seguridad Samsung Knox
   - **Do not delete these files** - They are part of Samsung Knox security system

2. **Haga copias de seguridad** antes de modificar
   - **Make backups** before modifying

3. **Validación XML** - Asegúrese de que el XML sea válido después de modificar
   - **XML Validation** - Ensure XML is valid after modification

4. **Permisos del sistema** - Modificar estos archivos puede requerir acceso root
   - **System permissions** - Modifying these files may require root access

5. **Knox warranty** - Modificar archivos de seguridad puede afectar Knox Warranty Bit
   - **Knox warranty** - Modifying security files may affect Knox Warranty Bit

6. **Impacto en aplicaciones** - Cambios incorrectos pueden bloquear aplicaciones legítimas
   - **Application impact** - Incorrect changes may block legitimate applications

---

## Herramientas para Generar Hashes / Tools to Generate Hashes

Para obtener el hash SHA256 de una aplicación:

To get the SHA256 hash of an application:

```bash
# Para APK / For APK
sha256sum app.apk

# Para certificado / For certificate
keytool -printcert -file CERT.RSA | grep SHA256
```

---

## Referencias / References

- Samsung Knox Documentation
- Android Security Framework
- ASKS (Application Security Knowledge System)

---

**Última actualización / Last updated:** 2025-12-28
**Versión del firmware / Firmware version:** UN1CA dm2q
