#
# Conditional build:
%bcond_with     libonly		# build package only with lib (needed bootstrap with ccs)
#
Summary:	General-purpose symmetric cluster manager
Summary(pl.UTF-8):	Zarządca symetrycznych klastrów ogólnego przeznaczenia
Name:		cman
Version:	2.00.00
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/cluster/releases/cluster-%{version}.tar.gz
# Source0-md5:	2ef3f4ba9d3c87b50adfc9b406171085
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://sources.redhat.com/cluster/cman/
%{!?with_libonly:BuildRequires:	ccs-devel}
BuildRequires:	openais-devel
BuildRequires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
MAN is a symmetric, general-purpose, kernel-based cluster manager. It
has two parts. Connection Manager (cnxman) handles membership,
messaging, quorum, event notification and transitions. Service Manager
(sm) handles "service groups" which are a general way of representing
and managing instances of external systems that require cluster
management. The CMAN cluster manager is the foundational system upon
which DLM, GFS, CLVM, and Fence all depend. The CMAN API in the kernel
and userspace is general and available for other programs to use.

%description -l pl.UTF-8
MAN to zarządca opartych na jądrze symetrycznych klastrów ogólnego
przeznaczenia. Składa się z dwóch części. Zarządca połączeń
(Connection Manager, cnxman) obsługuje członkostwo, komunikację,
kworum, powiadamianie o zdarzeniach i przejścia. Zarządca usług
(Service Manager, sm) obsługuje "grupy usług", które są ogólnym
sposobem reprezentacji i zarządzania instancjami zewnętrznych systemów
wymagających zarządzania klastrem. Zarządca klastrów CMAN to
podstawowy system, na którym polegają DLM, GFS, CLVM i Fence. API
CMAN-a w jądrze i przestrzeni użytkownika jest ogólne i w całości
dostępne do wykorzystania w innych programach.

%package devel
Summary:	CMAN header files
Summary(pl.UTF-8):	Pliki nagłówkowe CMAN
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
CMAN header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe CMAN.

%package static
Summary:	CMAN static library
Summary(pl.UTF-8):	Biblioteka statyczna CMAN
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
CMAN static library.

%description devel -l pl.UTF-8
Biblioteka statyczna CMAN.

%prep
%setup -q -n cluster-%{version}

cd %{name}
%{__perl} -pi -e 's/-g -O/%{rpmcflags}/' lib/Makefile
%{__perl} -pi -e 's/-g/%{rpmcflags}/' {cman_tool,tests}/Makefile

%build
cd %{name}
./configure \
	--ccsincdir="$PWD/../ccs/lib" \
	--incdir=%{_includedir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}
%{__make} %{?with_libonly:-C lib} \
	CC="%{__cc}" \
	incdir=`pwd`/include

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig,/etc/rc.d/init.d}
cd %{name}

%{__make} %{?with_libonly:-C lib} install \
	DESTDIR=$RPM_BUILD_ROOT

install %SOURCE1 $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %SOURCE2 $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	
/sbin/ldconfig
/sbin/chkconfig --add %{name}

%postun	-p /sbin/ldconfig

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{!?with_libonly:%attr(755,root,root) %{_sbindir}/*}
%attr(755,root,root) %{_libdir}/libcman.so.*.*
%if %{without libonly}
%attr(755,root,root) %{_libdir}/lcrso/service_cman.lcrso
%{_mandir}/man5/cman.5*
%{_mandir}/man5/qdisk.5*
%{_mandir}/man8/cman_tool.8*
%{_mandir}/man8/mkqdisk.8*
%{_mandir}/man8/qdiskd.8*
#%attr(754,root,root) /etc/rc.d/init.d/cman
#%attr(754,root,root) /etc/rc.d/init.d/qdiskd
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%attr(755,root,root) %{_libdir}/libcman.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libcman.a
