%global local_initrddir	%_initrddir
%global _sysconfdir	%_sysconfdir/eas/
%define rel 6

Summary: 	Enterprise Audit Shell
Name: 		eas
Version: 	2.0.00
Release: 	%mkrel %rel
License: 	GPL
Group: 		Shells
URL: 		https://eas.strchr.net/
BuildRequires:	openssl-devel
Source0: 	http://prdownloads.sourceforge.net/sudosh/%{name}-%{version}.tar.bz2
Source1:	eas.profile
Source2:	easd.init
Patch0:		eas-2.0.00-fix-destdir-use.patch
Patch1:		eas-2.0.00-default-user.patch
Patch2:		eas-2.0.00-fix-str-fmt.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Enterprise Audit Shell enables organizations to centrally control and audit
UNIX shell access. Audit logs are recorded and archived detailing shell input
and output, which can be played back and reviewed.

%package -n easd
Summary: 	Enterprise Audit Shell - Server
License: 	GPL
Group: 		Shells
Requires:	eash
Requires(pre):	rpm-helper

%description -n easd
Enterprise Audit Shell enables organizations to centrally control and audit
UNIX shell access. Audit logs are recorded and archived detailing shell input
and output, which can be played back and reviewed.

This package contains the server portion.

%package -n eash
Summary: 	Enterprise Audit Shell - Client shell
License: 	GPL
Group: 		Shells

%description -n eash
Enterprise Audit Shell enables organizations to centrally control and audit
UNIX shell access. Audit logs are recorded and archived detailing shell input
and output, which can be played back and reviewed.

This package contains the client (shell) portion.

%prep
%setup -q
%patch0 -p1 -b .destdir
%patch1 -p1 -b .defaultuser
%patch2 -p0 -b .str
chmod -x *.pdf

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
install -d %{buildroot}/%{_sysconfdir}
install -d %{buildroot}/etc/profile.d
%makeinstall_std
chmod u+w %{buildroot}/%{_sysconfdir}/{certs/,}*
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/etc/profile.d/eash.sh
install -d %{buildroot}/%{_logdir}/easd
install -d %{buildroot}/%{local_initrddir}
install -m 755 %{SOURCE2} %{buildroot}/%{local_initrddir}/easd

%pre -n easd
%_pre_useradd easd %{_logdir}/easd /bin/false

%post -n easd
%_post_service easd

%preun -n easd
%_preun_service easd

%postun -n easd
%_postun_userdel easd

%clean
rm -rf $RPM_BUILD_ROOT

%files -n eash
%defattr(-,root,root,-)
%{_bindir}/eas*
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/eash_config
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/certs/root.pem
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/certs/client.pem
/etc/profile.d/eash.sh

%files -n easd
%defattr(-,root,root,-)
%{_sbindir}/eas*
%attr(640,root,easd) %config(noreplace) %{_sysconfdir}/easd_config
%attr(700,easd,easd) %{_logdir}/easd
%attr(640,root,easd) %config(noreplace) %{_sysconfdir}/certs/server.pem
%{local_initrddir}/easd
%dir %{_sysconfdir}/css
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/css/*.css
%doc AUTHORS INSTALL README ChangeLog eas-mkcerts.tar EAS_Admin_Guide.pdf


# Todo:
# -better default ssl paths?
# -cron scripts for backups (db and logs)?

%{!?_with_unstable:* %(LC_ALL=C date +"%a %b %d %Y") %{packager} %{version}-%{release}}
%{!?_with_unstable: - rebuild of %{version}-%{rel}}

