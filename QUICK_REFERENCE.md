# 🚀 Guía Rápida - Códigos Secretos Samsung Galaxy S23

## ⚡ Códigos Más Usados

| Código | Función | ⚠️ Peligro |
|--------|---------|-----------|
| `*#0*#` | Menú completo de pruebas de hardware | 🟢 Seguro |
| `*#*#4636#*#*` | Información del teléfono y estadísticas | 🟢 Seguro |
| `*#06#` | Ver IMEI del dispositivo | 🟢 Seguro |
| `*#1234#` | Versión de firmware | 🟢 Seguro |
| `*#12580*369#` | Info de hardware y software | 🟢 Seguro |
| `*#9900#` | SysDump / Registro del sistema | 🟡 Cuidado |
| `*#0228#` | Estado de la batería | 🟢 Seguro |
| `*#0011#` | Estado del servicio GSM | 🟢 Seguro |
| `*#7353#` | Menú de prueba rápida | 🟢 Seguro |
| `*#197328640#` | Modo de servicio principal | 🔴 PELIGRO |
| `*2767*3855#` | Reset completo - BORRA TODO | 🔴🔴🔴 PELIGRO |

## 🎯 Leyenda de Peligro

- 🟢 **Seguro**: Solo lectura, no modifica nada
- 🟡 **Cuidado**: Permite cambios, usa con precaución
- 🔴 **Peligro**: Puede causar problemas si se usa mal
- 🔴🔴🔴 **PELIGRO EXTREMO**: PUEDE BORRAR DATOS O DAÑAR EL DISPOSITIVO

## 📱 Apps de Ingeniería en el Firmware

### Aplicaciones Privilegiadas (/system/priv-app/):
1. **ModemServiceMode** - Modo de servicio del módem
2. **SecFactoryPhoneTest** - Pruebas de fábrica
3. **DiagMonAgent95** - Monitoreo de diagnóstico
4. **DeviceDiagnostics** - Diagnóstico del dispositivo
5. **NetworkDiagnostic** - Diagnóstico de red
6. **SEMFactoryApp** - App de fábrica SEM
7. **SmartEpdgTestApp** - Prueba ePDG
8. **FactoryTestProvider** - Proveedor de pruebas

### Aplicaciones del Sistema (/system/app/):
1. **FactoryCameraFB** - Cámara de fábrica
2. **FactoryAirCommandManager** - Air Command de fábrica
3. **UwbTest** - Prueba UWB
4. **WlanTest** - Prueba WLAN

## 🔧 Pruebas Rápidas (Desde *#0*#)

- **Red/Green/Blue** - Prueba de colores
- **Touch** - Prueba táctil
- **Mega Cam** - Cámara trasera
- **Front Cam** - Cámara frontal
- **Sensor** - Todos los sensores
- **Vibration** - Motor de vibración
- **Speaker** - Altavoz
- **LED** - LED de notificación

## 💡 Tips Rápidos

### Para verificar hardware al comprar usado:
```
1. Marca *#0*#
2. Prueba TODOS los componentes
3. Verifica IMEI con *#06#
4. Compara con la caja
```

### Para diagnóstico de señal:
```
1. Marca *#0011#
2. Observa nivel de señal (dBm)
3. -50 dBm = Excelente
4. -100 dBm = Pobre
```

### Para ver salud de la batería:
```
1. Marca *#0228#
2. Verifica ciclos de carga
3. Verifica voltaje y temperatura
```

## ⚠️ REGLAS DE ORO

1. ❌ **NUNCA** cambies bandas de red sin saber qué haces
2. ❌ **NUNCA** actualices firmware desde menús de servicio
3. ❌ **NUNCA** uses códigos de reset sin backup
4. ✅ **SIEMPRE** anota configuraciones antes de cambiar
5. ✅ **SIEMPRE** haz backup antes de experimentar

## 🆘 Si algo sale mal:

```
1. Reinicia el dispositivo
2. Restablece configuración de red
3. Restablecimiento de fábrica (última opción)
```

## 📝 Notas

- **Operador**: Algunos códigos pueden estar bloqueados por tu operador
- **Región**: Algunos códigos varían según la región
- **Firmware**: Algunos códigos solo funcionan en versiones específicas

## 🔗 Más Información

Ver archivo completo: `ENGINEERING_MENUS_GUIDE.md`

---

**Dispositivo**: Samsung Galaxy S23 (SM-S916B / dm2q)
**Firmware**: UN1CA - Build S916BXXS8EYK5
**Android**: 16 (SDK 36)

---

⚠️ **USA BAJO TU PROPIO RIESGO**
