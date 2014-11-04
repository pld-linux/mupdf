Summary:	MuPDF - lightweight PDF, XPS and CBZ viewer and parser/rendering library
Summary(pl.UTF-8):	MuPDF - lekka przeglądarka oraz biblioteka renderująca PDF, XPS, CBZ
Name:		mupdf
Version:	1.3
Release:	2
License:	AGPL v3+
Group:		Applications/Text
#Source0Download: http://code.google.com/p/mupdf/downloads/list?q=source
Source0:	http://mupdf.googlecode.com/files/%{name}-%{version}-source.tar.gz
# Source0-md5:	fe53c2a56ebd7759f5f965bc4ff66359
Patch0:		%{name}-openjpeg.patch
Patch1:		%{name}-curl.patch
Patch2:		%{name}-v8.patch
Patch3:		%{name}-shared.patch
URL:		http://www.mupdf.com/
BuildRequires:	curl-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	jbig2dec-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	openjpeg2-devel >= 2
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	v8-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# needs symbols from one of libmupdf-js-*
%define		skip_post_check_so	libmupdf.so.*

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
Requires:	openjpeg2-devel >= 2
Requires:	openssl-devel
Requires:	v8-devel
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
%patch3 -p1

# use system libs instead
%{__rm} -r thirdparty/{curl,freetype,jbig2dec,jpeg,openjpeg,zlib}

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	V8_PRESENT=yes \
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
%attr(755,root,root) %{_bindir}/mudraw
%attr(755,root,root) %{_bindir}/mujstest-v8
%attr(755,root,root) %{_bindir}/mupdf-x11
%attr(755,root,root) %{_bindir}/mupdf-x11-curl
%attr(755,root,root) %{_bindir}/mupdf-x11-v8
%attr(755,root,root) %{_bindir}/mutool
%{_mandir}/man1/mudraw.1*
%{_mandir}/man1/mupdf.1*
%{_mandir}/man1/mutool.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmupdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmupdf.so.0
%attr(755,root,root) %{_libdir}/libmupdf-js-none.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmupdf-js-none.so.0
%attr(755,root,root) %{_libdir}/libmupdf-js-v8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmupdf-js-v8.so.0

%files devel
%defattr(644,root,root,755)
%doc docs/{naming,overview,progressive,refcount,thirdparty}.txt
%attr(755,root,root) %{_libdir}/libmupdf.so
%attr(755,root,root) %{_libdir}/libmupdf-js-none.so
%attr(755,root,root) %{_libdir}/libmupdf-js-v8.so
%{_libdir}/libmupdf.la
%{_libdir}/libmupdf-js-none.la
%{_libdir}/libmupdf-js-v8.la
%{_includedir}/mupdf

%files static
%defattr(644,root,root,755)
%{_libdir}/libmupdf.a
%{_libdir}/libmupdf-js-none.a
%{_libdir}/libmupdf-js-v8.a
