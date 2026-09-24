# Temporary override for Nord SoC bring-up.
# Nord kernel support is available in the 'qcom-next' branch with
# tag: qcom-next-7.3-rc2-20260921, but we can't move to this tag
# globally yet due to test failures on other SoCs.
# To work around this, only use this tag for Nord. Drop this file once
# all SoCs are functional against a single 'qcom-next' tag.

# tag: qcom-next-7.3-rc2-20260921
LINUX_VERSION:nord = "7.2+7.3-rc2+nord"
SRCREV:nord = "8f69c5810aa30bfa58bf58256fed38e666b231c2"

# DTB files specified in the nord compatibles only exist in
# the 'qcom-next' tag used by Nord, not in the default SRCREV that
# yocto-check-layer builds against.  Backport the two board DTS 
# files, so the default kernel source tree has them too.
SRC_URI:append = " \
    file://0001-FROMLIST-arm64-dts-qcom-Add-initial-support-for-Nord.patch \
    file://0002-FROMLIST-arm64-dts-qcom-Add-device-tree-for-Nord-RRD.patch \
    file://0001-FROMLIST-dt-bindings-clock-qcom-Add-EMAC-CNOC-APB-cl.patch \
    file://0002-FROMLIST-clk-qcom-segcc-nord-Add-EMAC-CNOC-APB-clock.patch \
    file://0003-FROMLIST-dt-bindings-phy-qcom-sa8775p-dwmac-sgmii-ph.patch \
    file://0004-FROMLIST-phy-qcom-sgmii-eth-prepare-for-additional-P.patch \
    file://0005-FROMLIST-phy-qcom-sgmii-eth-add-Nord-USXGMII-support.patch \
    file://0006-FROMLIST-dt-bindings-net-pcs-add-Qualcomm-Nord-XPCS.patch \
    file://0007-FROMLIST-net-pcs-xpcs-add-USXGMII-Clause-37-autoneg-.patch \
    file://0008-FROMLIST-net-pcs-xpcs-add-custom-platform-register-a.patch \
    file://0009-FROMLIST-net-pcs-xpcs-add-Qualcomm-Nord-platform-sup.patch \
    file://0010-FROMLIST-net-pcs-xpcs-initialize-runtime-PM-as-suspe.patch \
    file://0011-FROMLIST-net-stmmac-Add-DW25GMAC-support-in-stmmac-c.patch \
    file://0012-FROMLIST-net-stmmac-Integrate-dw25gmac-into-hwif-han.patch \
    file://0013-FROMLIST-dt-bindings-net-qcom-ethqos-add-Qualcomm-No.patch \
    file://0014-FROMLIST-net-stmmac-support-custom-XGMAC-register-la.patch \
    file://0015-FROMLIST-net-stmmac-qcom-ethqos-support-external-PCS.patch \
    file://0016-FROMLIST-net-stmmac-add-Qualcomm-Nord-ETHQOS-support.patch \
    file://0017-PENDING-net-stmmac-QCOM-DW25GMAC-fixes.patch \
    file://0018-PENDING-arm64-dts-qcom-add-Ethernet-support-for-Nord.patch \
"
# Drop the above backports for Nord itself as Nord SRCREV/tag above already
# carries these two commits, so re-applying them would fail.
SRC_URI:remove:nord = "file://0001-FROMLIST-arm64-dts-qcom-Add-initial-support-for-Nord.patch"
SRC_URI:remove:nord = "file://0002-FROMLIST-arm64-dts-qcom-Add-device-tree-for-Nord-RRD.patch"
