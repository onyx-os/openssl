Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: openssl
Epoch: 0
Version: 3.5.0
Release: 1%{?dist}
License: Apache-2.0
URL: https://www.openssl.org

Source: https://www.openssl.org/source/openssl-%{version}.tar.gz
Patch1: onyx-support.patch
Patch2: 0001-Do-not-install-html-docs.patch
Patch3: 0002-Override-default-paths-for-the-CA-directory-tree.patch

BuildRequires: gcc
BuildRequires: perl, zlib-devel
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description
The OpenSSL toolkit provides support for secure communications between machines.
OpenSSL includes a certificate management tool and shared libraries which provide
various cryptographic algorithms and protocols.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Requires: ca-certificates

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs package
contains the libraries that are used by various applications which support
cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which use OpenSSL
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel package
contains include files needed to develop applications which support various
cryptographic algorithms and protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Requires: perl
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Provides: deprecated()

%description perl
Perl scripts provided with OpenSSL

%prep
%autosetup -p1

%build
./config --prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls --libdir=%{_lib}
%make_build

%install
%make_install
PKITLS=$RPM_BUILD_ROOT%{_sysconfdir}/pki/tls
PKICA=$RPM_BUILD_ROOT%{_sysconfdir}/pki/CA
mkdir $PKITLS/openssl.d
mkdir -p $PKICA/private
mkdir -p $PKICA/certs
mkdir -p $PKICA/crl
mkdir -p $PKICA/newcerts
mv $PKITLS/misc/*.pl $RPM_BUILD_ROOT%{_bindir}
mv $PKITLS/misc/tsget $RPM_BUILD_ROOT%{_bindir}
rm $PKITLS/*.cnf.dist

%files
%license LICENSE.txt
%doc NEWS.md README.md
%{_bindir}/openssl
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%exclude %{_mandir}/man1/*.pl*
%exclude %{_mandir}/man1/tsget*

%files libs
%license LICENSE.txt
%{_libdir}/libcrypto.so.*
%{_libdir}/libssl.so.*
%{_libdir}/engines-*
%{_libdir}/ossl-modules
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%dir %{_sysconfdir}/pki/tls/openssl.d
%config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%config(noreplace) %{_sysconfdir}/pki/tls/ct_log_list.cnf

%files devel
%doc CHANGES.md doc/dir-locals.example.el doc/openssl-c-indent.el
%{_prefix}/include/openssl
%{_libdir}/*.so
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/cmake/OpenSSL

%files perl
%{_bindir}/c_rehash
%{_bindir}/tsget
%{_bindir}/*.pl
%{_mandir}/man1/*.pl*
%{_mandir}/man1/tsget*
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/CA/certs
%dir %{_sysconfdir}/pki/CA/crl
%dir %{_sysconfdir}/pki/CA/newcerts

