# Etersoft (c) 2007, 2008
# Multiplatform spec for autobuild system

# in kernel build dir you can have gcc_version.inc file with export GCC_VERSION=x.xx

# For build install,
# 	kernel-headers-modules-XXXX for ALT Linux
# 	kernel-devel-XXXX for FCx / ASP Linux
# 	kernel-source-stripped-XXXX for Mandriva 2007
# 	linux-headers for Debian / Ubuntu
# 	kernel-source-XXXX for SuSe
# 	kernel-source-XXXX for Slackware / MOPSLinux

Name: linux-cifs
Version: 1.53
Release: alt4

Summary: Advanced Common Internet File System for Linux with Etersoft extension

Packager: Vitaly Lipatov <lav@altlinux.ru>

License: GPL 2
Group: System/Kernel and hardware
Url: http://linux-cifs.samba.org/

Source: ftp://updates.etersoft.ru/pub/Etersoft/WINE@Etersoft/sources/tarball/%name-%version.tar.bz2
Source1: http://pserver.samba.org/samba/ftp/cifs-cvs/cifs-%version.tar.bz2

BuildRequires: rpm-build-compat >= 0.97

# Spec part for ALT Linux
%if %_vendor == "alt"
BuildRequires: kernel-build-tools
BuildRequires: kernel-headers-modules-std-smp kernel-headers-modules-wks-smp kernel-headers-modules-ovz-smp
# do not work?
%ifarch x86_64
# Don't know if ifnarch exist
BuildRequires: kernel-headers-modules-std-smp
%else
BuildRequires: kernel-headers-modules-std-pae
%endif
%endif

%if %_vendor == "suse"
# due kernel dependencies
AutoReq: no
%endif

%define module_dir /lib/modules/%name

ExclusiveOS: Linux
#ExclusiveArch: i586

%description
The CIFS VFS is a virtual file system for Linux to allow access to
servers and storage appliances compliant with the SNIA CIFS Specification
version 1.0 or later.
Popular servers such as Samba, Windows 2000, Windows XP and many others
support CIFS by default.
The CIFS VFS provides some support for older servers based on the more
primitive SMB (Server Message Block) protocol (you also can use the Linux
file system smbfs as an alternative for accessing these).
CIFS VFS is designed to take advantage of advanced network file system
features such as locking, Unicode (advanced internationalization),
hardlinks, dfs (hierarchical, replicated name space), distributed caching
and uses native TCP names (rather than RFC1001, Netbios names).

Unlike some other network file systems all key network function including
authentication is provided in kernel (and changes to mount and/or a mount
helper file are not required in order to enable the CIFS VFS). With the
addition of upcoming improvements to the mount helper (mount.cifs) the
CIFS VFS will be able to take advantage of the new CIFS URL specification
though.

This package has Etersoft's patches for WINE@Etersoft sharing access support.

#cifs-bld-tmp/fs/cifs
%define intdir new-cifs-backport

%prep
%setup -q
tar xfj %SOURCE1
patch -s -p1 -d  %intdir <%name-shared-%version.patch

%install
#export KBUILD_VERBOSE=1
MAN_DIR=%buildroot%_mandir/ INIT_DIR=%buildroot%_initdir/ SBIN_DIR=%buildroot%_sbindir/ \
	INSTALL_MOD_PATH=%buildroot/lib/modules BUILDDIR=`pwd`/%intdir  \
	DESTDIR=%buildroot SRC_DIR=%_usrsrc/%name-%version ./build.sh

%post
%post_service %name
%start_service %name

%preun
%preun_service %name

%files
%_initdir/%name
%_initdir/%name.outformat
/lib/modules/*
%_usrsrc/%name-%version/

%changelog
* Thu Jan 31 2008 Vitaly Lipatov <lav@altlinux.ru> 1.50c-alt4
- fix build on Fedora 8 (2.6.18-53)

* Sun Jan 27 2008 Vitaly Lipatov <lav@altlinux.ru> 1.50c-alt3
- move modules placement
- move src files to name-version for dkms compatibility
- change module name to etercifs.ko

* Fri Dec 28 2007 Vitaly Lipatov <lav@altlinux.ru> 1.50c-alt2
- add fix for SLED10 kernel 2.6.16.46
- fix warnings, add missed access setting in reopen file func

* Tue Nov 06 2007 Vitaly Lipatov <lav@altlinux.ru> 1.50c-alt1
- update version
- fix spec according to Korinf build system

* Fri Oct 12 2007 Vitaly Lipatov <lav@altlinux.ru> 1.50-alt1
- update version

* Fri Sep 14 2007 Sergey Lebedev <barabashka@altlinux.ru> 1.50-alt0
- new version cifs 1.50

* Fri Jul 27 2007 Vitaly Lipatov <lav@altlinux.ru> 1.48a-alt7
- fix build on 2.6.22 kernels
- fix scripts for Debian/Ubuntu

* Tue Jun 26 2007 Vitaly Lipatov <lav@altlinux.ru> 1.48a-alt6
- WINE@Etersoft 1.0.7 bugfix release
- some start script fixes, install manually build first
- fix build for kernels in symlinked build dir
- fix build on ASP Linux 2.6.9-55 kernels

* Tue Jun 19 2007 Vitaly Lipatov <lav@altlinux.ru> 1.48a-alt5
- WINE@Etersoft 1.0.7 release
- fix build on ALT ovz-smp
- fix build with 2.6.9 and older kernel
- fix build on ALT Linux 2.4
- fix caching after oplock break (eterbug #477)
- fix build with 2.6.18 on CentOS/5 and Fedora

* Sun Jun 17 2007 Vitaly Lipatov <lav@altlinux.ru> 1.48a-alt4
- WINE@Etersoft 1.0.7 rc1
- script fixes

* Thu Jun 14 2007 Vitaly Lipatov <lav@altlinux.ru> 1.48a-alt3
- WINE@Etersoft 1.0.7 beta
- fix inode revalidate for read requests
- fix build module scripts

* Tue Jun 12 2007 Vitaly Lipatov <lav@altlinux.ru> 1.48a-alt2
- WINE@Etersoft 1.0.7 alpha

* Fri Jun 08 2007 Vitaly Lipatov <lav@altlinux.ru> 1.48a-alt1
- initial build for WINE@Etersoft project
