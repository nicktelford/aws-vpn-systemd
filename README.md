# AWS VPN (with SystemD)

_SystemD units and helper scripts to manage AWS VPN connections using SystemD,
instead of the Amazon GUI._

## Pre-requisites

* BASH 4+
* SystemD
* AWS VPN client or a compatibly patched OpenVPN client
* `ncat` from extras/nmap in arch.
* `dig` from extras/bind in arch.

## Assumptions

* The `openvpn` user exists, and the VPN client should run as this user.
* The `network` group exists, and members of this group may manage VPN connections. If you add current user to a group you need to logout/login.
* AWS VPN configuration files are stored in `/etc/openvpn/client/<instance>.conf`,
  where `<instance>` is the hostname of your VPN. If you are using AWS VPN Client then edit your vpn configuration and get rid of `auth-federate` if you have any. Then, copy your vpn configuration file to `/etc/openvpn/client/<instance>.conf`
* Your DNS configuration is being managed by `systemd-resolved`

## Usage

Replace `<instance>` with the hostname of your VPN below. Multiple VPNs may be
configured by repeating these steps for each VPN.

First, install the files, either using the Arch package, or manually as described below.

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
