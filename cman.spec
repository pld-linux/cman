Summary:	General-purpose symmetric cluster manager
Summary(pl):	Zarz±dca symetrycznych klastrów ogólnego przeznaczenia
Name:		cman
Version:	1.0
%define	bver	pre32
Release:	0.%{bver}.1
License:	GPL v2
Group:		Applications/System
Source0:	http://people.redhat.com/cfeist/cluster/tgz/%{name}-%{version}-%{bver}.tar.gz
# Source0-md5:	0564c8b91dfccb75de792414cccf16bd
# from cman-kernel CVS
Source1:	cnxman-socket.h
# NoSource1-md5: 5b10f050be925739f47b27ddb5075f5f (rev. 1.8)
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

%description devel
CMAN header files.

%description devel -l pl
Pliki nag³ówkowe CMAN.

%prep
%setup -q -n %{name}-%{version}-%{bver}

install -d include/cluster
cp -f %{SOURCE1} include/cluster

%{__perl} -pi -e 's/-g -O/%{rpmcflags}/' lib/Makefile
%{__perl} -pi -e 's/-g/%{rpmcflags}/' {cman_tool,tests}/Makefile

%build
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_includedir}/cluster
install include/cluster/cnxman-socket.h $RPM_BUILD_ROOT%{_includedir}/cluster

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man5/cman.5*
%{_mandir}/man8/cman_tool.8*
#%attr(754,root,root) /etc/rc.d/init.d/cman

%files devel
%defattr(644,root,root,755)
# XXX dir shared with dml-devel
%dir %{_includedir}/cluster
%{_includedir}/cluster/cnxman-socket.h
