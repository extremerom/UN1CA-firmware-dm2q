# Guía de Archivos XML de Seguridad

## ¿Qué hacen estos archivos?

Estos archivos XML son parte del sistema de seguridad Samsung Knox en el firmware de Android. Controlan qué aplicaciones pueden instalarse, ejecutarse y qué permisos tienen.

---

## 📋 Resumen Rápido

| Archivo | Propósito Principal |
|---------|-------------------|
| **ADP.xml** | Protección de datos de aplicaciones - valida integridad |
| **ASKSB.xml** | Lista negra - aplicaciones bloqueadas |
| **ASKSC.xml** | Lista de certificados de seguridad |
| **ASKSHB.xml** | Lista negra oculta |
| **ASKSP.xml** | Paquetes con permisos especiales |
| **ASKSRNEW.xml** | Aplicaciones con restricciones |
| **ASKSTS.xml** | Almacén de aplicaciones confiables |
| **ASKSW.xml** | Lista blanca - aplicaciones permitidas |
| **PAICheck.xml** | Verificación de autenticidad de paquetes |

---

## 📖 Descripción Detallada

### 1. ADP.xml - Application Data Protection

**Para qué sirve:**
- Verifica que las aplicaciones del sistema no hayan sido modificadas
- Usa hashes SHA256 para validar integridad
- Parte del sistema Knox de Samsung

**Cómo modificarlo:**
```xml
<HASHVALUE name="tu_hash_sha256_aqui">
    <pattern value="[0-9]+">
        <hashCode value="123456789" />
        <versionType value="1" />
        <format value="([0-9]+)" />
    </pattern>
</HASHVALUE>
```

**Campos importantes:**
- `VERSION value`: Fecha de la versión (YYYYMMDD)
- `name`: Hash SHA256 de la aplicación
- `pattern`: Patrón regex para validar versiones
- `hashCode`: Código numérico único
- `versionType`: Tipo de versión (1, 2, 3, 5, o números largos)

---

### 2. ASKSB.xml - Lista Negra (Blacklist)

**Para qué sirve:**
- Bloquea aplicaciones maliciosas o no deseadas
- Impide su instalación o ejecución

**Cómo bloquear una aplicación:**
```xml
<HASHVALUE name="hash_de_la_aplicacion">
  <HASH value="ALL"/>
</HASHVALUE>
```

- Use `value="ALL"` para bloquear todas las versiones
- Use un hash específico para bloquear una versión particular

---

### 3. ASKSC.xml - Certificados

**Para qué sirve:**
- Almacena certificados de seguridad
- Valida firmas de aplicaciones

**Cómo agregar certificado:**
```xml
<CLIST>
  <CERT name="nombre_del_certificado">
    <HASH value="hash_del_certificado"/>
  </CERT>
</CLIST>
```

---

### 4. ASKSHB.xml - Lista Negra Oculta

**Para qué sirve:**
- Similar a ASKSB pero más discreta
- Bloquea aplicaciones sin mostrar mensajes al usuario

**Uso:** Igual que ASKSB.xml

---

### 5. ASKSP.xml - Paquetes Especiales

**Para qué sirve:**
- Define aplicaciones que necesitan permisos especiales
- Controla UIDs (identificadores de usuario)

**Ejemplo:**
```xml
<HASHVALUE name="com.mi.aplicacion">
  <UID name="NONE"/>
</HASHVALUE>
```

**Aplicaciones actuales en el archivo:**
- com.sec.android.easyMover
- com.rsupport.rs.activity.rsupport.aas2

---

### 6. ASKSRNEW.xml - Aplicaciones Restringidas

**Para qué sirve:**
- Lista aplicaciones con acceso limitado
- Restringe funcionalidades específicas

**Cómo agregar restricción:**
```xml
<RESTRICTED>
  <PACKAGE name="nombre.del.paquete">
    <RESTRICTION type="tipo_de_restriccion"/>
  </PACKAGE>
</RESTRICTED>
```

---

### 7. ASKSTS.xml - Almacén de Confianza

**Para qué sirve:**
- Define aplicaciones confiables
- Otorga permisos especiales a apps del sistema

**Configuración actual:**
```xml
<STORE name="PrePackageInstaller">
    <DUMMY value="0"/>
</STORE>
```

**Para agregar nueva app confiable:**
```xml
<STORE name="MiAplicacionConfiable">
    <DUMMY value="0"/>
</STORE>
```

---

### 8. ASKSW.xml - Lista Blanca (Whitelist)

**Para qué sirve:**
- Permite explícitamente ciertas aplicaciones
- Útil cuando se tiene una política estricta de seguridad

**Ejemplo:**
```xml
<HASHVALUE name="hash_de_app_permitida">
    <HASH value="hash_de_firma_1"/>
    <HASH value="hash_de_firma_2"/>
</HASHVALUE>
```

---

### 9. PAICheck.xml - Verificación de Autenticidad

**Para qué sirve:**
- Verificación adicional de paquetes
- Actualmente vacío en esta configuración

**Estado:** Archivo vacío, reservado para uso futuro

---

## 🔓 Cómo Desactivar o Reducir las Protecciones de Seguridad

### ⚠️ ADVERTENCIA CRÍTICA
Desactivar estas protecciones **REDUCE SIGNIFICATIVAMENTE** la seguridad de tu dispositivo. Solo hazlo si entiendes completamente las consecuencias.

### Métodos para Desactivar Protecciones:

#### Método 1: Vaciar las Listas (Más Seguro)
Vaciar los archivos deja la estructura pero sin restricciones activas:

**Para ASKSB.xml (Lista Negra):**
```xml
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<VERSION value="20251228"/>
<LIST>
</LIST>
```

**Para ASKSC.xml, ASKSHB.xml, ASKSRNEW.xml:**
Mantener la misma estructura vacía con solo VERSION y el contenedor principal.

#### Método 2: Eliminar Entradas Específicas
En lugar de vaciar todo, elimina solo las aplicaciones que quieres permitir:

**Ejemplo en ASKSB.xml:**
```xml
<!-- Comentar o eliminar la entrada específica -->
<!-- <HASHVALUE name="hash_de_app_bloqueada">
  <HASH value="ALL"/>
</HASHVALUE> -->
```

#### Método 3: Mover Apps de Lista Negra a Lista Blanca
Si una app está bloqueada en ASKSB.xml, agrégala a ASKSW.xml:

1. Obtén el hash de la aplicación
2. Elimina su entrada de ASKSB.xml
3. Agrégala a ASKSW.xml

#### Método 4: Desactivar ADP (Validación de Integridad)
**MUY PELIGROSO - Puede romper el sistema**

Vaciar ADP.xml elimina la validación de integridad:
```xml
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<VERSION value="20251228"/>
<ADP version="3.1">
</ADP>
```

### 🚨 Consecuencias de Desactivar Protecciones:

| Protección Desactivada | Consecuencias |
|------------------------|---------------|
| **ADP.xml** | - Apps modificadas pueden ejecutarse<br>- Malware no será detectado<br>- Sistema inestable |
| **ASKSB.xml** | - Apps maliciosas conocidas pueden instalarse<br>- Pérdida de protección antimalware |
| **ASKSTS.xml** | - Apps no confiables pueden obtener permisos especiales<br>- Riesgo de escalación de privilegios |
| **ASKSW.xml** | - Política de apps permitidas se desactiva |

### ✅ Recomendación Segura:

En lugar de desactivar completamente, considera:

1. **Modificación Selectiva**: Solo modifica las entradas específicas que necesitas
2. **Lista Blanca Personal**: Usa ASKSW.xml para permitir tus apps personalizadas
3. **Mantén ADP.xml**: Nunca modifiques ADP.xml a menos que sea absolutamente necesario
4. **Actualiza VERSION**: Siempre actualiza el campo VERSION con la fecha actual

### 🛡️ Alternativa: Modo Permisivo

En lugar de desactivar, puedes hacer las listas más permisivas:

**ASKSB.xml - Solo bloquear apps específicas conocidas como malware**
**ASKSW.xml - Agregar todas tus apps confiables**
**ASKSTS.xml - Agregar apps que necesitan permisos especiales**

---

## 🛠️ Cómo Modificar Estos Archivos

### Paso 1: Hacer Copia de Seguridad
```bash
adb pull /system/etc/ADP.xml ADP.xml.backup
adb pull /system/etc/ASKSB.xml ASKSB.xml.backup
adb pull /system/etc/ASKSW.xml ASKSW.xml.backup
# Hacer backup de todos los archivos que vas a modificar
```

### Paso 2: Editar el Archivo
Use un editor de texto que preserve el formato XML

### Paso 3: Validar XML
Asegúrese de que el XML sea válido antes de aplicar cambios
```bash
xmllint --noout archivo.xml
```

### Paso 4: Aplicar Cambios
```bash
adb root
adb remount
adb push ADP.xml /system/etc/
adb reboot
```

---

## 🔑 Obtener Hashes

### Hash de un APK:
```bash
sha256sum aplicacion.apk
```

### Hash del certificado de una APK:
```bash
unzip -p aplicacion.apk META-INF/*.RSA | keytool -printcert | grep SHA256
```

### Con OpenSSL:
```bash
openssl dgst -sha256 aplicacion.apk
```

---

## ⚠️ ADVERTENCIAS IMPORTANTES

### 🔴 Antes de Modificar:

1. **Haga copia de seguridad completa** del sistema
2. **Entienda lo que está haciendo** - cambios incorrectos pueden:
   - Impedir que el teléfono arranque
   - Bloquear aplicaciones del sistema
   - Activar el bit de garantía Knox
3. **Requiere acceso root** para modificar estos archivos
4. **Validez del XML** - el XML debe ser sintácticamente correcto

### 🟡 Consecuencias Posibles:

- ❌ Pérdida de garantía Samsung Knox
- ❌ Algunos servicios de Samsung pueden dejar de funcionar
- ❌ Aplicaciones bancarias pueden detectar modificación
- ❌ Samsung Pay puede dejar de funcionar

### 🟢 Buenas Prácticas:

1. ✅ Siempre hacer backup antes de modificar
2. ✅ Modificar un archivo a la vez
3. ✅ Probar después de cada cambio
4. ✅ Documentar qué cambió
5. ✅ Tener un plan de recuperación

---

## 📱 Compatibilidad

- **Dispositivo:** Samsung Galaxy (serie UN1CA-dm2q)
- **Sistema:** Android con Samsung Knox
- **Versión firmware:** UN1CA-firmware-dm2q
- **Fecha:** 2025-12-28

---

## 🔧 Solución de Problemas

### El teléfono no arranca después de modificar:
1. Arrancar en modo recovery
2. Restaurar desde backup
3. O reflashear el firmware original

### Aplicaciones del sistema no funcionan:
1. Verificar sintaxis XML
2. Revisar hashes - deben ser correctos
3. Verificar que VERSION esté actualizado

### Knox muestra error:
- Los cambios en estos archivos pueden disparar Knox
- Puede ser irreversible
- Considere si realmente necesita los cambios

---

## 📚 Ejemplos Prácticos

### Ejemplo 1: Bloquear una aplicación específica

Editar `ASKSB.xml`:
```xml
<VERSION value="20251228"/>
<LIST>
  <HASHVALUE name="a1b2c3d4e5f6...">
    <HASH value="ALL"/>
  </HASHVALUE>
</LIST>
```

### Ejemplo 2: Permitir una aplicación personalizada

Editar `ASKSW.xml`:
```xml
<VERSION value="20251228"/>
<LIST>
    <HASHVALUE name="mi_app_hash">
        <HASH value="firma_de_mi_app"/>
    </HASHVALUE>
</LIST>
```

### Ejemplo 3: Agregar app confiable

Editar `ASKSTS.xml`:
```xml
<VERSION value="20251228"/>
<TRUSTEDSTORE>
    <STORE name="MiAppConfiable">
        <DUMMY value="0"/>
    </STORE>
</TRUSTEDSTORE>
```

---

## 📞 Recursos Adicionales

- **Documentación Samsung Knox:** https://docs.samsungknox.com/
- **Android Security:** https://source.android.com/security
- **XDA Developers:** Foros de la comunidad para más ayuda

---

## 📝 Notas Finales

Estos archivos son parte crítica del sistema de seguridad de Samsung. Modificarlos sin entender completamente las consecuencias puede resultar en un dispositivo inestable o no funcional.

**Recomendación:** Solo modifique estos archivos si:
- Tiene experiencia con Android y sistemas root
- Comprende XML y hashing
- Tiene un backup completo
- Está preparado para posibles problemas

---

**Creado:** 2025-12-28  
**Versión:** 1.0  
**Autor:** Documentación UN1CA Firmware
