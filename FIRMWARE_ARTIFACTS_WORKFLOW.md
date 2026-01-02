# Firmware Artifacts Upload Workflow

## Overview

This document describes the GitHub Actions workflow that automatically uploads firmware artifacts from the UN1CA-firmware-dm2q repository. The workflow collects specific directories from the system, vendor, recovery, and vendor_boot partitions and creates a comprehensive artifact package.

## Workflow File

**Location**: `.github/workflows/upload-firmware-artifacts.yml`

## Trigger Conditions

The workflow is triggered by:

1. **Manual Dispatch**: Can be triggered manually from the GitHub Actions tab
2. **Push Events**: Automatically runs when changes are pushed to the `main` branch in any of the monitored directories
3. **Pull Request Events**: Runs when pull requests modify any of the monitored directories

### Monitored Directories

- `system/system/bin/**`
- `system/system/lib/**`
- `system/system/lib64/**`
- `system/system/etc/**`
- `vendor/bin/**`
- `vendor/lib/**`
- `vendor/lib64/**`
- `vendor/etc/**`
- `vendor/firmware/**`
- `recovery/**`
- `vendor_boot/**`

## Artifact Contents

The workflow creates a comprehensive package containing:

### System Partition Files

#### system/system/bin/
- **Description**: System binaries and executables
- **Contents**: 
  - Core Android system daemons and services
  - System utilities and tools
  - Shell commands and applications
  - Package manager tools
  - Network utilities
  - Debugging tools

#### system/system/lib/ (32-bit)
- **Description**: System libraries for 32-bit architecture
- **Contents**:
  - Android framework libraries
  - System services libraries
  - Hardware abstraction layer (HAL) libraries
  - Codec and media processing libraries
  - Graphics and rendering libraries
  - Audio processing libraries

#### system/system/lib64/ (64-bit)
- **Description**: System libraries for 64-bit architecture
- **Contents**: Same categories as lib/ but compiled for ARM64 architecture

#### system/system/etc/
- **Description**: System configuration files
- **Contents**:
  - System property files
  - Init scripts and service definitions (.rc files)
  - Permission and feature declarations (.xml files)
  - VINTF manifests
  - Certificates and security policies
  - Audio, camera, and media configuration
  - Network and connectivity settings

### Vendor Partition Files

#### vendor/bin/
- **Description**: Vendor-specific binaries and executables
- **Contents**:
  - Hardware-specific daemons and services
  - Vendor HAL implementations
  - Qualcomm proprietary services
  - Samsung proprietary services
  - Camera, audio, and graphics servers

#### vendor/lib/ (32-bit)
- **Description**: Vendor libraries for 32-bit architecture
- **Contents**:
  - Hardware-specific libraries
  - Vendor HAL implementations
  - Qualcomm and Samsung proprietary libraries
  - Camera, audio, graphics, and sensor libraries
  - Codec implementations
  - Security and DRM libraries

#### vendor/lib64/ (64-bit)
- **Description**: Vendor libraries for 64-bit architecture
- **Contents**: Same categories as vendor/lib/ but compiled for ARM64 architecture

#### vendor/etc/
- **Description**: Vendor configuration files
- **Contents**:
  - Hardware-specific configuration
  - HAL service definitions (.rc files)
  - VINTF manifests for vendor services
  - Calibration and tuning files
  - Sensor configuration
  - Camera ISP tuning data
  - Audio DSP configuration

#### vendor/firmware/
- **Description**: Binary firmware files for hardware components
- **Contents**:
  - Camera ISP firmware
  - Audio DSP firmware
  - Modem firmware
  - GPU firmware
  - Sensor hub firmware
  - Bluetooth and WiFi firmware
  - Security processor firmware
  - Qualcomm subsystem firmware

### Recovery Partition

#### recovery/
- **Description**: Recovery partition files
- **Contents**:
  - Recovery kernel (`kernel`) - Used for system recovery and updates
  - Device tree blobs (`dtb`, `dtb.0-3`) - Hardware configuration
  - Device tree source files (`*.dts`, `*.dts.yaml`)
  - Kernel configuration (`kernel_configs.txt`)
  - Kernel version information
  - AVB verification data (`recovery.avb.json`)
  - Recovery root filesystem (if present)

### Vendor Boot Partition

#### vendor_boot/
- **Description**: Vendor boot partition files
- **Contents**:
  - Device tree blobs (`dtb`, `dtb.0-3`)
  - Device tree source files (`*.dts`, `*.dts.yaml`)
  - Boot configuration (`bootconfig`)
  - Vendor ramdisk (`root.1/`) containing:
    - Kernel modules (`.ko` files)
    - Vendor firmware
    - Init scripts
    - Device-specific files
  - AVB verification data (`vendor_boot.avb.json`)
  - Metadata files (`vendor_boot.json`)

## Workflow Steps

### 1. Checkout Repository
Uses `actions/checkout@v4` to clone the repository.

### 2. Create Directory Structure
Creates the artifact output directory structure mirroring the source layout.

### 3. Copy Files
Individual steps for each directory:
- Copies all files from source to artifact output
- Counts and reports the number of files copied
- Handles missing directories gracefully
- Preserves directory structure

### 4. Create Documentation
Generates a comprehensive `README.md` inside the artifact package with:
- Package overview
- Directory structure
- Technical specifications
- Usage notes
- File type descriptions

### 5. Generate Manifest
Creates `MANIFEST.txt` containing:
- Complete list of all files in the package
- File count statistics per directory
- Total package size

### 6. Create Release ZIP
Compresses the artifact package into a ZIP file with maximum compression (level 9).

### 7. Create GitHub Release
Creates a new GitHub release with:
- Timestamp-based tag (e.g., `firmware-artifacts-v20240102-143000`)
- Comprehensive release notes
- Technical specifications
- Package contents overview

### 8. Upload ZIP to Release
Attaches the compressed ZIP file to the GitHub release.

### 9. Upload Artifacts
Uploads the artifact package to GitHub Actions artifacts with:
- Name: `firmware-artifacts-{commit_sha}`
- Retention: 90 days
- Compression level: 9 (maximum)

### 10. Create Summary
Generates a workflow summary showing:
- File counts per directory
- Total package size
- Directory structure
- Key features included

## Output Artifacts

### GitHub Actions Artifact
- **Name**: `firmware-artifacts-{commit_sha}`
- **Retention**: 90 days
- **Access**: Available in the workflow run's artifacts section

### GitHub Release
- **Tag**: `firmware-artifacts-v{timestamp}`
- **File**: `firmware-artifacts-dm2q-{commit_sha}.zip`
- **Contents**: Same as the GitHub Actions artifact but permanently available

### Package Structure

```
artifact_output/
├── README.md              # Package documentation
├── MANIFEST.txt           # Complete file listing
├── system/
│   └── system/
│       ├── bin/          # System binaries (400+ files)
│       ├── lib/          # 32-bit system libraries (2000+ files)
│       ├── lib64/        # 64-bit system libraries (3000+ files)
│       └── etc/          # System configuration (1000+ files)
├── vendor/
│   ├── bin/              # Vendor binaries (200+ files)
│   ├── lib/              # 32-bit vendor libraries (3000+ files)
│   ├── lib64/            # 64-bit vendor libraries (4000+ files)
│   ├── etc/              # Vendor configuration (500+ files)
│   └── firmware/         # Firmware files (1000+ files)
├── recovery/             # Recovery files (20+ files)
└── vendor_boot/          # Vendor boot files (20+ files)
```

## Technical Specifications

### Device Information
- **Device**: Samsung Galaxy S21 FE 5G
- **Codename**: DM2Q
- **Chipset**: Qualcomm Snapdragon 888 (SM8350)
- **Architecture**: ARM64 (aarch64)

### File Statistics (Approximate)
- **Total Files**: 14,000+
- **Total Size**: Several GB (compressed to ~2-3 GB)
- **Binary Executables**: 600+
- **Shared Libraries**: 9,000+
- **Configuration Files**: 1,500+
- **Firmware Files**: 1,000+
- **Device Trees**: 8 (4 DTB files with source and YAML)

### Supported HAL Versions
- Camera HAL: 1.0, 2.x, 3.x
- Audio HAL: 2.0, 4.0, 5.0, 6.0, 7.0
- Graphics HAL: 2.0, 3.0, 4.0
- Sensors HAL: 1.0, 2.0
- And many more...

## Usage Instructions

### Accessing the Artifacts

#### Via GitHub Actions
1. Go to the repository's "Actions" tab
2. Select the workflow run
3. Scroll to the "Artifacts" section at the bottom
4. Download `firmware-artifacts-{commit_sha}`

#### Via GitHub Releases
1. Go to the repository's "Releases" page
2. Find the release with tag `firmware-artifacts-v{timestamp}`
3. Download `firmware-artifacts-dm2q-{commit_sha}.zip`

### Extracting the Package

```bash
# Download the ZIP file
wget https://github.com/extremerom/UN1CA-firmware-dm2q/releases/download/{tag}/firmware-artifacts-dm2q-{sha}.zip

# Extract the package
unzip firmware-artifacts-dm2q-{sha}.zip -d firmware-artifacts/

# View the README
cat firmware-artifacts/README.md

# View the manifest
cat firmware-artifacts/MANIFEST.txt
```

### Using the Files

#### For ROM Development
- Use system and vendor libraries for building custom ROMs
- Reference configuration files for proper device setup
- Include firmware files in ROM packages

#### For Recovery Development
- Use recovery kernel and device trees
- Reference recovery configuration

#### For Kernel Development
- Use device tree source files
- Reference kernel configuration
- Include vendor boot components

#### For Application Development
- Reference system libraries for dependency information
- Check HAL versions for compatibility
- Review configuration files for feature support

## Important Notes

### File Permissions
When using these files, ensure proper permissions are set:
- Binaries: `0755` (rwxr-xr-x)
- Libraries: `0644` (rw-r--r--)
- Configuration: `0644` (rw-r--r--)
- Firmware: `0644` (rw-r--r--)

### SELinux Contexts
Files from the vendor partition may require specific SELinux contexts. Refer to the original partition's `file_contexts` file.

### Dependencies
- Libraries and binaries are compiled for ARM64 architecture
- Some files may have dependencies on specific kernel versions
- System libraries may depend on other system libraries
- Vendor libraries may depend on proprietary Qualcomm components

### Compatibility
- Files are extracted from official Samsung firmware
- May not be compatible with other devices or Android versions
- Vendor files are specific to Snapdragon 888 (SM8350)
- Some components require Samsung's OneUI framework

## Maintenance

### Updating the Workflow

To modify what gets included in the artifact:

1. Edit `.github/workflows/upload-firmware-artifacts.yml`
2. Add or remove copy steps as needed
3. Update the documentation in the workflow
4. Test the workflow with a manual dispatch

### Adding New Directories

To include additional directories:

1. Add the path to the `paths` trigger configuration
2. Create a new copy step in the workflow
3. Update the directory structure creation step
4. Update the documentation

### Modifying Retention

To change how long artifacts are kept:

```yaml
- name: Upload firmware artifacts
  uses: actions/upload-artifact@v4
  with:
    retention-days: 90  # Change this value (1-400 days)
```

## Troubleshooting

### Workflow Not Triggering

**Problem**: Workflow doesn't run after pushing changes.

**Solution**:
- Ensure changes are in monitored directories
- Check that branch is `main`
- Verify workflow file syntax with yamllint
- Check GitHub Actions is enabled for the repository

### Missing Files in Artifact

**Problem**: Some expected files are not in the artifact.

**Solution**:
- Check if files exist in the repository
- Verify the copy commands include the correct paths
- Check for permission issues
- Review workflow logs for error messages

### Artifact Too Large

**Problem**: Artifact exceeds GitHub's size limits.

**Solution**:
- Split into multiple artifacts
- Increase compression level (already at maximum)
- Exclude large unnecessary files
- Use GitHub Releases for large packages

### Release Creation Fails

**Problem**: GitHub Release creation step fails.

**Solution**:
- Check `GITHUB_TOKEN` permissions
- Verify no release with same tag exists
- Check repository settings allow releases
- Review error messages in workflow logs

## Related Workflows

This repository includes several other artifact upload workflows:

- **upload-camera-artifacts.yml**: Camera-specific files
- **upload-device-tree-files.yml**: Device tree files from external repository
- **upload-engineering-artifacts.yml**: Engineering and debugging files
- **upload-factory-apps-artifacts.yml**: Factory testing applications
- **upload-fota-agent-artifacts.yml**: FOTA (Firmware Over The Air) components

## Contributing

To improve this workflow:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request with a clear description

## License

This workflow and documentation are part of the UN1CA-firmware-dm2q repository. The firmware files themselves are proprietary to Samsung and Qualcomm.

## Support

For issues or questions:
- Open an issue in the GitHub repository
- Check existing workflow runs for examples
- Review the workflow logs for error messages
- Consult GitHub Actions documentation

## Version History

- **v1.0** (2024-01-02): Initial release
  - Support for system partition directories
  - Support for vendor partition directories
  - Support for recovery and vendor_boot partitions
  - Automatic GitHub Release creation
  - Comprehensive documentation
