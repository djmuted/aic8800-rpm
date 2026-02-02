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
# Copy the contents of the 'firmware' directory we prepared
cp -r firmware/* %{buildroot}/lib/firmware/aic8800/

# --- Install Driver Source for DKMS ---
mkdir -p %{buildroot}/usr/src/%{name}-%{version}

# Copy everything from current dir (.) to the buildroot
# excluding the 'firmware' dir we just processed and the hidden .git stuff
find . -maxdepth 1 -not -name 'firmware' -not -name '.' -not -name '..' -exec cp -r {} %{buildroot}/usr/src/%{name}-%{version}/ \;

# Create dkms.conf
cat > %{buildroot}/usr/src/%{name}-%{version}/dkms.conf <<EOF
PACKAGE_NAME="%{name}"
PACKAGE_VERSION="%{version}"
BUILT_MODULE_NAME[0]="aic8800_fdrv"
DEST_MODULE_LOCATION[0]="/kernel/drivers/net/wireless"
AUTOINSTALL="yes"
EOF

%files
/usr/src/%{name}-%{version}

%files -n aic8800-firmware
/lib/firmware/aic8800
