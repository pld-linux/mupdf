# TODO: build shared library
Summary:	MuPDF - lightweight PDF, XPS and CBZ viewer and parser/rendering library
Summary(pl.UTF-8):	MuPDF - lekka przeglądarka oraz biblioteka renderująca PDF, XPS, CBZ
Name:		mupdf
Version:	1.3
Release:	0.1
License:	AGPL v3
Group:		Libraries
#Source0Download: http://code.google.com/p/mupdf/downloads/list?q=source
Source0:	http://mupdf.googlecode.com/files/%{name}-%{version}-source.tar.gz
# Source0-md5:	fe53c2a56ebd7759f5f965bc4ff66359
Patch0:		%{name}-openjpeg.patch
Patch1:		%{name}-curl.patch
Patch2:		%{name}-v8.patch
URL:		http://www.mupdf.com/
BuildRequires:	curl-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	jbig2dec-devel
BuildRequires:	libjpeg-devel
BuildRequires:	openjpeg2-devel >= 2
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	v8-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MuPDF is a lightweight PDF, XPS and CBZ viewer and parser/rendering
library.

%description -l pl.UTF-8
MuPDF to lekka przeglądarka oraz biblioteka analizująca/renderująca
pliki PDF, XPS i CBZ.

%package devel
Summary:	Header files for MuPDF library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki MuPDF
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for MuPDF library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki MuPDF.

%package static
Summary:	Static MuPDF library
Summary(pl.UTF-8):	Statyczna biblioteka MuPDF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MuPDF library.

%description static -l pl.UTF-8
Statyczna biblioteka MuPDF.

%prep
%setup -q -n %{name}-%{version}-source
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__rm} -r thirdparty/{curl,freetype,jbig2dec,jpeg,openjpeg,zlib}

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__make} \
	CC="%{__cc}" \
	V8_PRESENT=yes \
	build=release

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

#%post	-p /sbin/ldconfig
#%postun	-p /sbin/ldconfig

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

%files devel
%defattr(644,root,root,755)
%doc docs/{naming,overview,progressive,refcount,thirdparty}.txt
%{_libdir}/libmupdf.a
%{_libdir}/libmupdf-js-none.a
%{_libdir}/libmupdf-js-v8.a
%{_includedir}/mupdf

%if 0
%files static
%defattr(644,root,root,755)
%{_libdir}/libmupdf.a
%{_libdir}/libmupdf-js-none.a
%{_libdir}/libmupdf-js-v8.a
%endif
