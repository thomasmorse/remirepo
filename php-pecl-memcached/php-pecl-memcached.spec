%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name memcached

Summary:      Extension to work with the Memcached caching daemon
Name:         php-pecl-memcached
Version:      1.0.2
Release:      3%{?dist}.2
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# 5.2.10 required to HAVE_JSON enabled
BuildRequires: php-devel >= 5.2.10
BuildRequires: php-pear
BuildRequires: php-igbinary-devel
BuildRequires: libmemcached-devel
BuildRequires: zlib-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:     php-common >= 5.2.10
Requires:     php-igbinary
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}


%description
This extension uses libmemcached library to provide API for communicating
with memcached servers.

memcached is a high-performance, distributed memory object caching system,
generic in nature, but intended for use in speeding up dynamic web 
applications by alleviating database load.

It also provides a session handler (memcached). 


%prep 
%setup -c -q
cd %{pecl_name}-%{version}


%build
cd %{pecl_name}-%{version}
phpize
%configure --enable-memcached-igbinary
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; ----- Options to use the memcached session handler

;  Use memcache as a session handler
;session.save_handler=memcached
;  Defines a comma separated list of server urls to use for session storage
;session.save_path="localhost:11211"
EOF

# Install XML package description
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
%{__rm} -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
cd %{pecl_name}-%{version}
# only check if build extension can be loaded
%{__ln_s} %{php_extdir}/json.so modules/
%{__ln_s} %{php_extdir}/igbinary.so modules/
%{_bindir}/php \
    -n -q -d extension_dir=modules \
    -d extension=json.so \
    -d extension=igbinary.so \
    -d extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}


%files
%defattr(-, root, root, -)
%doc %{pecl_name}-%{version}/{CREDITS,LICENSE,README.markdown,ChangeLog}
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sat Feb 19 2011 Remi Collet <fedora@famillecollet.com> - 1.0.2-3.2
- rebuild for remi repo with SASL for fedora <= 10 and EL <= 5

* Sat Oct 02 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-3.1
- remove patch 

* Fri Oct 01 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-3
- rebuild against libmemcached 0.44 with SASL support

* Wed Sep 29 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-2
- rebuild with igbinary support

* Tue May 04 2010 Remi Collet <fedora@famillecollet.com> - 1.0.2-1
- update to 1.0.2 for libmemcached 0.40

* Sat Mar 13 2010 Remi Collet <fedora@famillecollet.com> - 1.0.1-1
- update to 1.0.1 for libmemcached 0.38

* Sun Feb 07 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3.1
- bump release

* Sat Feb 06 2010 Remi Collet <fedora@famillecollet.com> - 1.0.0-3
- rebuilt against new libmemcached
- add minimal %%check

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <fedora@famillecollet.com> - 1.0.0-1
- Update to 1.0.0 (First stable release)

* Sat Jun 27 2009 Remi Collet <fedora@famillecollet.com> - 0.2.0-1
- Update to 0.2.0 + Patch for HAVE_JSON constant

* Sun Apr 29 2009 Remi Collet <fedora@famillecollet.com> - 0.1.5-1
- Initial RPM

