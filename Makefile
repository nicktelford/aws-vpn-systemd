NAME        := aws-vpn-systemd
VERSION     := 2.1
OPENVPN_VER := 2.7.4
OPENVPN_URL := https://build.openvpn.net/downloads/releases/openvpn-$(OPENVPN_VER).tar.gz
DIST_DIR    := $(CURDIR)/dist

.PHONY: pkg deb rpm clean

$(DIST_DIR):
	mkdir -p $@

pkg: | $(DIST_DIR)
	docker run --rm \
		-v "$(CURDIR):/src:ro" \
		-v "$(DIST_DIR):/dist" \
		archlinux:base-devel \
		bash -c 'pacman -Sy --noconfirm openssl \
			&& useradd -m builder \
			&& mkdir -p /workspace \
			&& cp -r /src/. /workspace/ \
			&& chown -R builder /workspace \
			&& su builder -c "cd /workspace/packaging/arch && makepkg -d" \
			&& cp /workspace/packaging/arch/*.pkg.tar.zst /dist/'

deb: | $(DIST_DIR)
	docker run --rm \
		-v "$(CURDIR):/src:ro" \
		-v "$(DIST_DIR):/dist" \
		ubuntu:24.04 \
		bash -c 'apt-get update -q \
			&& DEBIAN_FRONTEND=noninteractive apt-get install -qy --no-install-recommends \
				build-essential ca-certificates dpkg-dev debhelper autoconf automake libtool pkg-config libssl-dev libnl-genl-3-dev libcap-ng-dev wget \
			&& mkdir -p /workspace/build \
			&& cp -r /src/. /workspace/build/ \
			&& cd /workspace/build \
			&& ln -sfn packaging/debian debian \
			&& dpkg-buildpackage -us -uc -b \
			&& cp /workspace/*.deb /dist/'

rpm: | $(DIST_DIR)
	docker run --rm \
		-v "$(CURDIR):/src:ro" \
		-v "$(DIST_DIR):/dist" \
		fedora:42 \
		bash -c 'dnf install -y --setopt=install_weak_deps=False \
				rpm-build autoconf automake libtool pkgconfig openssl-devel libnl3-devel libcap-ng-devel wget \
			&& tar czf /tmp/$(NAME)-$(VERSION).tar.gz \
				--transform "s|^\./|$(NAME)-$(VERSION)/|" \
				--exclude=".git" --exclude="./dist" \
				-C /src . \
			&& wget -q -O /tmp/openvpn-$(OPENVPN_VER).tar.gz $(OPENVPN_URL) \
			&& rpmbuild -ba /src/packaging/rpm/$(NAME).spec \
				--define "_sourcedir /tmp" \
				--define "_builddir /tmp/BUILD" \
				--define "_rpmdir /dist" \
				--define "_srcrpmdir /dist"'

clean:
	$(RM) -r $(DIST_DIR)
