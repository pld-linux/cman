Summary:	General-purpose symmetric cluster manager
Summary(pl):	Zarz±dca symetrycznych klastrów ogólnego przeznaczenia
Name:		cman
Version:	1.03.00
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/cluster/releases/cluster-%{version}.tar.gz
# Source0-md5:	8eea23df70d2007c4fb8c234cfea49cf
URL:		http://sources.redhat.com/cluster/cman/
BuildRequires:	ccs-devel
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

%description -l pl
MAN to zarz±dca opartych na j±drze symetrycznych klastrów ogólnego
przeznaczenia. Sk³ada siê z dwóch czê¶ci. Zarz±dca po³±czeñ
(Connection Manager, cnxman) obs³uguje cz³onkostwo, komunikacjê,
kworum, powiadamianie o zdarzeniach i przej¶cia. Zarz±dca us³ug
(Service Manager, sm) obs³uguje "grupy us³ug", które s± ogólnym
sposobem reprezentacji i zarz±dzania instancjami zewnêtrznych systemów
wymagaj±cych zarz±dzania klastrem. Zarz±dca klastrów CMAN to
podstawowy system, na którym polegaj± DLM, GFS, CLVM i Fence. API
CMAN-a w j±drze i przestrzeni u¿ytkownika jest ogólne i w ca³o¶ci
dostêpne do wykorzystania w innych programach.

%package devel
Summary:	CMAN header files
Summary(pl):	Pliki nag³ówkowe CMAN
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
CMAN header files.

%description devel -l pl
Pliki nag³ówkowe CMAN.

%package static
Summary:	CMAN static library
Summary(pl):	Biblioteka statyczna CMAN
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
CMAN static library.

%description devel -l pl
Biblioteka statyczna CMAN.

%prep
%setup -q -n cluster-%{version}
install -d %{name}/include/cluster
ln -s . %{name}/include/cluster/cluster
install %{name}-kernel/src/cnxman-socket.h %{name}/include/cluster

cd %{name}
%{__perl} -pi -e 's/-g -O/%{rpmcflags}/' lib/Makefile
%{__perl} -pi -e 's/-g/%{rpmcflags}/' {cman_tool,tests}/Makefile

%build
cd %{name}
./configure \
	--incdir=%{_includedir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}
%{__make} \
	CC="%{__cc}" \
	incdir=`pwd`/include

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_includedir}/cluster
install include/cluster/cnxman-socket.h $RPM_BUILD_ROOT%{_includedir}/cluster

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/libcman.so.*.*
%{_mandir}/man5/cman.5*
%{_mandir}/man8/cman_tool.8*
#%attr(754,root,root) /etc/rc.d/init.d/cman

%files devel
%defattr(644,root,root,755)
# XXX dir shared with dml-devel
%dir %{_includedir}/cluster
%{_includedir}/*.h
%{_includedir}/cluster/*.h
%attr(755,root,root) %{_libdir}/libcman.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libcman.a
