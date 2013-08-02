%define	debug_package %{nil}

Summary:	A set of system configuration, setup files and directories
Name:		setup-ARM
Version:	2.7.22
Release:	2
License:	Public Domain
Group:		System/Base
Url:		https://abf.rosalinux.ru/moondrake/setup
Source0:	%{name}-%{version}.tar.xz
Source1:	setup-ARM.rpmlintrc
Provides:	setup
ExcludeArch:	%{ix86} x86_64
%rename		filesystem

#Requires:	shadow-utils
Requires(posttrans):	qemu-static-hack
Requires(posttrans):	shadow-conv
Requires(posttrans):	glibc

%description
The setup package contains a set of very important system configuration, setup 
files and directories, such as passwd, group, profile, basic directory layout
for a Linux system and more.

The filesystem is one of the basic packages that is installed on a Linux 
system.  Filesystem  contains the basic directory layout for a Linux operating 
system, including the correct permissions for the directories.

%prep
%setup -q -n setup-%{version}

%build
%make

%install
%makeinstall_std

# from filesystem

mkdir -p %{buildroot}/%{_lib}
mkdir -p %{buildroot}/%{_libdir}

mkdir -p %{buildroot}/{mnt,media,bin,boot,dev}
mkdir -p %{buildroot}/{opt,proc,root,sbin,srv,sys,tmp}
mkdir -p %{buildroot}/{home,initrd}
mkdir -p %{buildroot}/lib/modules

mkdir -p %{buildroot}%{_sysconfdir}/{profile.d,security,ssl,sysconfig,default,opt,xinetd.d}

mkdir -p %{buildroot}%{_prefix}/{etc,src,lib}
mkdir -p %{buildroot}/{%{_bindir},%{_includedir},%{_sbindir},%{_datadir}}
mkdir -p %{buildroot}/%{_datadir}/{misc,pixmaps,applications,desktop-directories,dict,doc,empty,fonts}
mkdir -p %{buildroot}/%{_datadir}/color/{icc,cmms,settings}

# man
mkdir -p %{buildroot}/%{_mandir}/man{1,2,3,4,5,6,7,8,9,n}
mkdir -p %{buildroot}/%{_infodir}

# games
mkdir -p %{buildroot}/{%{_gamesbindir},%{_gamesdatadir}}
mkdir -p %{buildroot}/{%{_libdir},%{_prefix}/lib}/games

mkdir -p %{buildroot}/{%{_libdir},%{_prefix}/lib}/gcc-lib

mkdir -p %{buildroot}/usr/local/{bin,doc,etc,games,lib,%{_lib},sbin,src,libexec,include}
mkdir -p %{buildroot}/usr/local/share/{applications,desktop-directories}
mkdir -p %{buildroot}/usr/local/share/{man/man{1,2,3,4,5,6,7,8,9,n},info}
mkdir -p %{buildroot}/usr/share/ppd

mkdir -p %{buildroot}/var/{adm,local,log,nis,preserve,run,lib,empty}
mkdir -p %{buildroot}/var/spool/{lpd,mail,news,uucp}
mkdir -p %{buildroot}/var/lib/{games,misc}
mkdir -p %{buildroot}/var/{tmp,db,cache/man,opt,games,yp}
mkdir -p %{buildroot}/var/lock/subsys

pushd %{buildroot}
ln -snf ../var/tmp usr/tmp
ln -snf spool/mail var/mail
popd

%posttrans
pwconv 2>/dev/null >/dev/null  || :
grpconv 2>/dev/null >/dev/null  || :

[ -f /var/log/lastlog ] || echo -n '' > /var/log/lastlog

if [ -x /usr/sbin/nscd ]; then
	nscd -i passwd -i group || :
fi

%files

# setup
%doc NEWS
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/passwd
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/fstab
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/resolv.conf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/group
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/hosts
%config(noreplace) %{_sysconfdir}/services
%config(noreplace) %{_sysconfdir}/inputrc
%config(noreplace) %{_sysconfdir}/filesystems
%config(noreplace) %{_sysconfdir}/host.conf
%config(noreplace) %{_sysconfdir}/hosts.allow
%config(noreplace) %{_sysconfdir}/hosts.deny
%config(noreplace) %{_sysconfdir}/motd
%config(noreplace) %{_sysconfdir}/printcap
%config(noreplace) %{_sysconfdir}/profile
%config(noreplace) %{_sysconfdir}/shells
%config(noreplace) %{_sysconfdir}/protocols
%attr(0644,root,root) %config(missingok,noreplace) %{_sysconfdir}/securetty
%config(noreplace) %{_sysconfdir}/csh.login
%config(noreplace) %{_sysconfdir}/csh.cshrc
%ghost %verify(not md5 size mtime) /var/log/lastlog

# from filesystem
%defattr(0755,root,root)
/bin
/dev
/boot
%dir /etc
/home
/initrd
/lib
%if %{_lib} != lib
/%{_lib}
%endif
%dir /media
%dir /mnt
%dir /opt
/proc
/srv
/sys
%attr(750,root,root) /root
/sbin
%attr(1777,root,root) /tmp
%{_prefix}
%dir /var
/var/adm
/var/db
/var/lib
/var/local
/var/empty
%dir %attr(775,root,uucp) /var/lock
/var/lock/subsys
/var/cache
%dir /var/log
/var/mail
/var/nis
/var/opt
/var/preserve
/var/run
%dir /var/spool
%dir %attr(0755,root,daemon) /var/spool/lpd
%attr(775,root,mail) /var/spool/mail
%attr(1777,root,root) /var/tmp
%attr(775,root,news) /var/spool/news
%attr(775,root,uucp) /var/spool/uucp
/var/yp

%changelog
* Wed Feb 07 2013 Matthew Dawkins <mattydaw@mandriva.org> 2.7.21-8
- merged filesystem into setup

* Mon Jan 14 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.7.21-7
- drop oldass scriptlets

* Sun Jan 13 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.7.21-6
- change %%pre to %%post scriptlet to avoid failure to install package in case
  scriptlet fails

* Sun Jan 13 2013 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.7.21-5
- drop prereqs on grep & rpm-helper to ease up on dependency loops, when
  they're actually needed, rpm-helper is sure to already be installed anyways

* Sun Sep 09 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.7.21-2
+ Revision: 816563
- drop dependency on run-parts, we haven't shipped it as part of this package
  for a while, so no sense in adding a dependency on it for legacy compatibility
- new version:
  	o don't create /etc/mtab
  	o remove run-parts from this package, it's packaged separately
  	o update /etc/protocols and /etc/services from debian package
  	  netbase 4.47
- drop redundant glibc dependency
- fix license tag
- drop redundant buildroot cleaning
- cosmetics
- change buildarch to noarch
- add Requires(pre): rpm-helper

* Tue May 29 2012 Guilherme Moro <guilherme@mandriva.com> 2.7.18-5
+ Revision: 801039
- Remove mtab, owned by util-linux now

* Sun Dec 11 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.7.18-4
+ Revision: 740166
- cleaned up spec
- removed defattr, clean section, BuildRoot, mkrel
- changed req for shadow-utils to shadow-conv
- (recently split to avoid dep loop)
- removed pre 2007 Conflicts
- removed reqs for run-parts

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2.7.18-3
+ Revision: 669970
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.7.18-2mdv2011.0
+ Revision: 607533
- rebuild

* Thu Dec 31 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.7.18-1mdv2010.1
+ Revision: 484524
- new version

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.7.17-2mdv2010.0
+ Revision: 427069
- rebuild

* Sat Apr 11 2009 Gustavo De Nardin <gustavodn@mandriva.com> 2.7.17-1mdv2009.1
+ Revision: 366419
- 2.7.17
  - stop csh from sourcing /etc/profile.d/* on non-interactive shells
    (bug #49407, comment 6)

* Fri Jan 09 2009 Frederic Crozat <fcrozat@mandriva.com> 2.7.16-1mdv2009.1
+ Revision: 327455
- Release 2.7.16 :
 - add dialout group, needed by latest udev, replace uucp group for serial stuff, just like Debian

* Wed Jan 07 2009 Pixel <pixel@mandriva.com> 2.7.15-1mdv2009.1
+ Revision: 326531
- 2.7.15: handle control + left/right arrow in gnome-terminal (#36287)

* Wed Dec 17 2008 Frederic Crozat <fcrozat@mandriva.com> 2.7.14-1mdv2009.1
+ Revision: 315121
- Release 2.7.14 :
 - fix warning in run-parts
 - configure inputrc to add trailing / to directories symlink (instead of patching bash)

* Sat Jul 12 2008 Olivier Thauvin <nanardon@mandriva.org> 2.7.13-1mdv2009.0
+ Revision: 234201
- 2.7.13: add tty0 to securetty for uml

* Thu May 22 2008 Vincent Danen <vdanen@mandriva.com> 2.7.12-3mdv2009.0
+ Revision: 210051
- use %%_pre_groupadd instead of groupadd directly to dynamically assign gid's on upgrades, since those gid's may already have been taken

* Sun May 18 2008 Vincent Danen <vdanen@mandriva.com> 2.7.12-2mdv2009.0
+ Revision: 208736
- create shadow, chkpwed, and auth groups in %%pre if they don't already exist in the system

* Wed May 14 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.7.12-1mdv2009.0
+ Revision: 207315
- new version

* Fri Mar 28 2008 Pixel <pixel@mandriva.com> 2.7.11-3mdv2008.1
+ Revision: 190933
- require run-parts for backward compatibility until other packages correctly
  require it directly

* Fri Mar 28 2008 Pixel <pixel@mandriva.com> 2.7.11-2mdv2008.1
+ Revision: 190867
- run-parts is moved to package run-parts

* Mon Jan 28 2008 Marcelo Ricardo Leitner <mrl@mandriva.com> 2.7.11-1mdv2008.1
+ Revision: 159330
- New upstream: 2.7.11. Closes: #34841
- Update URL tag.

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Dec 12 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.7.10-1mdv2008.1
+ Revision: 119058
- new version

* Tue Sep 11 2007 Oden Eriksson <oeriksson@mandriva.com> 2.7.9-2mdv2008.0
+ Revision: 84515
- rebuild

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - new release

