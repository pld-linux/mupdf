Summary:	MuPDF - lightweight PDF, XPS and CBZ viewer and parser/rendering library
Summary(pl.UTF-8):	MuPDF - lekka przeglądarka PDF, XPS, CBZ
Name:		mupdf
Version:	1.13.0
Release:	2
License:	AGPL v3+
Group:		Applications/Text
Source0:	http://www.mupdf.com/downloads/%{name}-%{version}-source.tar.gz
# Source0-md5:	447bc5c3305efe9645e12fce759e0198
URL:		http://www.mupdf.com/
BuildRequires:	OpenGL-glut-devel
BuildRequires:	curl-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	glfw-devel
BuildRequires:	jbig2dec-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	mujs-devel >= 1.0.4
BuildRequires:	openjpeg2-devel >= 2.1.0
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	zlib-devel
Obsoletes:	mpudf-devel < 1.13.0
Obsoletes:	mpudf-libs < 1.13.0
Obsoletes:	mpudf-static < 1.13.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MuPDF is a lightweight PDF, XPS and CBZ viewer.

%description -l pl.UTF-8
MuPDF to lekka przeglądarka pliki PDF, XPS i CBZ.

%prep
%setup -q -n %{name}-%{version}-source

# use system libs instead
%{__rm} -r thirdparty/{curl,freetype,jbig2dec,libjpeg,mujs,openjpeg,zlib}

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} -j1 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	HAVE_MUJS=yes \
	MUJS_CFLAGS= \
	MUJS_LIBS="-lmujs" \
	SYS_OPENJPEG_CFLAGS="$(pkg-config --cflags libopenjp2)" \
	build=release \
	libdir=%{_libdir} \
	verbose=yes

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HAVE_MUJS=yes \
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
