#Module-Specific definitions
%define mod_name mod_geoip
%define mod_conf A10_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Module for apache (2.0.x) to use the GeoIP database
Name:		apache-%{mod_name}
Version:	1.2.4
Release:	%mkrel 1
Group:		System/Servers
License:	GPL
URL:		http://www.maxmind.com/app/mod_geoip
Source0:	http://www.maxmind.com/download/geoip/api/mod_geoip2/%{mod_name}2_%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
Requires:	geoip
BuildRequires:	GeoIP-devel >= 1.4.0
BuildRequires:	libtool 
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
GeoIP is a C library that enables the user to find the country that any IP
address or hostname originates from. 
It uses a file based database that contains IP blocks as keys,
and countries as values. This database should be more complete and accurate
than using reverse DNS lookups. Commercial databases and automatic update
services are available from http://www.maxmind.com/

This module can be used to automatically select the geographically closest
mirror, to analyze your web server logs to determine the countries of your
visitors, for credit card fraud detection, and for software export controls.

See INSTALL file in document directory for how to use it.

%prep

%setup -q -n %{mod_name}2_%{version}

cp %{SOURCE1} %{mod_conf}

%build

%{_sbindir}/apxs -c mod_geoip.c -L%{_libdir} -I%{_includedir} -lGeoIP 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc INSTALL README Changes README.php 
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
