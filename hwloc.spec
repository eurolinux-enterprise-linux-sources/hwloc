Summary:   Portable Hardware Locality - portable abstraction of hierarchical architectures
Name:      hwloc
Version:   1.5
Release:   3%{?dist}
License:   BSD
Group:     Applications/System
URL:       http://www.open-mpi.org/projects/hwloc/
Source0:   http://www.open-mpi.org/software/hwloc/v1.5/downloads/%{name}-%{version}.tar.bz2
Source1:   http://www.open-mpi.org/software/hwloc/v1.1/downloads/%{name}-1.1.tar.bz2

BuildRequires: libX11-devel libxml2-devel cairo-devel ncurses-devel pciutils-devel transfig doxygen w3m
%ifnarch s390 s390x
BuildRequires: libibverbs-devel
%endif
%ifnarch s390 s390x %{arm}
BuildRequires: numactl-devel
##Requires: numactl-libs
%endif

%description
The Portable Hardware Locality (hwloc) software package provides 
a portable abstraction (across OS, versions, architectures, ...) 
of the hierarchical topology of modern architectures, including 
NUMA memory nodes,  shared caches, processor sockets, processor cores
and processing units (logical processors or "threads"). It also gathers
various system attributes such as cache and memory information. It primarily
aims at helping applications with gathering information about modern
computing hardware so as to exploit it accordingly and efficiently.

hwloc may display the topology in multiple convenient formats. 
It also offers a powerful programming interface (C API) to gather information 
about the hardware, bind processes, and much more.

%package devel
Summary:   Headers and shared development libraries for hwloc
Group:     Development/Libraries
Requires:  %{name} = %{version}-%{release}

%description devel
Headers and shared object symbolic links for the hwloc.

%prep
%setup -q -c
%setup -q -T -D -a 1


%build

cd %{name}-%{version}
%configure
%{__make} %{?_smp_mflags} V=1
cd ../hwloc-1.1
%configure
%{__make} %{?_smp_mflags} V=1
cd ..

%install
# Install the compat lib first so that the libhwloc.so symlink gets overwritten
# by the new version in the next step.
cd hwloc-1.1/src
%{__make} install-libLTLIBRARIES DESTDIR=%{buildroot} INSTALL="%{__install} -p"
cd ../..

cd %{name}-%{version}
%{__make} install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

#Fix wrong permition on file hwloc-assembler-remote => I have reported this to upstream already
%{__chmod} 0755 %{buildroot}%{_bindir}/hwloc-assembler-remote

%{__mv} %{buildroot}%{_defaultdocdir}/%{name} %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%{__cp} -p AUTHORS COPYING NEWS README VERSION %{buildroot}%{_defaultdocdir}/%{name}-%{version}
%{__cp} -p doc/hwloc-hello.c %{buildroot}%{_defaultdocdir}/%{name}-%{version}

# We don't ship .la files.
%{__rm} -rf %{buildroot}%{_libdir}/libhwloc.la

%check
cd %{name}-%{version}
%{__make} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%{_bindir}/%{name}*
%{_bindir}/lstopo
%{_bindir}/lstopo-no-graphics
%{_mandir}/man7/%{name}*
%{_mandir}/man1/%{name}*
%{_mandir}/man1/lstopo*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{name}.dtd
%{_datadir}/%{name}/%{name}-valgrind.supp
%dir %{_defaultdocdir}/%{name}-%{version}
%{_defaultdocdir}/%{name}-%{version}/*[^c]
%{_libdir}/libhwloc*so.*

%files devel
%defattr(-, root, root, -)
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_includedir}/%{name}.h
%{_defaultdocdir}/%{name}-%{version}/*c
%{_libdir}/*.so


%changelog
* Thu Aug 21 2014 Michal Schmidt <mschmidt@redhat.com> - 1.5-3
- Make libhwloc.so point to the current library version, not the compat one.
  Resolves: rhbz1135040

* Fri Jul 18 2014 Jay Fenlason <fenlason@redhat.com> - 1.5-2
- Build the 1.1 version as well, so we have the old library for backward
  compatability.
  Resolves: rhbz1070347

* Wed Aug 15 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.5-1
- Update to version 1.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 1.4.2-1
- Update to version 1.4.2

* Wed Apr 18 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.4.1-2
- Fixed build dependency for s390x

* Mon Apr 16 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.4.1-1
- Update to version 1.4.1
- BZ812622 - libnuma was splitted out of numactl package

* Thu Apr 12 2012 Dan Horák <dan[at]danny.cz> - 1.4-2
- no InfiniBand on s390(x)

* Wed Feb 14 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.4-1
- Update to 1.4 release

* Mon Nov 14 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3-1
- Update build for ARM support

* Sat Oct 15 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.3-0
 - 1.3 release
 - added dependency on libibverbs-devel pciutils-devel
 - cannot provide support for cuda (cuda_runtime_api.h). 
 - Nvidia CUDA is free but not open-source therefore not in Fedora.

* Fri Oct 07 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2.2-1
 - moved *.so to the devel package
 - libhwloc*so* in the main package

* Wed Oct 05 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2.2-0
- 1.2.2 release
- Fix for BZ https://bugzilla.redhat.com/show_bug.cgi?id=724937 for 32-bit PPC

* Sat Sep 17 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2.1-0
- 1.2.1 release
- Moved libhwloc*.so* to the main package

* Mon Jun 27 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2-0
- 1.2 release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan  3 2011 Dan Horák <dan[at]danny.cz> - 1.1-0.1
- fix build on s390(x) where numactl is missing

* Sat Jan  1 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.1-0
- 1.1 rel# Patch to the 1.1 fix 2967 http://www.open-mpi.org/software/hwloc/nightly/v1.1/hwloc-1.1rc6r2967.tar.bz2
- Fix hwloc_bitmap_to_ulong right after allocating the bitmap.
- Fix the minimum width of NUMA nodes, caches and the legend in the graphical lstopo output.
- Cleanup error management in hwloc-gather-topology.sh.
- Add a manpage and usage for hwloc-gather-topology.sh on Linux.
- Rename hwloc-gather-topology.sh to hwloc-gather-topology to be consistent with the upcoming version 1.2ease

* Mon Jul 19 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.2-1
- 1.0.2 release
- added "check" section to the RPM SPEC file

* Mon Jul 19 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.2-0.1.rc1r2330
- 1.0.2 release candidate

* Mon Jul 12 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-19
- Fixed issues as described at https://bugzilla.redhat.com/show_bug.cgi?id=606498#c6

* Fri Jul 09 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-18
- Fixed issues as described at https://bugzilla.redhat.com/show_bug.cgi?id=606498

* Fri Jun 18 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-17
- Initial build
