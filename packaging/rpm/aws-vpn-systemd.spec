%global openvpn_version 2.7.4
%global debug_package %{nil}

Name:           aws-vpn-systemd
Version:        2.1
Release:        1%{?dist}
Summary:        systemd services for managing AWS Client VPN without the GUI
License:        GPL-2.0-only
URL:            https://github.com/nicktelford/aws-vpn-systemd

# Create with: git archive --prefix=aws-vpn-systemd-%%{version}/ HEAD -o aws-vpn-systemd-%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        https://build.openvpn.net/downloads/releases/openvpn-%{openvpn_version}.tar.gz
Source2:        %{name}.sysusers

BuildRequires:  systemd-rpm-macros
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  openssl-devel
BuildRequires:  libnl3-devel
BuildRequires:  libcap-ng-devel

Requires:       systemd
Requires:       polkit
Requires:       socat
%{?sysusers_requires_compat}

%description
Provides systemd services and a patched OpenVPN binary (acvc-openvpn)
for managing AWS Client VPN connections that use SAML authentication,
without requiring the official AWS VPN client.

%prep
%setup -q -n %{name}-%{version}
tar xzf %{SOURCE1} -C ..
patch -p1 -d ../openvpn-%{openvpn_version} \
    < patches/openvpn-%{openvpn_version}-aws.patch
cd ../openvpn-%{openvpn_version} && autoreconf -fi

%build
cd ../openvpn-%{openvpn_version}
./configure \
    --disable-lzo \
    --disable-lz4 \
    --disable-plugins \
    --disable-pkcs11 \
    --disable-systemd \
    --with-crypto-library=openssl
%make_build

%install
install -Dm755 ../openvpn-%{openvpn_version}/src/openvpn/openvpn \
    %{buildroot}/usr/local/bin/acvc-openvpn
install -Dm644 src/aws-vpn \
    %{buildroot}/usr/local/bin/aws-vpn
install -Dm755 src/vpn-dns-up \
    %{buildroot}/usr/local/bin/vpn-dns-up
install -Dm755 src/vpn-dns-down \
    %{buildroot}/usr/local/bin/vpn-dns-down
install -Dm644 src/00-openvpn-resolved.rules \
    %{buildroot}/etc/polkit-1/rules.d/00-openvpn-resolved.rules
install -Dm644 src/system_aws-vpn@.service \
    %{buildroot}/usr/local/lib/systemd/system/aws-vpn@.service
install -Dm644 src/user_aws-vpn@.service \
    %{buildroot}/usr/local/lib/systemd/user/aws-vpn@.service
install -Dm755 src/aws-vpn-sleep \
    %{buildroot}/usr/lib/systemd/system-sleep/aws-vpn
install -Dm644 src/connected.html \
    %{buildroot}/usr/local/share/%{name}/connected.html
install -Dm644 %{SOURCE2} \
    %{buildroot}%{_sysusersdir}/%{name}.conf

%pre
%sysusers_create_compat %{SOURCE2}

%files
/usr/local/bin/acvc-openvpn
/usr/local/bin/aws-vpn
/usr/local/bin/vpn-dns-up
/usr/local/bin/vpn-dns-down
/etc/polkit-1/rules.d/00-openvpn-resolved.rules
/usr/local/lib/systemd/system/aws-vpn@.service
/usr/local/lib/systemd/user/aws-vpn@.service
/usr/lib/systemd/system-sleep/aws-vpn
%dir /usr/local/share/%{name}
/usr/local/share/%{name}/connected.html
%{_sysusersdir}/%{name}.conf

%changelog
* Thu May 01 2026 Nick Telford <nick.telford@gmail.com> - 2.1-1
- Initial RPM packaging
