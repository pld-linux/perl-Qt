#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	Qt
Summary:	Qt - A Perl module interface to Qt
Summary(pl.UTF-8):	Qt - interfejs Perla do Qt
Name:		perl-Qt
Version:	0.03
Release:	0.1
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Qt/%{pdir}-%{version}.tar.gz
# Source0-md5:	8a6c80b457edd2c85d45ef8228991a3c
URL:		http://search.cpan.org/dist/Qt/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
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

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes CREDITS INSTALL README TODO
%{perl_vendorarch}/Qt/*.pm
%dir %{perl_vendorarch}/auto/Qt/

%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
