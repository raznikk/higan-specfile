
Name: higan
Version: 104b
Release: 1%{?dist}

License: GPLv3
Summary: Emulator
URL:     http://byuu.org/emulation/higan
Source0: https://gitlab.com/higan/higan/repository/archive.tar.gz?ref=v%{version}

BuildRequires: gcc-c++
BuildRequires: gtk2-devel
BuildRequires: gtksourceview2-devel
BuildRequires: libao-devel
BuildRequires: libX11-devel
BuildRequires: libXv-devel
BuildRequires: openal-soft-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: SDL-devel
BuildRequires: systemd-devel


%description
Higan is an emulator.


%prep
%autosetup -n higan-v104b-0034adab3be51d365a6d45a308a1683d35909a52

sed -i \
        -e "/handle/s#/usr/local/lib#/usr/%{_libdir}#" \
        nall/dl.hpp || die "fixing libdir failed!"

# fix so that it doesn't build march=native
pushd higan
sed -i 's/march=native/march=x86-64/g' GNUmakefile
popd

pushd icarus
sed -i 's/march=native/march=x86-64/g' GNUmakefile
popd


%build
pushd icarus
make %{?_smp_mflags} compiler="$(which g++)" phoenix="gtk" platform="linux"
popd

pushd higan
make %{?_smp_mflags} compiler="$(which g++)" phoenix="gtk" platform="linux" profile="profile_accuracy"
popd


%install
install -d %{buildroot}/%{_datadir}/applications

pushd higan
%make_install prefix=%{buildroot}/%{_prefix}
popd
pushd icarus
%make_install prefix=%{buildroot}/%{_prefix}
popd


%files
%{_bindir}/higan
%{_bindir}/icarus
%{_datadir}/applications/higan.desktop
%{_datadir}/higan
%{_datadir}/icarus
%{_datadir}/icons/higan.png


%changelog
* Sat Sep 16 2017 Barry Britt <barry.britt@gmail.com> = 104-1
- Update to v104b.

* Sun Sep 04 2016 Randy Barlow <randy@electronsweatshop.com> - 101-1
- Update to v101.

* Fri Aug 05 2016 Randy Barlow <randy@electronsweatshop.com> - 100-1
- Update to v100.

* Tue Jun 21 2016 Randy Barlow <bowlofeggs@fedoraproject.org> - 099-1
- Initial release.
