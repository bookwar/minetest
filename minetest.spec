Name:		minetest
Version:	0.2.20110922_2
Release:	1%{?dist}
Summary:	An InfiniMiner/Minecraft inspired game

Group:		Amusements/Games
License:	GPLv2+
URL:		http://celeron.55.lt/minetest/		


#Github Source	https://github.com/celeron55/minetest/tarball/stable
Source0:	%{name}-%{version}.tar.gz	
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	cmake >= 2.6.0
BuildRequires:	irrlicht-devel bzip2-devel libpng-devel libjpeg-turbo-devel libXxf86vm mesa-libGL-devel	jthread-devel sqlite-devel gettext-devel
Requires:	mesa-libGL irrlicht jthread sqlite gettext

%description
An InfiniMiner/Minecraft inspired game

%prep
%setup -q -n %{name}-%{version}

%build
%cmake -DSQLITE3_INCLUDE_DIR=%{_includedir}/sqlite3 -DJTHREAD_INCLUDE_DIR=%{_includedir}/jthread .
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/%{name}
%{_bindir}/%{name}server
%{_datadir}/%{name}/*.png
%{_docdir}/%{name}/*

%doc doc/README.txt doc/changelog.txt minetest.conf.example


%changelog
* Fri Sep 30 2011 Aleksandra Bookwar <alpha@bookwar.info> - 0.2.20110922_2-1
- Basic build of the current stable version.


