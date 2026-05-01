# AWS VPN (with SystemD)

_SystemD units and helper scripts to manage AWS Client VPN connections using
SystemD, instead of the Amazon GUI._

## Pre-requisites

* Linux with SystemD
* BASH 4+
* `socat`
* `grep`, `sed`, `awk` and other basic utilities

## Installation

Packages are built using Docker — no distro-specific toolchain needs to be
installed locally. Built packages are written to `dist/`.

**Arch Linux:**
```
$ make pkg
$ pacman -U dist/aws-vpn-systemd-*.pkg.tar.zst
```

**Ubuntu / Debian:**
```
$ make deb
$ apt install ./dist/aws-vpn-systemd_*.deb
```

**Fedora / Red Hat:**
```
$ make rpm
$ dnf install dist/x86_64/aws-vpn-systemd-*.rpm
```

Each target compiles a patched OpenVPN binary from the latest OpenVPN 2.x
release and packages it alongside the SystemD units and helper scripts. The
patched build is required because AWS Client VPN uses the OpenVPN management
interface to carry SAML assertions, which can be up to 128 KB — far larger
than stock OpenVPN's 128-byte limit.

## Assumptions

* The `openvpn` user exists, and the VPN should run as this user.
* The `network` group exists, and members of this group may manage VPN connections.
* AWS VPN configuration files are stored in `/etc/openvpn/client/<instance>.conf`,
  where `<instance>` is the hostname of your VPN.
* DNS is managed by `systemd-resolved`.

## Usage

Replace `<instance>` with the hostname of your VPN. Multiple VPNs may be
configured by repeating these steps for each one.

Place the configuration file for your VPN in `/etc/openvpn/client/<instance>.conf`.
If this directory doesn't exist, create it. Files should be owned by
`openvpn:network`.

If your VPN configuration file includes the `auth-federate` directive, remove
it — this is not understood by OpenVPN and is merely used as a marker to
indicate an Amazon VPN configuration.

Enable and start the _system_ unit:

```
$ systemctl enable --now aws-vpn@<instance>
```

This starts the OpenVPN process and keeps it running across reboots. You only
need to do this once per VPN.

To connect (authenticate and bring the tunnel up), start the _user_ unit:

```
$ systemctl --user start aws-vpn@<instance>
```

This opens a browser window to complete SAML authentication. Once done, the
browser tab can be safely closed if it doesn't close automatically.

To disconnect, stop only the _user_ unit:

```
$ systemctl --user stop aws-vpn@<instance>
```

The _system_ unit keeps running; you can reconnect at any time by starting
the user unit again.

If the machine is suspended while the VPN is connected, it will automatically
reconnect on resume, opening a browser window to re-authenticate.

## Debugging

System unit logs:
```
$ journalctl -u aws-vpn@<instance>
```

User unit logs:
```
$ journalctl --user -u aws-vpn@<instance>
```

Check both — issues can arise in either.

If you can connect but DNS resolution fails for some services, verify you're
using `systemd-resolved`, then try adding `dhcp-option DOMAIN-ROUTE .` to
your VPN configuration file.

## Details

The system unit runs the OpenVPN process, connects to the VPN, and installs
routes. The user unit handles SAML authentication via a browser window in the
local user's session.

The two services communicate over the OpenVPN management interface on a UNIX
domain socket. A user must be a member of the `network` group to connect; the
system service verifies group membership over the socket.

VPN configuration lives in `/etc/openvpn/client/<instance>.conf`, e.g.
`/etc/openvpn/client/myvpn.example.com.conf`.
