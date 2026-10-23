FILESEXTRAPATHS:prepend := "${THISDIR}/${BPN}:"

SRC_URI:append:nord = " \
    file://nord-lab-mac \
    file://20-nord-lab-mac.conf \
"

PACKAGE_ARCH:nord = "${MACHINE_ARCH}"

do_install:append:nord() {
    if ${@bb.utils.contains('PACKAGECONFIG', 'systemd', 'true', 'false', d)}; then
        install -Dm 0755 ${UNPACKDIR}/nord-lab-mac ${D}${libexecdir}/nord-lab-mac
        install -Dm 0644 ${UNPACKDIR}/20-nord-lab-mac.conf \
            ${D}${systemd_system_unitdir}/NetworkManager.service.d/20-nord-lab-mac.conf
        sed -i 's|@LIBEXECDIR@|${libexecdir}|g' \
            ${D}${systemd_system_unitdir}/NetworkManager.service.d/20-nord-lab-mac.conf
    fi
}
