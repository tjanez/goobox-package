Name:		goobox
Version:	3.2.1
Release:	0.1%{?dist}
Summary:	A Compact Disk Player and Ripper for GNOME

License:	GPLv2+
URL:		https://people.gnome.org/~paobac/goobox/
Source0:	http://ftp.gnome.org/pub/gnome/sources/goobox/3.2/%{name}-%{version}.tar.xz

# mandatory BuildRequires
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(libbrasero-media3)
BuildRequires:	pkgconfig(libmusicbrainz5)
BuildRequires:	pkgconfig(libdiscid)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(sm)
BuildRequires:	itstool
BuildRequires:	intltool
BuildRequires:	desktop-file-utils
# optional BuildRequires
BuildRequires:	pkgconfig(libnotify)
# NOTE: The libcoverart dependency is commented out since libcoverart is not
# packaged in Fedora yet (2014-03-11).
#BuildRequires:	pkgconfig(libcoverart)

# mandatory GStreamer plugins (cdparanoiasrc, audioconvert, volume, giosink)
# and OGG Vorbis encoder are currently all part of gstreamer1-plugins-base
Requires:	gstreamer1-plugins-base
# Flac and Wave encoders are currently part of gstreamer-plugins-good
Requires:	gstreamer1-plugins-good
# MP3 encoder is currently part of gstreamer1-plugins-ugly, which is
# available after enabling Third party repositories:
# https://fedoraproject.org/wiki/Third_party_repositories
# NOTE: When rpm gains support for weak dependencies, the following
# Recommends statement will be uncommented
#Recommends:	gstreamer1-plugins-ugly


%description
Goobox allows one to play CDs and save the tracks to disk as mp3, ogg, flac
or wav files (depending on the appropriate GStreamer plugins being installed).
Track titles and CD covers are set automatically using the MusicBrainz web
service.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
%make_install
# remove the deprecated "Encoding" key from the .desktop file
desktop-file-install \
  --remove-key="Encoding" \
  --delete-original \
  --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}/%{_datadir}/applications/%{name}.desktop
# find all the locale files belonging to the package
%find_lang %name --with-gnome


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/glib-2.0/schemas/org.gnome.Goobox.gschema.xml
%{_datadir}/GConf/gsettings/%{name}.convert


%changelog
* Sat Mar 22 2014 Tadej Janež <tadej.janez@tadej.hicsalta.si> 3.2.1-0.1
- Initial package.

