#!/system/bin/sh
# CSC Verification Script
# Checks current CSC configuration and status

echo "======================================"
echo "CSC Configuration Checker"
echo "======================================"
echo ""

echo "Device Information:"
echo "- Model: $(getprop ro.product.model)"
echo "- Device: $(getprop ro.product.device)"
echo "- Product: $(getprop ro.product.name)"
echo "- Build: $(getprop ro.build.display.id)"
echo "- Android: $(getprop ro.build.version.release)"
echo ""

echo "CSC Properties:"
echo "- ro.csc.sales_code: $(getprop ro.csc.sales_code)"
echo "- ril.sales_code: $(getprop ril.sales_code)"
echo "- persist.sys.csc_code: $(getprop persist.sys.csc_code)"
echo "- ro.csc.country_code: $(getprop ro.csc.country_code)"
echo "- ro.csc.countryiso_code: $(getprop ro.csc.countryiso_code)"
echo ""

echo "Build Properties:"
echo "- ro.product.name: $(getprop ro.product.name)"
echo "- ro.product.locale: $(getprop ro.product.locale)"
echo "- ro.baseband: $(getprop ro.baseband)"
echo ""

# Check if root is available
if [ "$(id -u)" -eq 0 ] || su -c "id" >/dev/null 2>&1; then
    echo "Root Access: Available"
    echo ""
    
    echo "EFS CSC Files (requires root):"
    su -c "
    if [ -f /efs/imei/mps_code.dat ]; then
        echo '- MPS Code: '$(cat /efs/imei/mps_code.dat)
    else
        echo '- MPS Code: File not found'
    fi
    
    if [ -f /efs/imei/sales_code.dat ]; then
        echo '- Sales Code: '$(cat /efs/imei/sales_code.dat)
    else
        echo '- Sales Code: File not found'
    fi
    " 2>/dev/null || echo "- Could not read EFS files"
    echo ""
    
    echo "CSC Related Files:"
    su -c "
    if [ -d /system/csc ]; then
        echo '- Multi-CSC directory exists'
        ls /system/csc/ 2>/dev/null | head -5 | while read csc; do
            echo '  - Available CSC: '$csc
        done
    else
        echo '- No Multi-CSC directory found'
    fi
    
    if [ -d /data/csc ]; then
        echo '- CSC data directory exists'
        echo '  - Files: '$(ls /data/csc/ 2>/dev/null | wc -l)
    else
        echo '- CSC data directory not found'
    fi
    " 2>/dev/null || echo "- Could not check CSC directories"
else
    echo "Root Access: Not available"
    echo "(Some checks require root access)"
fi

echo ""
echo "Network Information:"
echo "- Operator: $(getprop gsm.operator.alpha)"
echo "- MCC/MNC: $(getprop gsm.operator.numeric)"
echo "- SIM State: $(getprop gsm.sim.state)"
echo ""

echo "======================================"
echo "All CSC-related properties:"
echo "======================================"
getprop | grep -i csc
echo ""

echo "======================================"
echo "Verification Complete"
echo "======================================"
