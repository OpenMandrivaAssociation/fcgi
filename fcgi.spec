%define major 0
%define libname %mklibname %{name} %{major}

Summary:	The FastCGI development kit
Name:		fcgi
Version:	2.4.0
Release:	%mkrel 9
License:	BSD-style
Group:		System/Servers
URL:		http://www.fastcgi.com/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		fcgi-no-libs.patch.bz2
BuildRequires:	libstdc++-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	libtool
Requires:	%{libname} = %{version}
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
FastCGI is an open extension to CGI that provides high performance
for all Internet applications without the penalties of Web server
APIs.

FastCGI is designed to be layered on top of existing Web server
APIs. For instance, the mod_fastcgi Apache module adds FastCGI 
support to the Apache server. FastCGI can also be used, with 
reduced functionality and reduced performance, on any Web server
that supports CGI.

This FastCGI Developer's Kit is designed to make developing 
FastCGI applications easy. The kit currently supports FastCGI 
applications written in C/C++, Perl, Tcl, and Java.

This package contains only shared libraries used by programs 
developed using FastCGI Developer's Kit and cgi-fcgi (bridge from
CGI to FastCGI).

%package -n	%{libname}
Summary:	Libraries for %{name} 
Group:          System/Libraries

%description -n	%{libname}
This package contains the %{name} library files.

%package -n	%{libname}-devel
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libfcgi-devel = %{version}
Obsoletes:	libfcgi-devel

%description -n	%{libname}-devel
This package contains FastCGI Developer's Kit, which is designed
to make developing FastCGI applications easy. The kit currently
supports FastCGI applications written in C/C++, Perl, Tcl, and
Java.

%package -n	%{libname}-static-devel
Summary:	Development static libraries for %{name}
Group:		Development/C
Requires:	%{libname}-devel = %{version}

%description -n	%{libname}-static-devel
This package contains static libraries of %{name}.

%prep

%setup -q
%patch -p1

%build
touch INSTALL NEWS AUTHORS ChangeLog COPYING
rm -f configure
libtoolize --copy --force; aclocal-1.7; autoconf; automake-1.7 --add-missing --copy

%configure2_5x \
    --with-global \
    --with-nodebug \
    --with-noassert \
    --with-notest

make
				
%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

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

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(0644,root,root,0755)
%doc doc/*.1 LICENSE.TERMS README
%attr(0755,root,root) %{_bindir}/cgi-fcgi
%attr(0755,root,root) /var/www/fcgi-bin/authorizer
%attr(0755,root,root) /var/www/fcgi-bin/echo
%attr(0755,root,root) /var/www/fcgi-bin/echo-cpp
%attr(0755,root,root) /var/www/fcgi-bin/echo-x
%attr(0755,root,root) /var/www/fcgi-bin/log-dump
%attr(0755,root,root) /var/www/fcgi-bin/size
%attr(0755,root,root) /var/www/fcgi-bin/threaded

%files -n %{libname}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_libdir}/libfcgi++.so.0*
%attr(0755,root,root) %{_libdir}/libfcgi.so.0*

%files -n %{libname}-devel
%defattr(0644,root,root,0755)
%doc doc/*.htm* doc/*.gif doc/fastcgi-* doc/*.3
%attr(0755,root,root) %{_libdir}/libfcgi++.so
%attr(0755,root,root) %{_libdir}/libfcgi.so
%attr(0755,root,root) %{_libdir}/libfcgi++.la
%attr(0755,root,root) %{_libdir}/libfcgi.la
%{_includedir}/*.h
%{_datadir}/fastcgi/*

%files -n %{libname}-static-devel
%defattr(0644,root,root,0755)
%{_libdir}/libfcgi++.a
%{_libdir}/libfcgi.a
