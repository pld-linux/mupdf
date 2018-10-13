Summary:	MuPDF - lightweight PDF, XPS and CBZ viewer and parser/rendering library
Summary(pl.UTF-8):	MuPDF - lekka przeglądarka PDF, XPS, CBZ
Name:		mupdf
Version:	1.14.0
Release:	1
License:	AGPL v3+
Group:		Applications/Text
Source0:	https://www.mupdf.com/downloads/archive/%{name}-%{version}-source.tar.gz
# Source0-md5:	98adc2f430cc7900397ab50a478485c5
URL:		https://www.mupdf.com/
BuildRequires:	OpenGL-glut-devel
BuildRequires:	curl-devel >= 7.51.0
BuildRequires:	freetype-devel >= 1:2.9.1
BuildRequires:	harfbuzz-devel >= 1.9.0
BuildRequires:	jbig2dec-devel >= 0.14
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	mujs-devel >= 1.0.4
BuildRequires:	openjpeg2-devel >= 2.3.0
BuildRequires:	openssl-devel >= 1.1.0
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	zlib-devel >= 1.2.11
Requires:	curl-libs-devel >= 7.51.0
Requires:	freetype >= 1:2.9.1
Requires:	harfbuzz >= 1.9.0
Requires:	jbig2dec >= 0.14
Requires:	openjpeg2 >= 2.3.0
Requires:	zlib >= 1.2.11
Obsoletes:	mupdf-devel < 1.13.0
Obsoletes:	mupdf-libs < 1.13.0
Obsoletes:	mupdf-static < 1.13.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MuPDF is a lightweight PDF, XPS and CBZ viewer.

%description -l pl.UTF-8
MuPDF to lekka przeglądarka pliki PDF, XPS i CBZ.

%prep
%setup -q -n %{name}-%{version}-source

# use system libs instead:
# curl 7.51.0
# freetype 2.9.1
# harfbuzz 1.9.0 + git update (nothing crucial)
# jbig2dec 0.14
# libjpeg 9
# mujs ?
# openjpeg 2.3.0
# zlib 1.2.11
%{__rm} -r thirdparty/{curl,freetype,jbig2dec,libjpeg,mujs,openjpeg,zlib}
# but keep:
# freeglut - 3.0.0 + some additional keyboard and clipboard APIs
# lcms2 - "art" fork with tread safety

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} -j1 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	SYS_OPENJPEG_CFLAGS="$(pkg-config --cflags libopenjp2)" \
	USE_SYSTEM_LIBS=yes \
	USE_SYSTEM_MUJS=yes \
	build=release \
	libdir=%{_libdir} \
	verbose=yes

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	USE_SYSTEM_LIBS=yes \
	USE_SYSTEM_MUJS=yes \
	build=release \
	prefix=%{_prefix} \
	libdir=%{_libdir}

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/mupdf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES CONTRIBUTORS README
%attr(755,root,root) %{_bindir}/mupdf-gl
%attr(755,root,root) %{_bindir}/mupdf-x11
%attr(755,root,root) %{_bindir}/mutool
%{_mandir}/man1/mupdf.1*
%{_mandir}/man1/mutool.1*
