Summary:	General-purpose symmetric cluster manager
Summary(pl):	Zarz�dca symetrycznych klastr�w og�lnego przeznaczenia
Name:		cman
%define	snap	20040625
Version:	0.0.0.%{snap}.1
Release:	1
License:	GPL
Group:		Applications/System
Source0:	%{name}.tar.gz
# Source0-md5:	76edec5d961fd1cf46ccac2b7b006f37
URL:		http://sources.redhat.com/cluster/
BuildRequires:	ccs-devel
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
MAN to zarz�dca opartych na j�drze symetrycznych klastr�w og�lnego
przeznaczenia. Sk�ada si� z dw�ch cz�ci. Zarz�dca po��cze�
(Connection Manager, cnxman) obs�uguje cz�onkostwo, komunikacj�,
kworum, powiadamianie o zdarzeniach i przej�cia. Zarz�dca us�ug
(Service Manager, sm) obs�uguje "grupy us�ug", kt�re s� og�lnym
sposobem reprezentacji i zarz�dzania instancjami zewn�trznych system�w
wymagaj�cych zarz�dzania klastrem. Zarz�dca klastr�w CMAN to
podstawowy system, na kt�rym polegaj� DLM, GFS, CLVM i Fence. API
CMAN-a w j�drze i przestrzeni u�ytkownika jest og�lne i w ca�o�ci
dost�pne do wykorzystania w innych programach.

%prep
%setup -q -n %{name}

%build
./configure \
	--incdir=%{_includedir} \
	--kernel_src=%{_kernelsrcdir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
