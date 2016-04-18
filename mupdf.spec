#
# Conditional build:
%bcond_with	v8	# use V8 JS engine instead of MuJS
#
Summary:	MuPDF - lightweight PDF, XPS and CBZ viewer and parser/rendering library
Summary(pl.UTF-8):	MuPDF - lekka przeglądarka oraz biblioteka renderująca PDF, XPS, CBZ
Name:		mupdf
Version:	1.8
Release:	1
License:	AGPL v3+
Group:		Applications/Text
Source0:	http://www.mupdf.com/downloads/%{name}-%{version}-source.tar.gz
# Source0-md5:	3205256d78d8524d67dd2a47c7a345fa
Patch0:		%{name}-openjpeg.patch
Patch1:		%{name}-shared.patch
Patch2:		%{name}-mujs.patch
URL:		http://www.mupdf.com/
BuildRequires:	OpenGL-glut-devel
BuildRequires:	curl-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	glfw-devel
BuildRequires:	jbig2dec-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
%{!?with_v8:BuildRequires:	mujs-devel >= 0-0.20160302}
BuildRequires:	openjpeg2-devel >= 2.1.0
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
%{?with_v8:BuildRequires:	v8-devel}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MuPDF is a lightweight PDF, XPS and CBZ viewer and parser/rendering
library.

%description -l pl.UTF-8
MuPDF to lekka przeglądarka oraz biblioteka analizująca/renderująca
pliki PDF, XPS i CBZ.

%package libs
Summary:	Shared MuPDF libraries
Summary(pl.UTF-8):	Biblioteki współdzielone MuPDF
Group:		Libraries

%description libs
Shared MuPDF libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone MuPDF.

%package devel
Summary:	Header files for MuPDF libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek MuPDF
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	freetype-devel >= 2
Requires:	jbig2dec-devel
Requires:	libjpeg-devel
Requires:	libstdc++-devel
%{!?with_v8:Requires:	mujs-devel}
Requires:	openjpeg2-devel >= 2.1.0
Requires:	openssl-devel
%{?with_v8:Requires:	v8-devel}
Requires:	zlib-devel

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
%patch2 -p1

# use system libs instead
%{__rm} -r thirdparty/{curl,freetype,glfw,jbig2dec,jpeg,mujs,openjpeg,zlib}

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} -j1 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
%if %{with v8}
	HAVE_V8=yes \
	V8_CFLAGS= \
	V8_LIBS="-lv8 -lstdc++" \
%else
	HAVE_MUJS=yes \
	MUJS_CFLAGS= \
	MUJS_LIBS="-lmujs" \
%endif
	SYS_OPENJPEG_CFLAGS="$(pkg-config --cflags libopenjp2)" \
	build=release \
	libdir=%{_libdir} \
	verbose=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	V8_PRESENT=yes \
	build=release \
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
%doc CHANGES CONTRIBUTORS README
%attr(755,root,root) %{_bindir}/mujstest
%attr(755,root,root) %{_bindir}/mupdf-x11
%attr(755,root,root) %{_bindir}/mupdf-x11-curl
%attr(755,root,root) %{_bindir}/mutool
%{_mandir}/man1/mupdf.1*
%{_mandir}/man1/mutool.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmupdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmupdf.so.0

%files devel
%defattr(644,root,root,755)
%doc docs/{naming,overview,progressive,refcount,thirdparty}.txt
%attr(755,root,root) %{_libdir}/libmupdf.so
%{_libdir}/libmupdf.la
%{_includedir}/mupdf

%files static
%defattr(644,root,root,755)
%{_libdir}/libmupdf.a
