# AWS VPN (with SystemD)

_SystemD units and helper scripts to manage AWS VPN connections using SystemD,
instead of the Amazon GUI._

## Pre-requisites

* BASH 4+
* SystemD
* The AWS VPN client or a compatibly patched OpenVPN client
* Nmap/OpenBSD netcat (i.e. `ncat`).
  - Note: GNU Netcat is _NOT_ supported.
* `grep`, `sed`, `awk` and other basic utilities

Note: if you use a patched OpenVPN client, you will either need to install it
at `/opt/awsvpnclient/Service/Resources/openvpn/acvc-openvpn` or replace the
paths in the source files in this repo. You will also need to supply an
equivalent `configure-dns` script to the one shipped in the Amazon VPN client.

## Assumptions

* The `openvpn` user exists, and the VPN client should run as this user.
* The `network` group exists, and members of this group may manage VPN connections.
* AWS VPN configuration files are stored in `/etc/openvpn/client/<instance>.conf`,
  where `<instance>` is the hostname of your VPN.
* Your DNS configuration is being managed by `systemd-resolved`

## Usage

Replace `<instance>` with the hostname of your VPN below. Multiple VPNs may be
configured by repeating these steps for each VPN.

First, install the files, either using the Arch package, or manually as described below.

Place the configuration file for your VPN in `/etc/openvpn/client/<instance>.conf`.
If this directory doesn't exist, create it. These files should be owned by
user:group `openvpn:network`.

If your VPN configuration file included the `auth-federate` directive, remove it
as this is not understood by the OpenVPN client and is merely used as a marker
to indicate that this is an Amazon VPN configuration.

Next, enable the _system_ unit for the VPN:

```
$ systemctl enable aws-vpn@<instance>
```

Then start it:

```
$ systemctl start aws-vpn@<instance>
```

This will now automatically be enabled at start-up, and you will not need to
type these commands again.

To connect to the VPN, start the _user_ unit:

```
$ systemctl --user start aws-vpn@<instance>
```

This will open a browser window to authenticate you according to your VPNs
SAML authentication flow. Once complete, if the browser tab/window doesn't
automatically close, it can be safely closed. 

To disconnect the VPN, stop only the _user_ unit:

```
$ systemctl --user stop aws-vpn@<instance>
```

Note: you should not need to stop/restart the _system_ unit, which can be used
to connect/disconnect/reconnect to the same VPN multiple times.

## Installation

To build an Arch Linux package and install it:

```
$ makepkg -si
```

To manually install, copy the included files to the correct locations:

* `sudo cp system_aws-vpn@.service /usr/local/lib/systemd/system/aws-vpn@.service`
* `sudo cp user_aws-vpn@.service /usr/local/lib/systemd/user/aws-vpn@.service`
* `sudo cp aws-vpn /usr/local/bin/aws-vpn`
* `sudo cp 00-openvpn-resolved.rules /etc/polkit-1/rules.d/`

Note: if you are not using the AWS VPN client, or have it installed in a
different location, you may need to edit `system_aws-vpn@.service` to modify
the directory it searches for the various files.

## Debugging

* System unit logs: `journalctl -u aws-vpn@<instance>`
* User unit logs: `journalctl --user -u aws-vpn@<instance>`

Check both sets of logs for signs of problems, as issues can arise in either of
them.

If you're able to connect, but are having issues resolving hostnames of some
services; first verify you're using systemd-resolved, and if you are, try
adding `dhcp-option DOMAIN-ROUTE .` to your VPN configuration file.

## Details

The system service actually connects to the VPN, installs the routes etc.
The user service takes care of doing the SSO authentication via SAML and a
browser window in the local user's session.

The two services communicate via the OpenVPN management interface, over a UNIX
domain socket.

In order to connect, a user must be a member of the `network` group. The
system service verifies connections over the UNIX domain socket are from within
this group.

To configure the VPN, the instance files are in `/etc/openvpn/client/<instance>.conf`,
e.g. /etc/openvpn/client/myvpn.example.com.conf
