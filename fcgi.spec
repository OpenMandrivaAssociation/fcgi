%define major 0
%define libname %mklibname %{name} %{major}

Summary:	The FastCGI development kit
Name:		fcgi
Version:	2.4.0
Release:	14
License:	BSD-style
Group:		System/Servers
URL:		http://www.fastcgi.com/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		fcgi-no-libs.patch
Patch1:		FastCGI-clientdata_pointer.patch
Patch2:		FastCGI-makefile.am_cppflags.patch
Patch3:		fastcgi-2.4.0_missing_call_to_fclose.patch
Patch4:		FastCGI-2.4.0-CVE-2011-2766.diff
Patch5:		fcgi-2.4.0-gcc4.4.diff
BuildRequires:	libstdc++-devel
BuildRequires:	autoconf automake libtool
Requires:	%{libname} >= %{version}

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
Requires:	%{libname} >= %{version}
Provides:	libfcgi-devel = %{version}
Obsoletes:	libfcgi-devel

%description -n	%{libname}-devel
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

%build
touch INSTALL NEWS AUTHORS ChangeLog COPYING
rm -f configure
libtoolize --copy --force; aclocal; autoconf; automake --add-missing --copy

%configure2_5x \
    --with-global \
    --with-nodebug \
    --with-noassert \
    --with-notest

make

%install
rm -rf %{buildroot}

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

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files
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
%attr(0755,root,root) %{_libdir}/libfcgi++.so.%{major}*
%attr(0755,root,root) %{_libdir}/libfcgi.so.%{major}*

%files -n %{libname}-devel
%doc doc/*.htm* doc/*.gif doc/fastcgi-* doc/*.3
%attr(0755,root,root) %{_libdir}/libfcgi++.so
%attr(0755,root,root) %{_libdir}/libfcgi.so
%{_includedir}/*.h
%{_datadir}/fastcgi/*


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 2.4.0-14
+ Revision: 773326
- fix build
- sync with MDVSA-2012:001
- various fixes

* Tue Dec 06 2011 Yuri Myasoedov <omerta13@mandriva.org> 2.4.0-13
+ Revision: 738408
- Added patch fixing building issue

  + Oden Eriksson <oeriksson@mandriva.com>
    - don't force the usage of automake1.7

* Tue Jul 22 2008 Thierry Vignaud <tv@mandriva.org> 2.4.0-11mdv2009.0
+ Revision: 240692
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Jul 07 2007 Oden Eriksson <oeriksson@mandriva.com> 2.4.0-9mdv2008.0
+ Revision: 49448
- make it build
- Import fcgi



* Mon Jun 26 2006 Oden Eriksson <oeriksson@mandriva.com> 2.4.0-8mdv2007.0
- rebuild
- fix deps

* Tue May 10 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4.0-7mdk
- added P0 by PLD
- make ite compile cleanly on x86_64

* Fri Jun 04 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.4.0-6mdk
- rebuilt against new deps and with gcc v3.4.x
- fix deps

* Wed Aug 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.4.0-5mdk
- put headers in %%{_includedir}/

* Wed Aug 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.4.0-4mdk
- use macros
- use spec file magic to make it compile...

* Sun Apr 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.4.0-3mdk
- rebuilt to have rpm v4.2 pick up provides

* Sun Apr 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.4.0-2mdk
- argh!!!, license is not GPL but BSD-style (darn templates...)
- clean up the spec file... (darn templates...)

* Sun Apr 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.4.0-1mdk
- initial cooker contrib, ripped from PLD, adapted for ML
