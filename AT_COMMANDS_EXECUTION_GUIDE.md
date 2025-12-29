# 🔧 Guía Práctica: Ejecución de Comandos AT desde Celular con Root

## 📋 Información General

Esta guía explica cómo ejecutar comandos AT directamente desde un Samsung Galaxy S23 (SM-S916B) con acceso root, utilizando los comandos extraídos del firmware del modem.

**⚠️ ADVERTENCIA CRÍTICA**: Los comandos AT pueden modificar configuraciones permanentes del modem. El uso incorrecto puede causar:
- 🔴 Pérdida de IMEI
- 🔴 Brick del modem
- 🔴 Pérdida de conectividad celular permanente
- 🔴 Invalidación de la garantía

---

## 🛠️ Requisitos Previos

### Hardware y Software
- ✅ Samsung Galaxy S23 (SM-S916B / dm2q)
- ✅ Root habilitado (Magisk recomendado)
- ✅ ADB habilitado
- ✅ Backup completo del dispositivo (EFS, NVRAM, etc.)

### Herramientas Necesarias
```bash
# En PC
- ADB y Fastboot
- Terminal emulator

# En el dispositivo
- Terminal Emulator (Termux recomendado)
- Root File Manager
- Magisk o SuperSU
```

---

## 📡 Comandos AT Extraídos del Modem

### Comandos Propietarios Samsung (130 comandos únicos)

Los siguientes comandos fueron extraídos del firmware del modem (modem.img):

#### Comandos de Prueba y Diagnóstico
```
AT+CPLDUCFG       # Configuración CPLD/FPGA
AT+MSLSECUR       # Seguridad MSL
AT+TESTMODE       # Modo de prueba
AT+GPSSTEST       # Prueba GPS
AT+LIFETIME       # Tiempo de vida del dispositivo
AT+TEMPTEST       # Prueba de temperatura
AT+SIMDETEC       # Detección de SIM
AT+SIMSWITC       # Cambio de SIM
AT+IMEITEST       # Prueba de IMEI
AT+MIPITEST       # Prueba MIPI
AT+OBDMTEST       # Prueba OBDM
AT+CHIPIDTT       # Test de ID de chip
AT+APCHIPTT       # Test de chip AP
```

#### Comandos de Configuración de Red
```
AT+BANSELCT       # Selección de banda
AT+NETMODEC       # Modo de red
AT+CHNSELCT       # Selección de canal
AT+SVCBANDB       # Bandas de servicio
AT+NRPATHCF       # Configuración de path NR (5G)
AT+MODECHAN       # Modo de canal
```

#### Comandos de Seguridad y Bloqueo
```
AT+LVOFLOCK       # Bloqueo LVO
AT+DETALOCK       # Bloqueo de detalles
AT+LOCKREAD       # Lectura de bloqueo
AT+LOCKINFO       # Información de bloqueo
AT+SIMLOCKU       # Bloqueo de SIM
AT+MEIDAUTH       # Autenticación MEID
```

#### Comandos de IMEI y Certificación
```
AT+IMEISIGN       # Firma de IMEI
AT+IMEICERT       # Certificado de IMEI
AT+AKSEEDNO       # Número de semilla AK
```

#### Comandos de Calibración RF
```
AT+READRSSI       # Lectura RSSI
AT+RFBKOFFC       # Offset RF backup
AT+RFMIPITT       # Test MIPI RF
AT+RFEVTAIT       # Test de evento RF
AT+RFNVCHKS       # Checksum NV RF
AT+RFBYCODE       # RF por código
AT+MAXPOWER       # Potencia máxima
AT+SECNRSSI       # RSSI NR secundario
```

#### Comandos de Sistema
```
AT+SYSSLEEP       # Suspensión del sistema
AT+VERSNAME       # Nombre de versión
AT+PRODCODE       # Código de producto
AT+CALIDATE       # Fecha de calibración
AT+SCMMONIT       # Monitor SCM
AT+EFSSYNCC       # Sincronización EFS
AT+TFSTATUS       # Estado TF
AT+FACTORST       # Reset de fábrica
AT+BAKUPCHK       # Verificación de backup
AT+FAILDUMP       # Volcado de fallas
AT+NAMCHECK       # Verificación NAM
AT+PRLVERIF       # Verificación PRL
AT+RECONDIT       # Reacondicionamiento
AT+FACTOLOG       # Log de fábrica
```

#### Comandos de Hardware
```
AT+GRIPSENS       # Sensor de agarre
AT+HWINDICK       # Indicador de viento de hardware
AT+ACLTESTT       # Test ACL
AT+ASDIVTES       # Test de diversidad de antena
AT+HOPATHCK       # Verificación de path HO
AT+RTSARCHK       # Verificación de búsqueda RTS
AT+CPSTACHK       # Verificación de estado CP
AT+SSUCONFG       # Configuración SSU
```

#### Comandos de Provisión
```
AT+BLOBSIGN       # Firma de blob
AT+PROVCASS       # Cassette de provisión
AT+KSTRINGB       # String B de clave
AT+PARALLEL       # Modo paralelo
AT+LDUSTCHK       # Verificación de polvo LD
AT+AOTKEYWR       # Escritura de clave AOT
```

#### Comandos Estándar 3GPP
```
AT+CFUN           # Funcionalidad del teléfono
AT+COPS           # Selección de operador
AT+CPIN           # Verificación de PIN
AT+CLCK           # Facility lock
AT+CCFC           # Call forwarding
AT+CCWA           # Call waiting
AT+CHLD           # Call hold
AT+CHUP           # Colgar llamada
AT+CLCC           # Lista de llamadas actuales
AT+CGATT          # GPRS attach/detach
AT+CGACT          # Activar contexto PDP
AT+CGDATA         # Entrada de datos
AT+CGDCONT        # Definir contexto PDP
AT+CGDSCONT       # Definir contexto PDP secundario
AT+CGTFT          # Traffic Flow Template
AT+CGEQREQ        # Calidad de servicio requerida
AT+CGEQMIN        # Calidad de servicio mínima
AT+CGEQOS         # Calidad de servicio
AT+CGCMOD         # Modificar contexto PDP
AT+CMEE           # Reporte de errores
AT+CMER           # Event reporting
AT+CMOD           # Modo de llamada
AT+CDV            # Dial voice call
AT+CEER           # Razón de error extendida
AT+CEMODE         # Modo CE
AT+CMGF           # Formato de mensaje
AT+CMGS           # Enviar SMS
AT+CMGW           # Escribir SMS
AT+CMGD           # Borrar SMS
AT+CMSS           # Enviar SMS almacenado
AT+CPMS           # Almacenamiento de mensajes preferido
AT+CPWD           # Cambiar password
AT+CNMPSD         # Network Management PSD
AT+CMEC           # Mobile Equipment Control
```

---

## 🔌 Métodos de Ejecución de Comandos AT

### Método 1: Via ADB desde PC (Recomendado para Principiantes)

Este es el método más seguro porque puedes ver los resultados en tiempo real.

```bash
# 1. Conectar el dispositivo
adb devices

# 2. Obtener shell root
adb shell
su

# 3. Verificar que el socket RIL existe
ls -la /dev/socket/rild

# 4. Enviar comando AT simple
echo -e "AT\r\n" | nc -U /dev/socket/rild

# 5. Enviar comandos AT específicos
# Ejemplo: Verificar funcionalidad
echo -e "AT+CFUN?\r\n" | nc -U /dev/socket/rild

# Ejemplo: Obtener info de operador
echo -e "AT+COPS?\r\n" | nc -U /dev/socket/rild

# Ejemplo: Verificar estado de red
echo -e "AT+CREG?\r\n" | nc -U /dev/socket/rild
```

**Salida esperada**:
```
+CFUN: 1
OK
```

### Método 2: Script Automatizado ADB

Crea este script en tu PC:

```bash
#!/bin/bash
# at_command.sh - Script para enviar comandos AT

if [ -z "$1" ]; then
    echo "Uso: $0 <comando_AT>"
    echo "Ejemplo: $0 'AT+COPS?'"
    exit 1
fi

COMMAND="$1"

# Enviar comando via ADB
adb shell su -c "echo -e '${COMMAND}\r\n' | nc -U /dev/socket/rild" 2>&1

echo ""
echo "Comando enviado: $COMMAND"
```

**Uso**:
```bash
chmod +x at_command.sh
./at_command.sh "AT+CFUN?"
./at_command.sh "AT+COPS?"
./at_command.sh "AT+CPIN?"
```

### Método 3: Directamente en el Dispositivo (Termux)

```bash
# 1. Instalar Termux desde F-Droid
# 2. Instalar paquetes necesarios
pkg install root-repo
pkg install tsu
pkg install netcat-openbsd

# 3. Obtener root
tsu

# 4. Enviar comandos AT
echo -e "AT+CFUN?\r\n" | nc -U /dev/socket/rild

# 5. Crear alias para facilitar
alias atcmd='echo -e'
alias sendat='nc -U /dev/socket/rild'

# Uso del alias
atcmd "AT+COPS?\r\n" | sendat
```

### Método 4: Script Bash en el Dispositivo

Crea este archivo en `/data/local/tmp/at_sender.sh`:

```bash
#!/system/bin/sh
# at_sender.sh - Enviar comandos AT desde el dispositivo

if [ -z "$1" ]; then
    echo "Uso: at_sender.sh <comando>"
    echo "Ejemplo: at_sender.sh 'AT+CFUN?'"
    exit 1
fi

SOCKET="/dev/socket/rild"
CMD="$1"

if [ ! -S "$SOCKET" ]; then
    echo "Error: Socket RIL no encontrado en $SOCKET"
    exit 1
fi

echo "Enviando: $CMD"
echo -e "${CMD}\r\n" | nc -U $SOCKET 2>&1

if [ $? -eq 0 ]; then
    echo "Comando enviado exitosamente"
else
    echo "Error al enviar comando"
fi
```

**Instalación y uso**:
```bash
# Subir el script
adb push at_sender.sh /data/local/tmp/
adb shell su -c "chmod +x /data/local/tmp/at_sender.sh"

# Ejecutar
adb shell su -c "/data/local/tmp/at_sender.sh 'AT+CFUN?'"
```

### Método 5: Aplicación Android con Root

```java
// ATCommandSender.java
import android.os.SystemProperties;
import java.io.*;
import java.net.Socket;
import android.net.LocalSocket;
import android.net.LocalSocketAddress;

public class ATCommandSender {
    
    private static final String SOCKET_NAME = "rild";
    
    public static String sendATCommand(String command) {
        LocalSocket socket = null;
        try {
            // Conectar al socket RIL
            socket = new LocalSocket();
            LocalSocketAddress address = new LocalSocketAddress(
                SOCKET_NAME,
                LocalSocketAddress.Namespace.RESERVED
            );
            socket.connect(address);
            
            // Enviar comando
            OutputStream os = socket.getOutputStream();
            String cmdWithCRLF = command + "\r\n";
            os.write(cmdWithCRLF.getBytes());
            os.flush();
            
            // Leer respuesta
            InputStream is = socket.getInputStream();
            BufferedReader reader = new BufferedReader(
                new InputStreamReader(is)
            );
            
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line).append("\n");
                if (line.equals("OK") || line.equals("ERROR")) {
                    break;
                }
            }
            
            return response.toString();
            
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        } finally {
            try {
                if (socket != null) socket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    
    // Método de prueba
    public static void main(String[] args) {
        String[] testCommands = {
            "AT",
            "AT+CFUN?",
            "AT+COPS?",
            "AT+CPIN?"
        };
        
        for (String cmd : testCommands) {
            System.out.println("Comando: " + cmd);
            String response = sendATCommand(cmd);
            System.out.println("Respuesta: " + response);
            System.out.println("---");
        }
    }
}
```

**AndroidManifest.xml** (permisos necesarios):
```xml
<uses-permission android:name="android.permission.MODIFY_PHONE_STATE" />
<uses-permission android:name="android.permission.READ_PHONE_STATE" />
<uses-permission android:name="android.permission.READ_PRIVILEGED_PHONE_STATE" />
```

### Método 6: Código Nativo (C/C++)

```c
// at_command_native.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#define SOCKET_PATH "/dev/socket/rild"
#define BUFFER_SIZE 4096

int send_at_command(const char *command) {
    int sock;
    struct sockaddr_un addr;
    char buffer[BUFFER_SIZE];
    int bytes_read;
    
    // Crear socket
    sock = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("socket");
        return -1;
    }
    
    // Configurar dirección
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCKET_PATH, sizeof(addr.sun_path) - 1);
    
    // Conectar
    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("connect");
        close(sock);
        return -1;
    }
    
    // Preparar comando con CRLF
    char cmd_with_crlf[256];
    snprintf(cmd_with_crlf, sizeof(cmd_with_crlf), "%s\r\n", command);
    
    // Enviar comando
    if (write(sock, cmd_with_crlf, strlen(cmd_with_crlf)) < 0) {
        perror("write");
        close(sock);
        return -1;
    }
    
    printf("Comando enviado: %s\n", command);
    
    // Leer respuesta
    memset(buffer, 0, sizeof(buffer));
    bytes_read = read(sock, buffer, sizeof(buffer) - 1);
    
    if (bytes_read > 0) {
        printf("Respuesta:\n%s\n", buffer);
    } else if (bytes_read < 0) {
        perror("read");
    }
    
    close(sock);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Uso: %s <comando_AT>\n", argv[0]);
        printf("Ejemplo: %s 'AT+CFUN?'\n", argv[0]);
        return 1;
    }
    
    return send_at_command(argv[1]);
}
```

**Compilación y uso**:
```bash
# Compilar para Android
aarch64-linux-android-gcc -o at_command at_command_native.c

# Subir al dispositivo
adb push at_command /data/local/tmp/
adb shell su -c "chmod +x /data/local/tmp/at_command"

# Ejecutar
adb shell su -c "/data/local/tmp/at_command 'AT+CFUN?'"
```

---

## 🔍 Ejemplos Prácticos de Comandos

### Comandos de Información (Seguros)

```bash
# Verificar funcionalidad del modem
echo -e "AT+CFUN?\r\n" | nc -U /dev/socket/rild
# Respuesta esperada: +CFUN: 1

# Obtener operador de red
echo -e "AT+COPS?\r\n" | nc -U /dev/socket/rild
# Respuesta: +COPS: 0,0,"Operador",7

# Estado de registro
echo -e "AT+CREG?\r\n" | nc -U /dev/socket/rild
# Respuesta: +CREG: 0,1

# Calidad de señal
echo -e "AT+CSQ\r\n" | nc -U /dev/socket/rild
# Respuesta: +CSQ: 25,99

# Estado del PIN
echo -e "AT+CPIN?\r\n" | nc -U /dev/socket/rild
# Respuesta: +CPIN: READY
```

### Comandos de Prueba (Usar con Precaución)

```bash
# Modo de prueba
echo -e "AT+TESTMODE?\r\n" | nc -U /dev/socket/rild

# Lectura de RSSI
echo -e "AT+READRSSI?\r\n" | nc -U /dev/socket/rild

# Test de temperatura
echo -e "AT+TEMPTEST\r\n" | nc -U /dev/socket/rild

# Detección de SIM
echo -e "AT+SIMDETEC?\r\n" | nc -U /dev/socket/rild

# Estado de GPS
echo -e "AT+GPSSTEST?\r\n" | nc -U /dev/socket/rild
```

### Comandos de Configuración (⚠️ PELIGROSOS)

```bash
# ⚠️ NO EJECUTAR sin entender completamente

# Cambiar modo de funcionalidad
# 0 = Mínimo, 1 = Completo, 4 = Deshabilitar RF
echo -e "AT+CFUN=1\r\n" | nc -U /dev/socket/rild

# Seleccionar banda (EJEMPLO - no ejecutar sin saber)
# echo -e "AT+BANSELCT=...\r\n" | nc -U /dev/socket/rild

# Configuración de red (EJEMPLO - no ejecutar)
# echo -e "AT+NETMODEC=...\r\n" | nc -U /dev/socket/rild
```

---

## 🛡️ Precauciones y Mejores Prácticas

### Antes de Ejecutar Comandos AT

1. **✅ Backup Completo**
```bash
# Backup de EFS (CRÍTICO)
adb shell su -c "dd if=/dev/block/by-name/efs of=/sdcard/efs.img"
adb pull /sdcard/efs.img

# Backup de modem
adb shell su -c "dd if=/dev/block/by-name/modem of=/sdcard/modem.img"
adb pull /sdcard/modem.img

# Backup de NVRAM
adb shell su -c "dd if=/dev/block/by-name/nvram of=/sdcard/nvram.img"
adb pull /sdcard/nvram.img
```

2. **✅ Documentar Todo**
```bash
# Guardar log de comandos
echo "$(date): AT+CFUN?" >> at_commands_log.txt
```

3. **✅ Verificar Permisos**
```bash
# Verificar que tienes acceso al socket
adb shell su -c "ls -la /dev/socket/rild"
# Debería mostrar: srw-rw---- radio radio
```

### Durante la Ejecución

- ⚠️ Ejecuta UN comando a la vez
- ⚠️ Espera la respuesta completa antes del siguiente
- ⚠️ Anota cada respuesta recibida
- ⚠️ Si recibes ERROR, detente inmediatamente

### Comandos que NUNCA Debes Ejecutar

```bash
# ❌ NUNCA ejecutes estos sin conocimiento experto:
AT+IMEISIGN=...      # Puede corromper IMEI
AT+FACTORST          # Reset de fábrica del modem
AT+LVOFLOCK=...      # Puede bloquear el dispositivo
AT+DETALOCK=...      # Bloqueo permanente
```

---

## 🔧 Troubleshooting

### Error: "nc: No such file or directory"

```bash
# Instalar netcat
adb shell su -c "pm install /system/app/busybox.apk"
# O usar busybox nc
adb shell su -c "busybox nc -U /dev/socket/rild"
```

### Error: "Permission denied"

```bash
# Verificar root
adb shell su -c "id"
# Debería mostrar: uid=0(root)

# Verificar permisos del socket
adb shell su -c "chmod 666 /dev/socket/rild"  # temporal
```

### No Recibo Respuesta

```bash
# Verificar que rild está corriendo
adb shell su -c "ps -A | grep rild"

# Reiniciar servicio RIL (puede causar pérdida temporal de señal)
adb shell su -c "killall rild"
# El sistema lo reiniciará automáticamente
```

### Respuesta: "ERROR"

```bash
# El comando no es soportado o tiene sintaxis incorrecta
# Verificar sintaxis exacta del comando
# Algunos comandos requieren parámetros específicos
```

---

## 📊 Monitoreo de Comandos AT

### Capturar todos los Comandos AT del Sistema

```bash
# Método 1: logcat filtrado
adb logcat -s RILJ:V RIL:V | grep -i "at+"

# Método 2: strace del proceso rild
adb shell su -c "strace -p $(pidof rild) -s 1024 -o /sdcard/rild_trace.txt"

# Método 3: tcpdump del socket
adb shell su -c "tcpdump -i any -s 0 -w /sdcard/ril_traffic.pcap"
```

### Analizar Logs

```bash
# Descargar y analizar
adb pull /sdcard/rild_trace.txt
grep "AT+" rild_trace.txt | sort | uniq
```

---

## 📚 Recursos Adicionales

### Documentación de Referencia

- **3GPP TS 27.007**: AT Command Set for User Equipment
- **3GPP TS 27.005**: SMS AT Commands
- **Qualcomm AT Commands**: (requiere NDA)

### Herramientas Útiles

```bash
# Terminal emulator con root
- Termux
- ConnectBot
- JuiceSSH

# Aplicaciones de diagnóstico
- Network Signal Guru (requiere root para AT commands)
- Cellular-Z
- NetMonitor
```

---

## ⚖️ Disclaimer Legal

Esta guía se proporciona **ÚNICAMENTE CON FINES EDUCATIVOS**.

**NO ME HAGO RESPONSABLE DE**:
- 🔴 Daños al dispositivo
- 🔴 Pérdida de IMEI
- 🔴 Pérdida de conectividad
- 🔴 Brick del modem
- 🔴 Pérdida de garantía
- 🔴 Violación de términos de servicio del operador
- 🔴 Problemas legales derivados del mal uso

**USA BAJO TU PROPIO RIESGO**

---

## 📝 Conclusión

Los comandos AT son una herramienta poderosa para diagnóstico y configuración avanzada del modem, pero deben usarse con extrema precaución. 

**Recomendaciones finales**:
1. ✅ Siempre haz backup de EFS/NVRAM
2. ✅ Documenta cada comando ejecutado
3. ✅ Comienza con comandos de solo lectura (?)
4. ✅ Nunca uses comandos que no entiendes
5. ✅ Mantén una copia del firmware de stock para restauración

---

**Firmware analizado**: UN1CA (SM-S916B / dm2q)  
**Comandos AT extraídos**: 130+ únicos del modem  
**Versión de la guía**: 1.0 - Diciembre 2024  

---

*Esta guía fue creada mediante análisis del firmware del modem y es solo para propósitos educativos y de investigación.*
