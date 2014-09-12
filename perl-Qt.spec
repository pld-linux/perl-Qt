#
# Conditional build:
%bcond_with	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	PerlQt
Summary:	Qt - A Perl module interface to Qt
Summary(pl.UTF-8):	Qt - interfejs Perla do Qt
Name:		perl-Qt
Version:	3.008
Release:	10
License:	GPL
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Qt/%{pdir}-%{version}.tar.gz
# Source0-md5:	a0cdc0c86b3e79c56f09f2af8c4c2c39
Patch0:		format-security.patch
URL:		http://search.cpan.org/dist/Qt/
BuildRequires:	libstdc++-devel
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	qt-devel
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Qt module itself only creates a $qApp and exports some QGlobal
imports.

This module is not the whole of the Qt interface, though. Each header
in Qt which holds a class is represented by a module with the name of
that class. Classes like QWidget and QApplication are represented by
modules of the same name. QResizeEvent is not a module, but rather is
part of the QEvent module, just as the QResizeEvent class is a part of
qevent.h.

Each class header that has been interfaced to Perl has a pod attached
which describes the function interface from Qt.

%description -l pl.UTF-8
Interfejs Perla do Qt.

%prep
%setup -q -n %{pdir}-%{version}
%patch0 -p1

%{__sed} 's/ -Wmissing-prototypes / /' -i configure

%build
%{__perl} Makefile.PL \
	--prefix=%{_prefix} \
	--with-qt-dir=%{_libdir} \
	INSTALLDIRS=vendor

%configure

cd PerlQt
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
cd ..

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc INSTALL README TODO
%attr(755,root,root) %{_bindir}/pqtapi
%attr(755,root,root) %{_bindir}/pqtsh
%attr(755,root,root) %{_bindir}/puic
%{perl_vendorarch}/Qt.pm
%dir %{perl_vendorarch}/Qt
%{perl_vendorarch}/Qt/*.pm
%dir %{perl_vendorarch}/auto/Qt
%attr(755,root,root) %{perl_vendorarch}/auto/Qt/*.so
%{_mandir}/man1/puic.1*
%{_mandir}/man3/Qt.3*
%attr(755,root,root) %{_libdir}/libsmokeqt.so.*.*.*
%ghost %attr(755,root,root) %{_libdir}/libsmokeqt.so.1
