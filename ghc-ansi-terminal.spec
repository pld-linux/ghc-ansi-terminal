#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	ansi-terminal
Summary:	Simple ANSI terminal support
Name:		ghc-%{pkgname}
Version:	0.6.2.3
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/ansi-terminal
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	8afe9864ce4600841a83febb40a2c753
URL:		http://hackage.haskell.org/package/ansi-terminal
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-unix >= 2.3.0.0
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-unix-prof >= 2.3.0.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4
Requires:	ghc-base < 5
Requires:	ghc-unix >= 2.3.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
ANSI terminal support for Haskell: allows cursor movement, screen
clearing, color output showing or hiding the cursor, and changing the
title. 

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-prof >= 6.12.3
Requires:	ghc-base-prof >= 4
Requires:	ghc-base-prof < 5

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSansi-terminal-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSansi-terminal-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/ANSI
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/ANSI/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSansi-terminal-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/Console/ANSI/*.p_hi
%endif
