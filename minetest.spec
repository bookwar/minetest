%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global gitcommit bc0e5c0
%global gitname celeron55

Name:		minetest
Version:	0.3.1
Release:	3.git%{gitcommit}%{?dist}
Summary:	Multiplayer infinite-world block sandbox with survival mode

Group:		Amusements/Games
License:	GPLv2+
URL:		http://celeron.55.lt/minetest/		
#		wget https://github.com/celeron55/minetest/tarball/bc0e5c0
#		wget https://raw.github.com/RussianFedora/minetest/master/minetest.desktop
Source0:	https://github.com/celeron55/minetest/tarball/%{gitcommit}
Source1:	%{name}.desktop

BuildRequires:	cmake >= 2.6.0
BuildRequires:	irrlicht-devel
BuildRequires:	bzip2-devel gettext-devel jthread-devel sqlite-devel
BuildRequires:	libpng-devel libjpeg-turbo-devel libXxf86vm mesa-libGL-devel
BuildRequires:	desktop-file-utils

Requires:	%{name}-server = %{version}-%{release}
Requires:	hicolor-icon-theme

%description 
Game of mining, crafting and building in the infinite world of cubic
blocks with optional hostile creatures, features both single and the
network multiplayer mode. There are no in-game sounds yet

%package	server
Summary:	Minetest multiplayer server
Group:		Amusements/Games

%description	server
Minetest multiplayer server. This package does not require X Window System

%prep
%setup -q -n %{gitname}-%{name}-%{gitcommit}

%build
%cmake -DJTHREAD_INCLUDE_DIR=%{_includedir}/jthread .
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Put icon in the new fdo location
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
cp -p %{name}-icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps

# Add desktop file
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE1}

# Move doc directory back to the sources
mkdir __doc
mv  $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/* __doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}
 
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}-icon.svg

%files server
%{_bindir}/%{name}server

%doc README.txt doc/changelog.txt doc/gpl-2.0.txt doc/mapformat.txt doc/protocol.txt

%changelog
* Sat Nov 12 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.3.1-3.gitbc0e5c0
- Fixed Release tag for Fedora review

* Sat Nov 12 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.3.1-2.gitbc0e5c0.R
- Fixed doc directories
- Split package into main and -server parts

* Wed Nov  9 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.3.1-1.gitbc0e5c0.R
- Update to stable 0.3.1 version

* Thu Nov  3 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.3.0-1.gitf65d157.R
- Update to stable 0.3.0 version

* Fri Sep 30 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.2.20110922_2-2.git960009d
- Desktop file and icon

* Fri Sep 30 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.2.20110922_2-1.git960009d
- Basic build of the current stable version
