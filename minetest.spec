%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global gitcommit bc0e5c0
%global gitname celeron55

Name:		minetest
Version:	0.3.1
Release:	2.git%{gitcommit}%{?dist}.R
Summary:	An InfiniMiner/Minecraft inspired game

Group:		Amusements/Games
License:	GPLv2+
URL:		http://celeron.55.lt/minetest/		

#		wget https://github.com/celeron55/minetest/tarball/bc0e5c0
#		wget https://raw.github.com/RussianFedora/minetest/master/minetest.desktop
Source0:	https://github.com/celeron55/minetest/tarball/%{gitcommit}
Source1:	%{name}.desktop


BuildRequires:	cmake >= 2.6.0
BuildRequires:	irrlicht-devel bzip2-devel libpng-devel libjpeg-turbo-devel libXxf86vm mesa-libGL-devel	jthread-devel sqlite-devel gettext-devel
BuildRequires:	desktop-file-utils

Requires:	hicolor-icon-theme

%description
An InfiniMiner/Minecraft inspired game

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
cp %{name}-icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps

# Add desktop file
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE1}

#Move doc directory back to the sources

mkdir __doc
mv  $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/* __doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}
 
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/%{name}server
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}-icon.svg

%doc README.txt doc/changelog.txt  doc/gpl-2.0.txt  doc/mapformat.txt  doc/protocol.txt

%changelog
* Sat Nov 12 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.3.1-2.gitbc0e5c0.R
- Fixed doc directories

* Wed Nov  9 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.3.1-1.gitbc0e5c0.R
- Update to stable 0.3.1 version

* Thu Nov  3 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.3.0-1.gitf65d157.R
- Update to stable 0.3.0 version

* Fri Sep 30 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.2.20110922_2-2.git960009d
- Desktop file and icon

* Fri Sep 30 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.2.20110922_2-1.git960009d
- Basic build of the current stable version
