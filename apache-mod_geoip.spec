#Module-Specific definitions
%define mod_name mod_geoip
%define mod_conf A10_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Module for apache (2.0.x) to use the GeoIP database
Name:		apache-%{mod_name}
Version:	1.2.9
Release:	1
Group:		System/Servers
License:	GPL
URL:		http://www.maxmind.com/app/mod_geoip
Source0:	https://github.com/maxmind/geoip-api-mod_geoip2/archive/%{version}.tar.gz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
Requires:	geoip
BuildRequires:	pkgconfig(geoip)
BuildRequires:	libtool 
Epoch:		1

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

%setup -qn geoip-api-mod_geoip2-%{version}

cat >%{mod_conf} <<'EOF'
LoadModule geoip_module %{_libdir}/apache-extramodules/%{mod_so}
EOF

%build
%{_bindir}/apxs -c mod_geoip.c `pkg-config --cflags geoip` `pkg-config --libs geoip`

%install
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/

%files
%defattr(-,root,root)
%doc README.md Changes README.php 
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
