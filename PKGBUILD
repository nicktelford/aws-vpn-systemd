# Maintainer: Nick Telford <nick.telford@gmail.com>
pkgname=aws-vpn-systemd
pkgver=2.0
pkgrel=1
epoch=
pkgdesc="SystemD services for managing AWS Client VPN without the GUI, including a patched OpenVPN."
arch=('x86_64')
url="https://github.com/nicktelford/aws-vpn-systemd"
license=('GPL-2.0-only')
depends=('systemd' 'polkit' 'openssl')
makedepends=('autoconf' 'automake' 'libtool' 'pkg-config')
optdepends=('socat: preferred network tool (supports all operations)'
            'nmap: provides ncat, a supported alternative to socat'
            'openbsd-netcat: supported alternative to socat')
sha256sums=('a80ac3825bef9e97d717bc027663169903e25d86d2631e68f1100fcb2a9de702')
source=('https://amazon-source-code-downloads.s3.amazonaws.com/aws/clientvpn/openvpn-2.6.12-aws-1.tar.gz')
validpgpkeys=()

prepare() {
  cd "$srcdir/openvpn"
  autoreconf -fi
}

build() {
  cd "$srcdir/openvpn"
  ./configure \
    --disable-lzo \
    --disable-lz4 \
    --disable-plugins \
    --disable-pkcs11 \
    --disable-systemd \
    --disable-dco \
    --with-crypto-library=openssl
  make
}

package() {
  install -Dm755 "$srcdir/openvpn/src/openvpn/openvpn" "$pkgdir/usr/local/bin/acvc-openvpn"
  install -Dm644 "$srcdir/aws-vpn" "$pkgdir/usr/local/bin/aws-vpn"
  install -Dm755 "$srcdir/vpn-dns-up" "$pkgdir/usr/local/bin/vpn-dns-up"
  install -Dm755 "$srcdir/vpn-dns-down" "$pkgdir/usr/local/bin/vpn-dns-down"
  install -Dm644 "$srcdir/00-openvpn-resolved.rules" "$pkgdir/etc/polkit-1/rules.d/00-openvpn-resolved.rules"
  install -Dm644 "$srcdir/system_aws-vpn@.service" "$pkgdir/usr/local/lib/systemd/system/aws-vpn@.service"
  install -Dm644 "$srcdir/user_aws-vpn@.service" "$pkgdir/usr/local/lib/systemd/user/aws-vpn@.service"
  install -Dm755 "$srcdir/aws-vpn-sleep" "$pkgdir/usr/lib/systemd/system-sleep/aws-vpn"
  install -Dm644 "$srcdir/connected.html" "$pkgdir/usr/local/share/aws-vpn-systemd/connected.html"
}
