# Nord lab Ethernet addresses

Nord images using NetworkManager with systemd generate two lab DHCP profiles
before NetworkManager starts. Rebuild the image to include this layer's
NetworkManager append. The 32 locally administered addresses to onboard are in
[nord-lab-macs.txt](nord-lab-macs.txt).

The final hexadecimal digit of `/etc/machine-id` selects a slot from 0 to 15.
The addresses are `02:11:22:33:44:XX`, where `XX` is `0x60 + 2 * slot` for
Ethernet 0 and the next value for Ethernet 1. For example, a machine ID ending
in `a` selects slot 10 and addresses ending in `74` and `75`.

The profiles match the physical ports through udev's `ID_PATH`:

| Port | ID_PATH |
|---|---|
| Ethernet 0 | `platform-1a00000.ethernet` |
| Ethernet 1 | `platform-1a80000.ethernet` |

They are written with mode 0600 to
`/run/NetworkManager/system-connections/nord-lab-ethernet{0,1}.nmconnection`.
The systemd `ExecStartPre` hook regenerates them on every NetworkManager start,
including after a reboot. Missing, zero or malformed machine IDs fail the hook.
The profiles use DHCP for IPv4 and automatic IPv6 configuration, and take
autoconnect priority 100 over NetworkManager's usual priority 0 profiles.
An already active connection or an explicitly selected profile is not replaced
by autoconnect priority; select the lab profiles when testing an existing image.

## Check assignments

On each board, inspect the generated profiles and the actual interface addresses:

```sh
cat /run/NetworkManager/system-connections/nord-lab-ethernet*.nmconnection
nmcli -f GENERAL.DEVICE,GENERAL.HWADDR,GENERAL.CONNECTION device show
```

To calculate the assignment without changing networking, run the script with a
separate output directory:

```sh
/usr/libexec/nord-lab-mac /etc/machine-id /etc/nord-lab-mac-slot /tmp/nord-lab-profiles
```

Use `udevadm info /sys/class/net/INTERFACE` to check the physical port's `ID_PATH`.
Only the matching onboard ports use these profiles; USB Ethernet and Wi-Fi do not.

## Collisions and machine identity

The pool contains 16 pairs. Different machine IDs can select the same pair:
with three uniformly distributed IDs the probability is about 18%. Compare
assignments before connecting boards to the lab and whenever another board is
added. There is no automatic collision detection or address reservation.

To resolve a collision, choose an unused slot and store its decimal number
(0 through 15) in `/etc/nord-lab-mac-slot` on that board. For example:

```sh
echo 7 > /etc/nord-lab-mac-slot
```

Reboot from the local console to apply the new pair. Preserve this override and
the board's machine ID across reflashing to retain the assignment. Do not clone
an initialized machine ID across boards. Recheck assignments if the ID changes.
