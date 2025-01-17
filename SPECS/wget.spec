Summary: A utility for retrieving files using the HTTP or FTP protocols
Name: wget
Version: 1.12
Release: 10%{?dist}
License: GPLv3+ and GFDL
Group: Applications/Internet
Url: http://www.gnu.org/software/wget/
Source: ftp://ftp.gnu.org/gnu/wget/wget-%{version}.tar.bz2

Patch1: wget-rh-modified.patch
Patch2: wget-1.12-path.patch
Patch3: wget-1.12-openssl_timeout.patch
Patch4: wget-1.12-fuzzed_response_seg_fault.patch
Patch5: wget-1.12-bz736445.patch
Patch6: wget-1.12-trust-server-names-option.patch
Patch7: wget-1.12-tls_sni_support.patch
Patch8: wget-1.12-parse-weblink-recursive.patch
Patch9: wget-1.12-Coverity-scan-errors-fixes.patch
Patch10: wget-1.12-CVE-2014-4877.patch
Patch11: wget-1.12-rh1328458.patch
Patch12: wget-1.12-mschret0.patch

Provides: webclient
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
# needed for test suite
BuildRequires: perl-libwww-perl, perl-IO-Socket-SSL
BuildRequires: openssl-devel, pkgconfig, texinfo, gettext, autoconf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
GNU Wget is a file retrieval utility which can use either the HTTP or
FTP protocols. Wget features include the ability to work in the
background while you are logged out, recursive retrieval of
directories, file name wildcard matching, remote file timestamp
storage and comparison, use of Rest with FTP servers and Range with
HTTP servers to retrieve files over slow or unstable connections,
support for Proxy servers, and configurability.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .ssl_timeout
%patch4 -p1 -b .fuzzed
%patch5 -p1 -b .subjectAltName
%patch6 -p1 -b .CVE-2010-2252
%patch7 -p1 -b .sni_support
%patch8 -p1 -b .weblink
%patch9 -p1 -b .coverity
%patch10 -p1 -b .CVE-2014-4877
%patch11 -p1 -b .rh1328458
%patch12 -p1 -b .mschret0

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
if pkg-config openssl ; then
    CPPFLAGS=`pkg-config --cflags openssl`; export CPPFLAGS
    LDFLAGS="-Wl,-z,relro `pkg-config --libs openssl`"; export LDFLAGS
fi
%configure --with-ssl --enable-largefile --enable-opie --enable-digest --enable-ntlm --enable-nls --enable-ipv6 --disable-rpath --disable-iri
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT CFLAGS="$RPM_OPT_FLAGS"
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%find_lang %{name}

%post
/sbin/install-info %{_infodir}/wget.info.gz %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/wget.info.gz %{_infodir}/dir || :
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS MAILING-LIST NEWS README COPYING doc/sample.wgetrc
%config(noreplace) %{_sysconfdir}/wgetrc
%{_mandir}/man1/wget.*
%{_bindir}/wget
%{_infodir}/*

%check
make check


%changelog
* Tue Oct 04 2016 Petr Menšík <pemensik@redhat.com> - 1.12-10
- #1166699 - 0 return code when url missing scheme

* Mon Oct 03 2016 Petr Menšík <pemensik@redhat.com> - 1.12-9
- Fix wget to include Host header on CONNECT as required by HTTP 1.1 (#1328458)

* Fri Jan 08 2016 Tomas Hozza <thozza@redhat.com> - 1.12-8
- Added build dependency needed to run HTTP unit tests (Related #1295847)
- Explicitly disabled IDN/IRI support during build due to QA TPS test failures (Related #1295847)

* Wed Jan 06 2016 Tomas Hozza <thozza@redhat.com> - 1.12-7
- Run test suite during build (#1295847)

* Fri Oct 24 2014 Tomas Hozza <thozza@redhat.com> - 1.12-6
- Fix CVE-2014-4877 wget: FTP symlink arbitrary filesystem access (#1156134)

* Wed Apr 02 2014 Tomas Hozza <thozza@redhat.com> 1.12-5
- Fix the parsing of weblink when doing recursive retrieving (#960137)
- Fix errors found by static analysis of source code (#873216)

* Tue Apr 01 2014 Tomas Hozza <thozza@redhat.com> 1.12-4
- Add SNI (Server Name Indication) support (#909604)

* Thu Feb 06 2014 Tomas Hozza <thozza@redhat.com> 1.12-3
- Add --trust-server-names option to fix CVE-2010-2252 (#1062190)

* Fri Jan 31 2014 Tomas Hozza <thozza@redhat.com> 1.12-2
- Fix wget to recognize certificates with alternative names (#736445)

* Mon Oct 01 2012 Tomas Hozza <thozza@redhat.com> 1.12-1.8
- Fixed wget from fuzzed http ending with segmentation fault (#714893)

* Thu Sep 27 2012 Tomas Hozza <thozza@redhat.com> 1.12-1.7
- Fixed timeout issue when using SSL and server doesn't answer (#814208)

* Fri Sep 21 2012 Tomas Hozza <thozza@redhat.com> 1.12-1.6
- Added gcc flag -fno-strict-aliasing to solve Testsuite regressions

* Fri Sep 21 2012 Tomas Hozza <thozza@redhat.com> 1.12-1.5
- Corrected upstream URL in SPEC file (#754168)

* Mon May 10 2010 Karsten Hopp <karsten@redhat.com> 1.12-1.4
- rebuild to fix bad dwarf cfi expressions caused by an older gcc

* Tue Feb 23 2010 Karsten Hopp <karsten@redhat.com> 1.12-1.3
- added GFDL to licenses

* Wed Nov 25 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.12-1.2
- don't provide /usr/share/info/dir

* Mon Nov 23 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.12-1.1
- Rebuilt for RHEL 6

* Tue Nov 17 2009 Karsten Hopp <karsten@redhat.com> 1.12-1
- update to wget-1.12
- fixes CVE-2009-3490 wget: incorrect verification of SSL certificate
  with NUL in name

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.11.4-5
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> 1.11.4-2
- rebuild with new openssl

* Wed Aug 13 2008 Karsten Hopp <karsten@redhat.com> 1.11.4-1
- update

* Wed Jun 04 2008 Karsten Hopp <karsten@redhat.com> 1.11.3-1
- wget-1.11.3, downgrades the combination of the -N and -O options
  to a warning instead of an error

* Fri May 09 2008 Karsten Hopp <karsten@redhat.com> 1.11.2-1
- wget-1.11.2, fixes #179962

* Mon Mar 31 2008 Karsten Hopp <karsten@redhat.com> 1.11.1-1
- update to bugfix release 1.11.1, fixes p.e. #433606

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.11-2
- Autorebuild for GCC 4.3

* Tue Dec 04 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-17
- rebuild to pick up new openssl SONAME

* Mon Aug 27 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-16
- fix license tag
- rebuild

* Mon Feb 12 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-15
- fix discarding of expired cookies
- escape non-printable characters
- drop to11 patch for now (#223754, #227853, #227498)

* Mon Feb 05 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-14
- shut up rpmlint, even though xx isn't a macro

* Mon Feb 05 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-13
- merge review changes (#226538)
  - use version/release/... in buildroot tag
  - remove BR perl
  - use SMP flags
  - use make install instead of %%makeinstall
  - include copy of license
  - use Requires(post)/Requires(preun)
  - use optflags
  - remove trailing dot from summary
  - change tabs to spaces

* Thu Jan 18 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-12
- don't abort (un)install scriptlets when _excludedocs is set (Ville Skyttä)

* Wed Jan 10 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-11
- add fix for CVE-2006-6719

* Thu Dec 08 2006 Karsten Hopp <karsten@redhat.com> 1.10.2-10
- fix repeated downloads (Tomas Heinrich, #186195)

* Thu Dec 07 2006 Karsten Hopp <karsten@redhat.com> 1.10.2-9
- add distflag, rebuild

* Thu Dec 07 2006 Karsten Hopp <karsten@redhat.com> 1.10.2-8
- Resolves: #218211
  fix double free corruption

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-7
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Karsten Hopp <karsten@redhat.de> 1.10.2-6
- fix resumed downloads (#205723)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-5.1
- rebuild

* Thu Jun 29 2006 Karsten Hopp <karsten@redhat.de> 1.10.2-5
- updated german translations from Robert Scheck

* Tue Jun 27 2006 Karsten Hopp <karsten@redhat.de> 1.10.2-4
- upstream patches

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 1.10.2-3
- rebuilt against new openssl

* Tue Oct 25 2005 Karsten Hopp <karsten@redhat.de> 1.10.2-2
- use %%{_sysconfdir} (#171555)

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- 1.10.2

* Thu Sep 08 2005 Karsten Hopp <karsten@redhat.de> 1.10.1-7
- fix builtin help of --load-cookies / --save-cookies (#165408)

* Wed Sep 07 2005 Karsten Hopp <karsten@redhat.de> 1.10.1-6
- convert changelog to UTF-8 (#159585)

* Mon Sep 05 2005 Karsten Hopp <karsten@redhat.de> 1.10.1-5
- update
- drop patches which are already in the upstream sources

* Wed Jul 13 2005 Karsten Hopp <karsten@redhat.de> 1.10-5
- update german translation

* Mon Jul 11 2005 Karsten Hopp <karsten@redhat.de> 1.10-4
- update german translation (Robert Scheck)

* Tue Jul 05 2005 Karsten Hopp <karsten@redhat.de> 1.10-3
- fix minor documentation bug
- fix --no-cookies crash

* Mon Jul 04 2005 Karsten Hopp <karsten@redhat.de> 1.10-2
- update to wget-1.10
  - drop passive-ftp patch, already in 1.10
  - drop CVS patch
  - drop LFS patch, similar fix in 1.10
  - drop protdir patch, similar fix in 1.10
  - drop actime patch, already in 1.10

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-22
- build with gcc-4

* Wed Feb 02 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-21 
- remove old copy of the manpage (#146875, #135597)
- fix garbage in manpage (#117519)

* Tue Feb 01 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-20 
- texi2pod doesn't handle texinfo xref's. rewrite some lines so that
  the man page doesn't have incomplete sentences anymore (#140470)

* Mon Jan 31 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-19 
- Don't set actime to access time of the remote file or tmpwatch might 
  remove the file again (#146440).  Set it to the current time instead.
  timestamping checks only modtime, so this should be ok.

* Thu Jan 20 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-18
- add support for --protocol-directories option as documented
  in the man page (Ville Skyttä, #145571)

* Wed Sep 29 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-17 
- additional LFS patch from Leonid Petrov to fix file lengths in 
  http downloads

* Thu Sep 16 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-16 
- more fixes

* Tue Sep 14 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-15 
- added strtol fix from Leonid Petrov, reenable LFS

* Tue Sep 14 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-14
- buildrequires gettext (#132519)

* Wed Sep 01 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-13
- disable LFS patch for now, it breaks normal downloads (123524#c15)

* Tue Aug 31 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-12 
- move largefile stuff inside the configure script, it didn't
  get appended to CFLAGS

* Tue Aug 31 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-11
- rebuild

* Tue Aug 31 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-10 
- fix patch

* Sun Aug 29 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-9
- more cleanups of the manpage (#117519)

* Fri Aug 27 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-8
- rebuild

* Fri Aug 27 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-7 
- clean up manpage (#117519)
- buildrequire texinfo (#123780)
- LFS patch, based on wget-LFS-20040630.patch from Leonid Petrov
  (#123524, #124628, #115348)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 11 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-3 
- fix documentation (#117517)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Nov 28 2003 Karsten Hopp <karsten@redhat.de> 1.9.1-3
- update to -stable CVS
- document the passive ftp default

* Fri Nov 28 2003 Karsten Hopp <karsten@redhat.de> 1.9.1-2
- add patch from -stable CVS

* Fri Nov 28 2003 Karsten Hopp <karsten@redhat.de> 1.9.1-1
- update to 1.9.1
- remove obsolete patches

* Mon Aug 04 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-15.3
- fix variable usage

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-15.2
- rebuild

* Wed Jun 25 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-15.1
- rebuilt

* Wed Jun 25 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-15
- default to passive-ftp (#97996)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-13
- rebuild

* Wed Jun 04 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-12
- merge debian patch for long URLs
- cleanup filename patch

* Sun May 11 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-11
- rebuild

* Sun May 11 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-10
- upstream fix off-by-one error

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-8
- rebuild

* Fri Dec 13 2002 Nalin Dahyabhai <nalin@redhat.com>
- use openssl pkg-config data, if present
- don't bomb out when building with newer openssl

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 1.8.2-7
- rebuild on all arches

* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Fri Oct 4 2002 Karsten Hopp <karsten@redhat.de> 1.8.2-5
- fix directory traversal bug

* Wed Jul 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.8.2-3
- Don't segfault when downloading URLs A-B-A (A-A-B worked) #49859

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.8.2 (bug-fix release)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- remove s390 patch, not needed anymore

* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.8.1-4
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add hack to not link against libmd5, even if available

* Fri Dec 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.8.1

* Thu Dec 13 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.8
- also include md5global to get it compile

* Sun Nov 18 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.7.1

* Mon Sep  5 2001 Phil Knirsch <phil@redhat.de> 1.7-3
- Added va_args patch required for S390.

* Mon Sep  3 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.7-2
- Configure with ssl support (duh - #53116)
- s/Copyright/License/

* Wed Jun  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.7
- Require perl for building (to get man pages)
- Don't include the Japanese po file, it's now included
- Use %%{_tmppath}
- no patches necessary
- Make /etc/wgetrc noreplace
- More docs

* Tue Jan 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Norwegian isn't a iso-8859-2 locale, neither is Danish.
  This fixes #15025.
- langify

* Sat Jan  6 2001 Bill Nottingham <notting@redhat.com>
- escape %%xx characters before fnmatch (#23475, patch from alane@geeksrus.net)

* Fri Jan  5 2001 Bill Nottingham <notting@redhat.com>
- update to 1.6, fix patches accordingly (#23412)
- fix symlink patch (#23411)

* Mon Dec 18 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese and Korean Resources

* Tue Aug  1 2000 Bill Nottingham <notting@redhat.com>
- setlocale for LC_CTYPE too, or else all the translations think their
  characters are unprintable.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 11 2000 Bill Nottingham <notting@redhat.com>
- build in new environment

* Mon Jun  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHS compliance

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Thu Aug 26 1999 Jeff Johnson <jbj@redhat.com>
- don't permit chmod 777 on symlinks (#4725).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree
- add Provides

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries
- version 1.5.3

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.5.2

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- modified group to Applications/Networking

* Wed Apr 22 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.5.0
- they removed the man page from the distribution (Duh!) and I added it back
  from 1.4.5. Hey, removing the man page is DUMB!

* Fri Nov 14 1997 Cristian Gafton <gafton@redhat.com>
- first build against glibc
