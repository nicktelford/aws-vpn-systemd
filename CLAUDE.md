# Summary
This project implements a VPN client for the AWS VPN, using a patched OpenVPN to support AWS' SAML authentication flow, and a pair of systemd units:

- The system unit (./src/system_aws-vpn@.service) runs as root and manages the OpenVPN connection, routes, etc.
- The user unit (./src/user_aws-vpn@.service) runs as the user and handles VPN SAML authentication.

The two units communicate using a UNIX domain socket. The user unit runs ./src/aws-vpn, which is a custom handler for the OpenVPN management interface.

The project is packaged for the following Linux distributions:

- Arch Linux (./packaging/arch)
- Debian/Ubuntu (./packaging/debian)
- RedHat/Fedora (./packaging/rpm)

# Project structure

- ./src/ - systemd units and BASH source files
- ./packaging/ - instructions for packaging for release
- ./patches/ - OpenVPN patch(es)
- ./dist/ - build target; contains nothing unless binary packages have been built
- ./Makefile - builds distro packages; targets: `clean`, `pkg` (arch), `deb`, `rpm` and `all`
- ./README.md - Further detail on project usage

# Debugging

To debug the installed and running version of each unit:

1. Identify the running VPN configuration NAME:

```
ls /etc/openvpn/client/*.conf
```

Where NAME is the name of the `.conf` file, e.g. `/etc/openvpn/client/NAME.conf`

2. Understand the current status of each unit:

```
systemctl status aws-vpn@NAME.service # system unit
systemctl status --user aws-vpn@NAME.service # user unit
```

3. Inspect detailed logs of each unit; you MUST include additional jouranlctl filters to restruct output to only the timeframes/invocations that are of interest.

```
journalctl -ocat -u aws-vpn@NAME.service # system unit
journalctl -ocat --user -u aws-vpn@NAME.service # user unit
```

# Versioning

To increment the relase version, update the `VERSION` variable in the `Makefile`. This variable is the source-of-truth for the release version used throughout this project.
