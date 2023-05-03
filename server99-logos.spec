Name:       server99-logos
Version:    18.0.0
Release:    8%{?dist}
Summary:    Icons and pictures

Group:      	System Environment/Base
URL:        	https://github.com/Server99-industries/server99-logos
Source0:    	https://github.com/Server99-industries/server99-logos/archive/refs/heads/main.tar.gz#/server99-logos-main.tar.gz
License:    	GPLv2 and LGPLv2+
BuildArch:  	noarch

Obsoletes:  redhat-logos
Obsoletes:  generic-logos < 17.0.0-5
Provides:   redhat-logos = %{version}-%{release}
Provides:   system-logos = %{version}-%{release}
Provides:   fedora-logos

Conflicts:  fedora-logos
Conflicts:  anaconda-images <= 10
Conflicts:  redhat-artwork <= 5.0.5
BuildRequires: hardlink
BuildRequires: 	make
# For generating the EFI icon
BuildRequires: libicns-utils
Requires(post): coreutils

%description
The server99-logos package contains various image files which can be
used by the bootloader, anaconda, and other related tools. It can
be used as a replacement for the fedora-logos package, if you are
unable for any reason to abide by the trademark restrictions on the
fedora-logos or fedora-remix-logos package.

%package httpd
Summary: Fedora-related icons and pictures used by httpd
Provides: system-logos-httpd = %{version}-%{release}
Provides: fedora-logos-httpd = %{version}-%{release}
Obsoletes:  generic-logos < 17.0.0-5
BuildArch: noarch

%description httpd
The server99-logos-httpd package contains image files which can be used by
httpd.

%prep
%autosetup -n server99-logos-main
%build
make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/firstboot/themes/server99
for i in firstboot/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/firstboot/themes/server99
done

mkdir -p %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora.icns %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora.vol %{buildroot}%{_datadir}/pixmaps/bootloader
install -p -m 644 bootloader/fedora-media.vol  %{buildroot}%{_datadir}/pixmaps/bootloader

mkdir -p %{buildroot}%{_datadir}/pixmaps
for i in pixmaps/* ; do
  install -p -m 644 $i %{buildroot}%{_datadir}/pixmaps
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge/
for i in plymouth/charge/* ; do
    install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/charge/
done

# File or directory names do not count as trademark infringement
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps/
install -p -m 644 icons/hicolor/48x48/apps/* %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
install	-p -m 644 icons/hicolor/scalable/apps/* %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
install	-p -m 644 icons/hicolor/symbolic/apps/* %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps/

(cd anaconda; make DESTDIR=%{buildroot} install)

# Plymouth logo
# The Plymoth spinner theme Fedora logo bits
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/spinner
install -p -m 644 pixmaps/fedora-gdm-logo.png $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/spinner/watermark.png
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/server99-spinner
install -p -m 644 pixmaps/fedora-gdm-logo.png $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/server99-spinner/watermark.png

# save some dup'd icons
hardlink -v %{buildroot}/

%post
touch --no-create %{_datadir}/icons/hicolor || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  if [ -f %{_datadir}/icons/hicolor/index.theme ]; then
    gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
fi
fi

%posttrans
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  if [ -f %{_datadir}/icons/hicolor/index.theme ]; then
    gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
fi


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_datadir}/firstboot/themes/*
%{_datadir}/anaconda/boot/*
%{_datadir}/anaconda/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/pixmaps/*
%{_datadir}/plymouth/themes/charge/*
%{_datadir}/plymouth/themes/spinner/watermark.png
%{_datadir}/plymouth/themes/server99-spinner/watermark.png
%exclude %{_datadir}/pixmaps/poweredby.png

%files httpd
%doc COPYING
%{_datadir}/pixmaps/poweredby.png

%changelog
* Wed May 3 2023 Stijn Rombouts
- Forked from generic-logos
