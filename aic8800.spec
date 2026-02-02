%define debug_package %{nil}

Name:           aic8800-usb-dkms
Version:        1.0.0
Release:        1%{?dist}
Summary:        AIC8800 USB WiFi Driver (DKMS)
License:        GPLv2
URL:            https://github.com/radxa-pkg/aic8800
Source0:        aic8800-source.tar.gz
Source1:        aic8800-firmware.tar.gz

Requires:       dkms
Requires:       aic8800-firmware
BuildArch:      noarch

%description
DKMS driver for AIC8800 USB WiFi adapters (AX900/AX300), based on Radxa patches.

%package -n aic8800-firmware
Summary:        Firmware for AIC8800 WiFi adapters
License:        Proprietary
BuildArch:      noarch
%description -n aic8800-firmware
Firmware files for AIC8800 series chipsets.

%prep
%setup -q -c -n aic8800-source -a 1

%install
# --- Install Firmware ---
mkdir -p %{buildroot}/lib/firmware/aic8800
cp -r firmware/* %{buildroot}/lib/firmware/aic8800/

# --- Install Driver Source for DKMS ---
# Find the USB driver directory. Radxa structure varies, so we find the Makefile for USB.
# Usually: src/USB/driver_fw/driver/aic8800
DRIVER_DIR=$(find . -type d -path "*/USB/driver_fw/driver/aic8800" | head -n 1)

mkdir -p %{buildroot}/usr/src/%{name}-%{version}
cp -r $DRIVER_DIR/* %{buildroot}/usr/src/%{name}-%{version}/

# Copy necessary includes if they are outside the driver dir (common issue with AIC source)
# We copy the whole 'src' to be safe, but structure it so DKMS finds the USB makefile
cp -r src %{buildroot}/usr/src/%{name}-%{version}/src_root

# Create dkms.conf
cat > %{buildroot}/usr/src/%{name}-%{version}/dkms.conf <<EOF
PACKAGE_NAME="%{name}"
PACKAGE_VERSION="%{version}"
BUILT_MODULE_NAME[0]="aic8800_fdrv"
# Point to the USB driver directory relative to where we copied source
MAKE[0]="make -C \${kernel_source_dir} M=\${dkms_source_tree} modules"
DEST_MODULE_LOCATION[0]="/kernel/drivers/net/wireless"
AUTOINSTALL="yes"
EOF

%files
/usr/src/%{name}-%{version}

%files -n aic8800-firmware
/lib/firmware/aic8800
