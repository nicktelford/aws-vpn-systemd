# Maintainer: Nick Telford <nick.telford@gmail.com>
pkgname=aws-vpn-systemd
pkgver=1
pkgrel=1
epoch=
pkgdesc="A set of SystemD services for managing the AWS VPN without the GUI."
arch=('any')
url="https://github.com/nicktelford/aws-vpn-systemd"
license=('GPL')
depends=('awsvpnclient' 'systemd' 'polkit')
optdepends=('openbsd-netcat: netcat implementation' 'nmap: netcat implementation')
conflicts=('gnu-netcat')
sha256sums=()
source=()
validpgpkeys=()

package() {
  install -Dm644 "$srcdir/aws-vpn" "$pkgdir/usr/local/bin/aws-vpn"
  install -Dm644 "$srcdir/00-openvpn-resolved.rules" "$pkgdir/etc/polkit-1/rules.d/00-openvpn-resolved.rules"
  install -Dm644 "$srcdir/system_aws-vpn@.service" "$pkgdir/usr/local/lib/systemd/system/aws-vpn@.service"
  install -Dm644 "$srcdir/user_aws-vpn@.service" "$pkgdir/usr/local/lib/systemd/user/aws-vpn@.service"
}

