SUMMARY = "QPS615 PCIe Ethernet kernel module"
DESCRIPTION = "Kernel module for the QPS615 PCIe Ethernet \
bridge chip. Builds the host driver plus Qualcomm specific platform logic"

LICENSE = "GPL-2.0-only"
LIC_FILES_CHKSUM = "file://${S}/drivers/net/ethernet/toshiba/tc956x/LICENSE;md5=5cecbcf0c040b635e20026c75b838d63"

PV = "6.0.1+git"

inherit module

SRCREV = "b65fb932d5bf6a8008e1f9b068e4a83b6999cb82"

SRC_URI = "\
	git://github.com/TC956X/TC9564_Host_Driver.git;protocol=https;branch=industrial_limited_tested \
	file://0001-net-ethernet-tc956x-Add-Qualcomm-platform-driver-sup.patch \
	file://0002-net-ethernet-tc956x-Makefile-support-cross-build-via.patch \
	file://0003-net-ethernet-tc956x-read-MAC-address-from-DT-NVMEM-o.patch \
	file://0004-net-ethernet-tc956x-Fix-API-changes-for-kernel-6.18-.patch \
	file://0005-net-ethernet-tc956x-Fix-module-auto-loading.patch \
"

#S = "${UNPACKDIR}/source"
B = "${S}/drivers/net/ethernet/toshiba/tc956x"

EXTRA_OEMAKE += "KCFLAGS='-DTC956X -DCONFIG_TC956X_PLATFORM_SUPPORT -DTC956X_SRIOV_PF' pf=1"

FILES:${PN} += "${nonarch_base_libdir}/firmware/TC956X_Firmware_PCIeBridge.bin"
