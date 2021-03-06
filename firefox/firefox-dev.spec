%define nspr_version 4.8.7
%define nss_version 3.12.9
%define cairo_version 1.10
%define freetype_version 2.1.9
%define lcms_version 1.18
%define sqlite_version 3.7.1

%define homepage http://start.fedoraproject.org/
%define default_bookmarks_file %{_datadir}/bookmarks/default-bookmarks.html
%define firefox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%define internal_version 4.0

%define mozappdir            %{_libdir}/firefox-%{internal_version}

%define tarballdir mozilla-central

%define official_branding    1
%define build_langpacks      1

%if ! %{official_branding}
%define cvsdate 20080327
%define nightly .cvs%{cvsdate}
%endif

%global relcan     b10
%global firefox    firefox
%global mycomment  Beta 10
%global datelang   20110126

Summary:        Mozilla Firefox Web browser
Name:           firefox
Version:        4.0
Release:        0.20.beta10%{?dist}
URL:            http://www.mozilla.org/projects/firefox/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Internet
%if %{official_branding}
## hg clone -u FIREFOX_3_6_3_RELEASE http://hg.mozilla.org/releases/mozilla-1.9.2
## tar cjf firefox-3.6.3.source.tar.bz2 --exclude .hg mozilla-1.9.2
%define tarball firefox-%{version}%{?relcan}.source.tar.bz2
%else
%define tarball firefox-3.1b3-source.tar.bz2
%endif
Source0:        %{tarball}
%if %{build_langpacks}
Source1:        firefox-langpacks-%{version}%{?relcan}-%{datelang}.tar.bz2
%endif
Source12:       firefox-redhat-default-prefs.js
# firefox3.destop without translation to allow change name
Source20:       firefox3.desktop
Source21:       firefox4.sh.in
Source23:       firefox.1
Source100:      find-external-requires

# build patches from xulrunner
#Patch0:        xulrunner-version.patch 	=> firefox / firefox4-version.patch
#Patch1:        mozilla-build.patch
Patch1:         firefox4-build.patch
#Patch3:         firefox4-jemalloc.patch
#Patch9:        mozilla-build-sbrk.patch
Patch9:         firefox4-build-sbrk.patch
Patch11:        mozilla-malloc.patch
Patch12:        xulrunner-2.0-64bit-big-endian.patch
Patch13:        xulrunner-2.0-secondary-jit.patch
Patch14:        xulrunner-2.0-chromium-types.patch
Patch15:        xulrunner-2.0-system-cairo.patch
Patch16:        xulrunner-2.0-system-cairo-tee.patch
Patch17:        xulrunner-2.0-os2cc.patch

# Fedora specific patches
Patch20:        mozilla-193-pkgconfig.patch
#Patch21:       mozilla-libjpeg-turbo.patch
Patch21:        firefox4-libjpeg-turbo.patch
Patch22:        mozilla-notify.patch
Patch23:        wmclass.patch

# build patches from firefox
Patch0:         firefox4-version.patch
#Patch1:         firefox4-jemalloc.patch	= xulrunner / firefox4-jemalloc.patch
#Patch2:         firefox4-build-throw.patch	= xulrunner / mozilla-malloc.patch

Patch30:        revert-562138.patch
Patch31:        firefox4-default.patch


# Fedora specific patches

# Upstream patches

# Remi specific patches


%if %{official_branding}
# Required by Mozilla Corporation


%else
# Not yet approved by Mozillla Corporation


%endif

# ---------------------------------------------------

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
# BR from Firefox
BuildRequires:  zip
BuildRequires:  libIDL-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= 2.1.9
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  startup-notification-devel
%ifarch %{ix86} x86_64
BuildRequires:  wireless-tools-devel
%endif

# BR from Xulrunner
%if %{fedora} >= 15
BuildRequires:  sqlite-devel >= %{sqlite_version}
%endif
%if %{fedora} >= 14
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
%endif
%if %{fedora} >= 11
BuildRequires:  hunspell-devel
%endif
%if %{fedora} >= 15
BuildRequires:  cairo-devel >= %{cairo_version}
%endif
%if %{fedora} >= 10
BuildRequires:  libnotify-devel
%endif
%if %{fedora} >= 9
BuildRequires:  lcms-devel >= %{lcms_version}
%endif
BuildRequires:  system-bookmarks
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf213
BuildRequires:  mesa-libGL-devel
BuildRequires:  yasm

Requires:       system-bookmarks
%if 0%{?fedora} >= 14
Requires:       nss >= %{nss_version}
Requires:       nspr >= %{nspr_version}
%endif
%if %{fedora} >= 9
BuildRequires:  lcms-devel >= %{lcms_version}
%endif
Obsoletes:      mozilla <= 37:1.7.13
%if %{name} == firefox
Obsoletes:      firefox4
Provides:       firefox4 = %{version}-%{release}
%endif
Provides:       webclient

%define _use_internal_dependency_generator 0
%define __find_requires %{SOURCE100}

# 10k of 11k files are in langpacks
%{?filter_setup:
%filter_provides_in %{mozappdir}/langpacks
%filter_requires_in %{mozappdir}/langpacks
%filter_setup
}

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

#---------------------------------------------------------------------

%prep
%if %{build_langpacks}
[ -f %{SOURCE1} ] || exit 1
%endif
%setup -q -c
cd %{tarballdir}

sed -e 's/__RPM_VERSION_INTERNAL__/%{internal_version}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch

# Build Patches
%patch1  -p2 -b .build
#patch3  -p1 -b .jemalloc
%patch9  -p2 -b .sbrk
%patch11 -p2 -b .malloc
#patch12 -p1 -b .macos
%patch12 -p2 -b .64bit-big-endian
%patch13 -p2 -b .secondary-jit
%patch14 -p2 -b .chromium-types
%if 0%{?fedora} >= 15
%patch15 -p1 -b .system-cairo
%patch16 -p1 -b .system-cairo-tee
%endif
%patch17 -p1 -b .os2cc

%patch20 -p2 -b .pk
%if %{fedora} >= 14
%patch21 -p2 -b .jpeg-turbo
%endif
%if %{fedora} >= 15
# when libnotify >= 0.7.0
%patch22 -p1 -b .notify
%endif
%patch23 -p1 -b .wmclass

%patch30 -p1 -b .revert-562138
%patch31 -p1 -b .default

%if 0%{?fedora} >= 15
# For xulrunner-2.0-system-cairo-tee.patch
autoconf-2.13
%endif

%{__rm} -f .mozconfig

cat <<EOF_MOZCONFIG | tee .mozconfig 
. \$topsrcdir/browser/config/mozconfig
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@

# --with-system-png is disabled because Mozilla requires APNG support in libpng
#ac_add_options --with-system-png
ac_add_options --prefix="\$PREFIX"
ac_add_options --libdir="\$LIBDIR"
%if %{fedora} >= 15
ac_add_options --enable-system-sqlite
%endif
%if %{fedora} >= 14
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
%endif
%if %{fedora} >= 11
ac_add_options --enable-system-hunspell
%endif
%if %{fedora} >= 15
ac_add_options --enable-system-cairo
%endif
%if %{fedora} >= 10
ac_add_options --enable-libnotify
%else
ac_add_options --disable-libnotify
%endif
%if %{fedora} >= 9
ac_add_options --enable-system-lcms
%endif
%ifarch ppc ppc64
ac_add_options --disable-necko-wifi
ac_add_options --disable-ipc
%endif
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-bz2
ac_add_options --with-pthreads
ac_add_options --disable-strip
ac_add_options --disable-tests
ac_add_options --disable-mochitest
ac_add_options --disable-installer
ac_add_options --disable-debug
ac_add_options --enable-optimize="\$MOZ_OPT_FLAGS"
ac_add_options --enable-xinerama
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --disable-xprint
ac_add_options --enable-pango
ac_add_options --enable-svg
ac_add_options --enable-canvas
ac_add_options --enable-startup-notification
ac_add_options --disable-cpp-exceptions
ac_add_options --disable-javaxpcom
ac_add_options --disable-crashreporter
ac_add_options --enable-safe-browsing
ac_add_options --disable-updater
ac_add_options --enable-shared-js
#ac_add_options --enable-chrome-format=jar
ac_add_options --enable-url-classifier
#ac_add_options --enable-extensions=default,python/xpcom
%if %{official_branding}
ac_add_options --enable-official-branding
%endif

export BUILD_OFFICIAL=1
export MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1
EOF_MOZCONFIG

#---------------------------------------------------------------------

%build
cd %{tarballdir}

# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
export MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS -fpermissive" | \
                             %{__sed} -e 's/-Wall//' -e 's/-fexceptions/-fno-exceptions/g')
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
%ifnarch ppc ppc64 s390 s390x
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -gt 1 ] && MOZ_SMP_FLAGS=-j$RPM_BUILD_NCPUS
%endif

INTERNAL_GECKO=%{internal_version}
MOZ_APP_DIR=%{_libdir}/%{name}-${INTERNAL_GECKO}

export LDFLAGS="-Wl,-rpath,${MOZ_APP_DIR}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

#---------------------------------------------------------------------

%install
%{__rm} -rf $RPM_BUILD_ROOT
cd %{tarballdir}

DESTDIR=$RPM_BUILD_ROOT make install

%{__mkdir_p} $RPM_BUILD_ROOT{%{_libdir},%{_bindir},%{_datadir}/applications}

sed -e 's/^Name=.*/Name=Firefox %{version} %{?mycomment}/' \
    -e "s/firefox/%{name}/" \
    %{SOURCE20} | tee %{name}.desktop

desktop-file-install --vendor mozilla \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category WebBrowser \
  --add-category Network \
  --delete-original %{name}.desktop 

# set up the firefox start script
%{__rm} -rf $RPM_BUILD_ROOT%{_bindir}/firefox
%{__cat} %{SOURCE21} | %{__sed} -e 's,FIREFOX_VERSION,%{internal_version},g' > \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

# set up our default preferences
%{__cat} %{SOURCE12} | %{__sed} \
	-e 's,FIREFOX_RPM_VR,fc%{fedora},g' \
	-e 's/Fedora/Remi/' > rh-default-prefs

######## Strange ########
if [ -f $RPM_BUILD_ROOT/%{mozappdir}/omni.jar ]; then
  unzip -o dist/firefox/omni.jar -d $RPM_BUILD_ROOT/%{mozappdir}
  rm -f $RPM_BUILD_ROOT/%{mozappdir}/omni.jar
fi
#########################

# Startup page for default language
sed -i -e 's@^\(browser\.startup\.homepage\(\|_reset\)\)=.*$@\1=%{homepage}@g;' \
      $RPM_BUILD_ROOT/%{mozappdir}/chrome/en-US/locale/branding/browserconfig.properties

# Export correct locale
%{__cat} > $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF
%{__chmod} 644 $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/firefox-l10n.js

# place the preferences
%{__cp} rh-default-prefs $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/all-redhat.js
%{__rm} rh-default-prefs

# set up our default bookmarks
%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/defaults/profile/bookmarks.html
ln -s %{default_bookmarks_file} $RPM_BUILD_ROOT/%{mozappdir}/defaults/profile/bookmarks.html

%{__install} -p -D -m 644 %{SOURCE23} $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/firefox-config

#cd $RPM_BUILD_ROOT/%{mozappdir}/chrome
#find . -name "*" -type d -maxdepth 1 -exec %{__rm} -rf {} \;
#cd -

#%{__cat} > $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/firefox-l10n.js << EOF
#pref("general.useragent.locale", "chrome://global/locale/intl.properties");
#EOF
#%{__chmod} 644 $RPM_BUILD_ROOT/%{mozappdir}/defaults/pref/firefox-l10n.js

%{__cp} other-licenses/branding/%{firefox}/default16.png \
        $RPM_BUILD_ROOT/%{mozappdir}/icons/
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
%{__cp} other-licenses/branding/%{firefox}/default16.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps
%{__cp} other-licenses/branding/%{firefox}/default22.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps
%{__cp} other-licenses/branding/%{firefox}/default24.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
%{__cp} other-licenses/branding/%{firefox}/default32.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
%{__cp} other-licenses/branding/%{firefox}/default48.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps
%{__cp} other-licenses/branding/%{firefox}/default256.png \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

echo > ../%{name}.lang
%if %{build_langpacks}
# Install langpacks
%{__mkdir_p} $RPM_BUILD_ROOT/%{mozappdir}/langpacks
%{__tar} xjf %{SOURCE1}
for langpack in `ls firefox-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensiondir=$RPM_BUILD_ROOT/%{mozappdir}/langpacks/langpack-$language@firefox.mozilla.org
  %{__mkdir_p} $extensiondir
  unzip -q $langpack -d $extensiondir
  find $extensiondir -type f | xargs chmod 644

  sed -i -e 's@^\(browser\.startup\.homepage\(\|_reset\)\)=.*$@\1=%{homepage}@g;' \
         $extensiondir/chrome/$language/locale/branding/browserconfig.properties
  cat    $extensiondir/chrome/$language/locale/branding/browserconfig.properties

  language=`echo $language | sed -e 's/-/_/g'`
  extensiondir=`echo $extensiondir | sed -e "s,^$RPM_BUILD_ROOT,,"`
  echo "%%lang($language) $extensiondir" >> ../%{name}.lang
done
%{__rm} -rf firefox-langpacks
%endif # build_langpacks

# System extensions
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/mozilla/extensions/%{firefox_app_id}
%{__mkdir_p} $RPM_BUILD_ROOT%{_libdir}/mozilla/extensions/%{firefox_app_id}

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE $RPM_BUILD_ROOT/%{mozappdir}

# Use the system hunspell dictionaries
%{__rm} -rf $RPM_BUILD_ROOT/%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{mozappdir}/dictionaries

# ghost files
touch $RPM_BUILD_ROOT/%{mozappdir}/components/compreg.dat
touch $RPM_BUILD_ROOT/%{mozappdir}/components/xpti.dat

# jemalloc shows up sometimes, but it's not needed here, it's in XR
#%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/libjemalloc.so

# Remi : this appears on Fedora <= 10
%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/*.chk
%{__rm} -f $RPM_BUILD_ROOT/%{mozappdir}/dependentlibs.list

# Don't need this
%{__rm}  -f $RPM_BUILD_ROOT/%{mozappdir}/removed-files
%{__rm} -rf $RPM_BUILD_ROOT/%{_includedir}/firefox-sdk-%{internal_version}
%{__rm} -rf $RPM_BUILD_ROOT/%{_libdir}/firefox-sdk-%{internal_version}
%{__rm} -rf $RPM_BUILD_ROOT/%{_datadir}/idl/firefox-sdk-%{internal_version}


#---------------------------------------------------------------------

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#---------------------------------------------------------------------

%pre
echo -e "\nWARNING : This %{name} %{version} %{mycomment} RPM is not an official"
echo -e "Fedora build and it overrides the official one. Don't file bugs on Fedora Project.\n"
echo -e "Use dedicated forums http://forums.famillecollet.com/\n"

%if %{?fedora}%{!?fedora:99} <= 12
echo -e "WARNING : Fedora %{fedora} is now EOL :"
echo -e "You should consider upgrading to a supported release.\n"
%endif

%post
chcon -t textrel_shlib_t %{mozappdir}/libxul.so &>/dev/null || :
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%preun
# Only for firefox (not for firefox4, tu manage update from firefox4 to firefox)
%if %{name} == firefox
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
  %{__rm} -rf %{mozappdir}/extensions
  %{__rm} -rf %{mozappdir}/langpacks
  %{__rm} -rf %{mozappdir}/plugins
fi
%endif

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_mandir}/man1/*
%dir %{_datadir}/mozilla/extensions/%{firefox_app_id}
%dir %{_libdir}/mozilla/extensions/%{firefox_app_id}
%{_datadir}/applications/mozilla-%{name}.desktop
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%doc %{mozappdir}/README.txt
#%{mozappdir}/*.properties
%{mozappdir}/chrome
%dir %{mozappdir}/components
%ghost %{mozappdir}/components/compreg.dat
%ghost %{mozappdir}/components/xpti.dat
%{mozappdir}/components/*.so
%{mozappdir}/components/*.xpt
%attr(644, root, root) %{mozappdir}/blocklist.xml
%attr(644, root, root) %{mozappdir}/components/*.js
#%attr(644, root, root) %{mozappdir}/components/components.list
%attr(644, root, root) %{mozappdir}/components/*.manifest
%attr(644, root, root) %{mozappdir}/*.manifest
%{mozappdir}/defaults
#%{mozappdir}/greprefs
%{mozappdir}/greprefs.js
%{mozappdir}/dictionaries
%dir %{mozappdir}/extensions
%{mozappdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%dir %{mozappdir}/langpacks
%{mozappdir}/icons
%{mozappdir}/searchplugins
%{mozappdir}/firefox
%{mozappdir}/firefox-bin
%{mozappdir}/modules
#%{mozappdir}/plugins
%{mozappdir}/res
%{mozappdir}/*.so
%if %{fedora} > 8
%ifarch %{ix86} x86_64
%{mozappdir}/plugin-container
%endif
%endif
%{mozappdir}/mozilla-xremote-client
%{mozappdir}/platform.ini
%{mozappdir}/run-mozilla.sh
%{mozappdir}/application.ini
#%{mozappdir}/.autoreg
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png

#---------------------------------------------------------------------

%changelog
* Thu Jan 27 2011 Remi Collet <rpms@famillecollet.com> - 4.0-0.20.beta10
- latest patch from rawhide

* Wed Jan 26 2011 Christopher Aillon <caillon@redhat.com> - 2.0-0.18
- Fix issue with popup windows showing in the wrong place

* Wed Jan 26 2011 Remi Collet <rpms@famillecollet.com> - 4.0-0.19.beta10
- update to 4.0b10
- switch to system cairo on fedora >= 15 only (patches from rawhide)

* Tue Jan 25 2011 Christopher Aillon <caillon@redhat.com> - 4.0-0.13b10
- Firefox 4.0 Beta 10

* Sat Jan 22 2011 Remi Collet <rpms@famillecollet.com> - 4.0-0.18.beta10.build1
- update to 4.0b10 build1 candidate
- BR nss >= 3.12.9, nspr >= 4.8.7

* Fri Jan 14 2011 Remi Collet <rpms@famillecollet.com> - 4.0-0.17.beta9
- update to 4.0b9

* Wed Jan 12 2011 Remi Collet <rpms@famillecollet.com> - 4.0-0.16.beta9.build1
- update to 4.0b9 build1 candidate
- use bundled cairo

* Fri Dec 31 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.15.beta8
- rename to firefox (and obsolete firefox4)

* Tue Dec 21 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.14.beta8
- update to 4.0b8

* Fri Dec 17 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.13.beta8.build1
- update to 4.0b8 build1 candidate

* Thu Nov 11 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.12.beta7
- update to 4.0b7
- raise cairo BR to 1.10 (fedora >= 14)

* Sat Nov 06 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.11.beta7.build1
- update to 4.0b7 build1 candidate

* Thu Sep 16 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.10.beta6
- update to 4.0b6

* Tue Sep 14 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.9.beta6.build2
- update to 4.0b6 build2
- add patch for https://bugzilla.mozilla.org/591152

* Wed Sep 08 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.8.beta5
- update to 4.0b5
- sync patches with rawhide
- set MOZ_OBJDIR

* Thu Sep 02 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.7.beta5.build1
- update to 4.0b5 build1

* Wed Aug 25 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.6.beta4
- update to 4.0 beta 4

* Wed Aug 18 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.5.beta4.build2
- update to 4.0b4 build2
- add BR yasm

* Sun Aug 15 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.4.beta3
- update to 4.0b3

* Sat Aug 07 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.3.beta3.build3
- update to 4.0b3 build3

* Wed Jul 28 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.2.beta2
- update to 4.0b2

* Wed Jul 28 2010 Remi Collet <rpms@famillecollet.com> - 4.0-0.1.beta2.build1
- update to 4.0b2 build1

* Sat Jul 24 2010 Remi Collet <rpms@famillecollet.com> - 3.6.8-1
- update to Firefox 3.6.8

* Tue Jul 20 2010 Remi Collet <rpms@famillecollet.com> - 3.6.7-1
- update to Firefox 3.6.7

* Tue Jun 29 2010 Remi Collet <rpms@famillecollet.com> - 3.6.6-1.1
- build with --disable-ipc option for F-8 and ppc

* Sun Jun 27 2010 Remi Collet <rpms@famillecollet.com> - 3.6.6-1
- update to Firefox 3.6.6

* Wed Jun 23 2010 Remi Collet <rpms@famillecollet.com> - 3.6.4-1
- update to Firefox 3.6.4 finale
- sync with patches from rawhide / F-13

* Thu Jun 10 2010 Remi Collet <rpms@famillecollet.com> - 3.6.4-0.4.build6
- F12 build
- fix sqlite dependency (3.6.22)
- fix path for mozilla-xremote-client in launcher 

* Sat May 29 2010 Remi Collet <rpms@famillecollet.com> - 3.6.4-0.3.build6
- update to Firefox 3.6.4 Beta (build6)

* Fri May 14 2010 Remi Collet <rpms@famillecollet.com> - 3.6.4-0.2.build4
- update to Firefox 3.6.4 Beta (build4)

* Thu May 13 2010 Remi Collet <rpms@famillecollet.com> - 3.6.4-0.1.build3
- update to Firefox 3.6.4 Beta (build3)

* Sat Apr 10 2010 Remi Collet <rpms@famillecollet.com> - 3.6.3-2.plugin1
- update to Firefox "lorentz" 3.6.3plugin1

* Fri Apr 02 2010 Remi Collet <rpms@famillecollet.com> - 3.6.3-1
- Update to Firefox 3.6.3 (sources from mercurial)

* Tue Mar 23 2010 Remi Collet <rpms@famillecollet.com> - 3.6.2-1
- Update to Firefox 3.6.2

* Thu Mar 18 2010 Remi Collet <rpms@famillecollet.com> - 3.6.2-0.3.build3
- Update to Firefox 3.6.2 Candidate Build 3

* Mon Mar 15 2010 Remi Collet <rpms@famillecollet.com> - 3.6.2-0.1.build1
- Update to Firefox 3.6.2 Candidate Build 1

* Thu Jan 21 2010 Remi Collet <rpms@famillecollet.com> - 3.6-1
- Update to Firefox 3.6 Finale

* Sat Jan 09 2010 Remi Collet <rpms@famillecollet.com> - 3.6-0.5.rc1
- Update to Firefox 3.6 Release Candidate 1

* Thu Dec 17 2009 Remi Collet <rpms@famillecollet.com> - 3.6-0.4.beta5
- Update to Firefox 3.6 Beta 5

* Thu Nov 26 2009 Remi Collet <rpms@famillecollet.com> - 3.6-0.4.beta4
- Update to Firefox 3.6 Beta 4

* Wed Nov 18 2009 Remi Collet <rpms@famillecollet.com> - 3.6-0.3.beta3
- Update to Firefox 3.6 Beta 3
- switch from firefox36 to firefox

* Tue Nov 10 2009 Remi Collet <rpms@famillecollet.com> - 3.6-0.2.beta2
- Update to Firefox 3.6 Beta 2

* Fri Nov  6 2009 Remi Collet <rpms@famillecollet.com> - 3.6-0.1.beta1
- Update to Firefox 3.6 Beta 1

* Thu Nov  5 2009 Remi Collet <rpms@famillecollet.com> - 3.5.5-1
- Update to Firefox 3.5.5 Final Release

* Thu Nov  5 2009 Jan Horak <jhorak@redhat.com> - 3.5.5-1
- Update to 3.5.5

* Wed Oct 28 2009 Remi Collet <rpms@famillecollet.com> - 3.5.4-1
- Update to Firefox 3.5.4 Final Release

* Mon Oct 26 2009 Jan Horak <jhorak@redhat.com> - 3.5.4-1
- Update to 3.5.4

* Wed Sep 9 2009 Remi Collet <rpms@famillecollet.com> - 3.5.3-1
- Update to Firefox 3.5.3 Final Release

* Mon Sep  7 2009 Jan Horak <jhorak@redhat.com> - 3.5.3-1
- Updated to 3.5.3.

* Thu Aug 6 2009 Martin Stransky <stransky@redhat.com> - 3.5.2-3
- Fix for #437596 - Firefox needs to register proper name
  for session restore.

* Tue Aug 4 2009 Remi Collet <rpms@famillecollet.com> - 3.5.2-1
- Update to Firefox 3.5.2 Final Release

* Mon Aug 3 2009 Martin Stransky <stransky@redhat.com> - 3.5.2-2
- Updated to 3.5.2.

* Fri Jul 24 2009 Jan Horak <jhorak@redhat.com> - 3.5.1-3
- Adjust icons cache update according to template

* Fri Jul 17 2009 Remi Collet <rpms@famillecollet.com> - 3.5.1-1
- Update to Firefox 3.5.1 Final Release

* Fri Jul 17 2009 Remi Collet <rpms@famillecollet.com> - 3.5.1-0.1.build1
- Update to Firefox 3.5.1 build1

* Wed Jun 30 2009 Remi Collet <rpms@famillecollet.com> - 3.5-1
- Update to Firefox 3.5 Final Release

* Wed Jun 27 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.27.rc3
- Update to Firefox 3.5 RC3

* Wed Jun 24 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.26.rc3.build2
- Update to Firefox 3.5 RC3 build2

* Fri Jun 19 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.26.rc2
- Update to Firefox 3.5 RC2

* Thu Jun 18 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.25.rc2.build2
- Update to Firefox 3.5 RC2 build2

* Wed Jun 17 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.24.rc1
- Update to Firefox 3.5 RC1

* Tue Jun 16 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.23.rc1.build2
- Update to Firefox 3.5 RC1 build2

* Sun Jun 14 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.22.rc1.build1
- Update to Firefox 3.5 RC1 build1

* Thu Jun 11 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.21.beta99
- Update to Firefox 3.5 Beta 99 (Preview)

* Tue Apr 28 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.2.beta4
- Update to Firefox 3.5 Beta 4

* Fri Apr 24 2009 Remi Collet <rpms@famillecollet.com> - 3.5-0.1.beta4
- Update to 3.5b4 build1
- use system-nss only if Fedora >= 11 (3.12.3)

* Thu Apr 23 2009 Remi Collet <rpms@famillecollet.com> - 3.1-0.1.beta3
- First Firefox 3.1 build from rawhide xulrunner + firefox spec

