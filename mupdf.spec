#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	MuPDF - lightweight PDF, XPS and CBZ viewer and parser/rendering library
Summary(pl.UTF-8):	MuPDF - lekka przeglądarka PDF, XPS, CBZ
Name:		mupdf
Version:	1.23.6
Release:	2
License:	AGPL v3+
Group:		Applications/Text
Source0:	https://www.mupdf.com/downloads/archive/%{name}-%{version}-source.tar.lz
# Source0-md5:	074fb84b19835dcbde558c1973d063cc
Patch0:		%{name}-soname.patch
Patch1:		%{name}-flags.patch
URL:		https://www.mupdf.com/
BuildRequires:	OpenGL-glut-devel
BuildRequires:	curl-devel >= 7.66.0
BuildRequires:	freetype-devel >= 1:2.13.0
BuildRequires:	gumbo-parser-devel >= 0.10.1
BuildRequires:	harfbuzz-devel >= 6.0.0
BuildRequires:	jbig2dec-devel >= 0.18
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	lzip
BuildRequires:	mujs-devel >= 1.3.3
BuildRequires:	openjpeg2-devel >= 2.5.0
BuildRequires:	openssl-devel >= 1.1.0
BuildRequires:	pkgconfig
BuildRequires:	python3-furo
BuildRequires:	python3-rst2pdf
BuildRequires:	sphinx-pdg
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	zlib-devel >= 1.2.13
Requires:	%{name}-libs = %{version}-%{release}
Requires:	curl-libs >= 7.66.0
Requires:	freetype >= 1:2.13.0
Requires:	gumbo-parser >= 0.10.1
Requires:	harfbuzz >= 6.0.0
Requires:	jbig2dec >= 0.18
Requires:	openjpeg2 >= 2.5.0
Requires:	zlib >= 1.2.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MuPDF is a lightweight PDF, XPS and CBZ viewer.

%description -l pl.UTF-8
MuPDF to lekka przeglądarka pliki PDF, XPS i CBZ.

%package libs
Summary:	Shared MuPDF libraries
Summary(pl.UTF-8):	Biblioteki współdzielone MuPDF
Group:		Libraries
Requires:	freetype >= 1:2.13.0
Requires:	jbig2dec >= 0.18
Requires:	mujs >= 1.3.3
Requires:	openjpeg2
Requires:	openssl >= 1.1.0
Requires:	zlib >= 1.2.13

%description libs
Shared MuPDF libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone MuPDF.

%package devel
Summary:	Header files for MuPDF libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek MuPDF
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	freetype-devel >= 1:2.13.0
Requires:	jbig2dec-devel >= 0.18
Requires:	libjpeg-devel
Requires:	libstdc++-devel
Requires:	mujs-devel >= 1.3.3
Requires:	openjpeg2-devel >= 2.5.0
Requires:	openssl-devel >= 1.1.0
Requires:	zlib-devel >= 1.2.13

%description devel
Header files for MuPDF libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek MuPDF.

%package static
Summary:	Static MuPDF libraries
Summary(pl.UTF-8):	Statyczne biblioteki MuPDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MuPDF libraries.

%description static -l pl.UTF-8
Statyczne biblioteki MuPDF.

%prep
%setup -q -n %{name}-%{version}-source
%patch0 -p1
%patch1 -p1

# use system libs instead:
# curl 7.66.0
# freetype 2.13.0
# gumbo-parser 0.10.1
# harfbuzz 6.0.0
# jbig2dec 0.18
# libjpeg 9
# mujs 1.3.3
# openjpeg 2.5.0
# zlib 1.2.13
%{__rm} -r thirdparty/{curl,freetype,gumbo-parser,harfbuzz,jbig2dec,libjpeg,mujs,openjpeg,zlib}
# but keep:
# freeglut - 3.0.0 + some additional keyboard and clipboard APIs
# lcms2 - "art" fork with tread safety

%build
%if %{with static_libs}
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
%endif

CFLAGS="%{rpmcflags} %{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} -j1 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	SYS_OPENJPEG_CFLAGS="$(pkg-config --cflags libopenjp2)" \
	USE_SYSTEM_LIBS=yes \
	USE_SYSTEM_MUJS=yes \
	build=release \
	shared=yes \
	libdir=%{_libdir} \
	verbose=yes

sphinx-build -M html docs/src build/docs

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	USE_SYSTEM_LIBS=yes \
	USE_SYSTEM_MUJS=yes \
	build=release \
	prefix=%{_prefix} \
	libdir=%{_libdir}
%endif

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	USE_SYSTEM_LIBS=yes \
	USE_SYSTEM_MUJS=yes \
	build=release \
	shared=yes \
	prefix=%{_prefix} \
	libdir=%{_libdir}

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/mupdf

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES CONTRIBUTORS README build/docs/html/{_images,_static,*.html,*.js}
%attr(755,root,root) %{_bindir}/mupdf-gl
%attr(755,root,root) %{_bindir}/mupdf-x11
%attr(755,root,root) %{_bindir}/mupdf-x11-curl
%attr(755,root,root) %{_bindir}/muraster
%attr(755,root,root) %{_bindir}/mutool
%{_mandir}/man1/mupdf.1*
%{_mandir}/man1/mutool.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmupdf.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/mupdf

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmupdf.a
%{_libdir}/libmupdf-third.a
%endif
