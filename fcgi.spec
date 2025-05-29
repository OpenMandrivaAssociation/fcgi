%define major	0
%define oldlibname %mklibname %{name} 0
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

%define _disable_rebuild_configure 1

Summary:	The FastCGI development kit
Name:		fcgi
Version:	2.4.6
Release:	1
License:	BSD-style
Group:		System/Servers
Url:		https://fastcgi-archives.github.io/
Source0:	https://github.com/FastCGI-Archives/fcgi2/archive/refs/heads/master.tar.gz
Patch0:		fcgi-no-libs.patch
Patch1:		FastCGI-clientdata_pointer.patch
Patch4:		FastCGI-2.4.0-CVE-2011-2766.diff
BuildRequires:	libstdc++-devel

%description
FastCGI is an open extension to CGI that provides high performance
for all Internet applications without the penalties of Web server
APIs.

FastCGI is designed to be layered on top of existing Web server
APIs. For instance, the mod_fastcgi Apache module adds FastCGI 
support to the Apache server. FastCGI can also be used, with 
reduced functionality and reduced performance, on any Web server
that supports CGI.

%package -n	%{libname}
Summary:	Libraries for %{name}
Group:          System/Libraries
%rename %{oldlibname}

%description -n	%{libname}
This package contains the %{name} library files.

%package -n	%{devname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}fcgi0-devel

%description -n	%{devname}
This package contains FastCGI Developer's Kit, which is designed
to make developing FastCGI applications easy. The kit currently
supports FastCGI applications written in C/C++, Perl, Tcl, and
Java.

%prep
%autosetup -p1 -n fcgi2-master

sed -i -e 's|AM_CONFIG_HEADER|AC_CONFIG_HEADERS|g' \
	configure*

%build
touch INSTALL NEWS AUTHORS ChangeLog COPYING
autoreconf -fi
%configure2_5x \
	--disable-static \
	--with-global \
	--with-nodebug \
	--with-noassert \
	--with-notest

make

%install
%makeinstall_std

install -d %{buildroot}%{_datadir}/fastcgi
cp -a examples/{Makefile*,*.c} %{buildroot}%{_datadir}/fastcgi/

# install the built examples (should we require apache here?)
install -d %{buildroot}/srv/www/fcgi-bin

pushd examples/.libs/
    install -m755 authorizer %{buildroot}/srv/www/fcgi-bin/
    install -m755 echo %{buildroot}/srv/www/fcgi-bin/
    install -m755 echo-cpp %{buildroot}/srv/www/fcgi-bin/
    install -m755 echo-x %{buildroot}/srv/www/fcgi-bin/
    install -m755 log-dump %{buildroot}/srv/www/fcgi-bin/
    install -m755 size %{buildroot}/srv/www/fcgi-bin/
    install -m755 threaded %{buildroot}/srv/www/fcgi-bin/
popd

%files
%doc doc/*.1 LICENSE.TERMS README.md
%{_bindir}/cgi-fcgi
/srv/www/fcgi-bin/authorizer
/srv/www/fcgi-bin/echo
/srv/www/fcgi-bin/echo-cpp
/srv/www/fcgi-bin/echo-x
/srv/www/fcgi-bin/log-dump
/srv/www/fcgi-bin/size
/srv/www/fcgi-bin/threaded
%{_mandir}/man1/cgi-fcgi.1*

%files -n %{libname}
%{_libdir}/libfcgi++.so.%{major}*
%{_libdir}/libfcgi.so.%{major}*

%files -n %{devname}
%doc doc/*.htm* doc/*.gif doc/fastcgi-* doc/*.3
%{_libdir}/libfcgi++.so
%{_libdir}/libfcgi.so
%{_includedir}/*.h
%{_datadir}/fastcgi/*
%{_libdir}/pkgconfig/fcgi.pc
%{_libdir}/pkgconfig/fcgi++.pc
%{_mandir}/man3/FCGI_*
