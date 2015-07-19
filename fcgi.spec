%define major	0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	The FastCGI development kit
Name:		fcgi
Version:	2.4.0
Release:	23
License:	BSD-style
Group:		System/Servers
Url:		http://www.fastcgi.com/
Source0:	http://www.fastcgi.com/dist/%{name}-%{version}.tar.gz
Patch0:		fcgi-no-libs.patch
Patch1:		FastCGI-clientdata_pointer.patch
Patch2:		FastCGI-makefile.am_cppflags.patch
Patch3:		fastcgi-2.4.0_missing_call_to_fclose.patch
Patch4:		FastCGI-2.4.0-CVE-2011-2766.diff
Patch5:		fcgi-2.4.0-gcc4.4.diff
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
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0

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
install -d %{buildroot}/var/www/fcgi-bin

pushd examples/.libs/
    install -m755 authorizer %{buildroot}/var/www/fcgi-bin/
    install -m755 echo %{buildroot}/var/www/fcgi-bin/
    install -m755 echo-cpp %{buildroot}/var/www/fcgi-bin/
    install -m755 echo-x %{buildroot}/var/www/fcgi-bin/
    install -m755 log-dump %{buildroot}/var/www/fcgi-bin/
    install -m755 size %{buildroot}/var/www/fcgi-bin/
    install -m755 threaded %{buildroot}/var/www/fcgi-bin/
popd

%files
%doc doc/*.1 LICENSE.TERMS README
%{_bindir}/cgi-fcgi
/var/www/fcgi-bin/authorizer
/var/www/fcgi-bin/echo
/var/www/fcgi-bin/echo-cpp
/var/www/fcgi-bin/echo-x
/var/www/fcgi-bin/log-dump
/var/www/fcgi-bin/size
/var/www/fcgi-bin/threaded

%files -n %{libname}
%{_libdir}/libfcgi++.so.%{major}*
%{_libdir}/libfcgi.so.%{major}*

%files -n %{devname}
%doc doc/*.htm* doc/*.gif doc/fastcgi-* doc/*.3
%{_libdir}/libfcgi++.so
%{_libdir}/libfcgi.so
%{_includedir}/*.h
%{_datadir}/fastcgi/*

