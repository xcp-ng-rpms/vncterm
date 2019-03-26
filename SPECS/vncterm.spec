Summary: vncterm tty to vnc utility
Name: vncterm
Version: 10.0.0
Release: 1%{dist}
License: GPL
Group: System/Hypervisor
Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/%{name}/archive?at=v%{version}&format=tar.gz&prefix=%{name}-%{version}#/%{name}-%{version}.tar.gz
BuildRequires: xen-libs-devel systemd
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This package contains the vncterm utility

%prep
%autosetup -p1 -n vncterm-10.0.0

%build
%{?cov_wrap} %{__make}

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_libdir}/xen/bin
%{__install} -d %{buildroot}/opt/xensource/libexec
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 755 %{name} %{buildroot}%{_libdir}/xen/bin
%{__install} -m 755 dom0term/dom0term.sh %{buildroot}/opt/xensource/libexec
%{__install} -m 755 dom0term/%{name}-wrapper %{buildroot}/opt/xensource/libexec
%{__install} dom0term/dom0term.service %{buildroot}%{_unitdir}
%{__install} -d %{buildroot}%{_var}/xen/%{name}

%clean
%{__rm} -rf %{buildroot}

%pre
/usr/bin/getent passwd vncterm >/dev/null 2>&1 || /usr/sbin/useradd \
    -M -U -r \
    -s /sbin/nologin \
    -d / \
    vncterm >/dev/null 2>&1 || :
/usr/bin/getent passwd vncterm_base >/dev/null 2>&1 || /usr/sbin/useradd \
    -M -U -r \
    -s /sbin/nologin \
    -d / \
    -u 131072 \
    vncterm_base >/dev/null 2>&1 || :

%post
grep -xq 'pts/0' /etc/securetty || echo 'pts/0' >>/etc/securetty
%systemd_post dom0term.service

%preun
%systemd_preun dom0term.service

%postun
%systemd_postun_with_restart dom0term.service

%files
%defattr(-,root,root,-)
%{_libdir}/xen/bin/%{name}
/opt/xensource/libexec/dom0term.sh
/opt/xensource/libexec/%{name}-wrapper
%{_unitdir}/dom0term.service
%dir %{_var}/xen/%{name}

%changelog
