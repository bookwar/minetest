%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global gitcommit 960009d
%global gitname celeron55

Name:		minetest
Version:	0.2.20110922_2
Release:	2.git%{gitcommit}%{?dist}.R
Summary:	An InfiniMiner/Minecraft inspired game

Group:		Amusements/Games
License:	GPLv2+
URL:		http://celeron.55.lt/minetest/		

#		wget https://github.com/celeron55/minetest/tarball/960009d
Source0:	https://github.com/celeron55/minetest/tarball/%{gitcommit}
Source1:	%{name}.desktop
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake >= 2.6.0
BuildRequires:	irrlicht-devel bzip2-devel libpng-devel libjpeg-turbo-devel libXxf86vm mesa-libGL-devel	jthread-devel sqlite-devel gettext-devel
Requires:	mesa-libGL irrlicht jthread sqlite gettext

%description
An InfiniMiner/Minecraft inspired game

%prep
%setup -q -n %{gitname}-%{name}-%{gitcommit}

%build
%cmake -DSQLITE3_INCLUDE_DIR=%{_includedir}/sqlite3 -DJTHREAD_INCLUDE_DIR=%{_includedir}/jthread .
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Put icon in the new fdo location
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
cp %{name}-icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
# Add desktop file
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications
 

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database -q

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%{_bindir}/%{name}
%{_bindir}/%{name}server
%{_datadir}/%{name}/*.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}-icon.svg
%{_docdir}/%{name}/*


%doc doc/README.txt doc/changelog.txt minetest.conf.example


%changelog
* Fri Sep 30 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.2.20110922_2-2.git960009d%{?dist}.R
- Desktop file and icon

* Fri Sep 30 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.2.20110922_2-1.git960009d%{?dist}.R
- Basic build of the current stable version.