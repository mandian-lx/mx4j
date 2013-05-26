# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


# Don't enable tests! Missing burlap, hessian, caucho-services packages
%define with_tests 0

%define gcj_support 0

%define jmx_version 1.2.1

%define section free

%define bootstrap 1

Name:           mx4j
Version:        3.0.2
Release:        4
Epoch:          0
Summary:        Open source implementation of JMX Java API
License:        Apache License
Group:          Development/Java
URL:            http://mx4j.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/mx4j/MX4J%20Source/3.0.2/mx4j-3.0.2-src.tar.gz
Source1:        %{name}-build.policy
Source2:        CatalogManager.properties
Source3:        http://mirrors.ibiblio.org/pub/mirrors/maven2/mx4j/mx4j/3.0.2/mx4j-3.0.2.pom
Source4:        http://mirrors.ibiblio.org/pub/mirrors/maven2/mx4j/mx4j-remote/3.0.2/mx4j-remote-3.0.2.pom
Patch0:         mx4j-javaxssl.patch
Patch2:         mx4j-build.patch
Patch3:         mx4j-docbook.patch
Patch5:         mx4j-caucho-build.patch
Patch7:         mx4j-split-tools.patch
Requires(post): jpackage-utils
Requires(postun): jpackage-utils
Requires:       jpackage-utils
Requires(pre):  coreutils
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
BuildRequires:  jpackage-utils > 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  java-rpmbuild > 0:1.5
BuildRequires:  ant-trax
%if ! %{bootstrap}
BuildRequires:  ant-apache-resolver
BuildRequires:  jaf
BuildRequires:  javamail >= 0:1.2
BuildRequires:  xjavadoc
BuildRequires:  xdoclet
BuildRequires:  wsdl4j
BuildRequires:  jakarta-commons-discovery
%endif
BuildRequires:  bcel >= 0:5.0
BuildRequires:  log4j >= 0:1.2.7
BuildRequires:  jakarta-commons-logging >= 0:1.0.1
# BuildRequires:  jetty5
BuildRequires:  jsse >= 0:1.0.2
BuildRequires:  jce >= 0:1.2.2
BuildRequires:  coreutils
BuildRequires:  docbook-style-xsl >= 0:1.61
BuildRequires:  xml-commons-resolver12
BuildRequires:  xml-commons-jaxp-1.3-apis
BuildRequires:  xerces-j2
BuildRequires:  libxml2-utils

%if %{with_tests}
BuildRequires:  ant-junit
BuildRequires:  junit >= 0:3.7.1
BuildRequires:  xmlunit
%endif
%if ! %{gcj_support}
Buildarch:      noarch
%endif
%if ! %{bootstrap}
Requires:       jaf
Requires:       javamail >= 0:1.2
%endif
Requires:       log4j >= 0:1.2.7
Requires:       jakarta-commons-logging >= 0:1.0.1
Requires:       bcel >= 0:5.0
Requires:       jsse >= 0:1.0.2
Requires:       jce >= 0:1.2.2
Requires:       xml-commons-resolver12
Requires:       xml-commons-jaxp-1.3-apis
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}
# Obsoletes:      openjmx
Provides:       jmxri = %{version}-%{release}

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
%endif

%description
OpenJMX is an open source implementation of the
Java(TM) Management Extensions (JMX).

%if ! %{bootstrap}
%package tools-extra
Group:          Development/Java
Summary:        Additional protocols and scripting for %{name}
BuildRequires:  jython >= 0:2.1
BuildRequires:  axis >= 0:1.1
# BuildRequires:  burlap >= 0:3.0.8
# BuildRequires:  caucho-services
# BuildRequires:  hessian >= 0:3.0.8
Requires:       jython >= 0:2.1
Requires:       axis >= 0:1.1
# Requires:       burlap >= 0:3.0.8
# Requires:       caucho-services
# Requires:       hessian >= 0:3.0.8

%description tools-extra
%{summary}.
%endif

%if ! %{bootstrap}
%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
# Obsoletes:      openjmx-javadoc

%description javadoc
%{summary}.
%endif

%if ! %{bootstrap}
%package manual
Group:          Development/Java
Summary:        Documentation for %{name}

%description    manual
%{summary}.
%endif

%prep
%setup -q

%patch0 -p1 -b .sav0
%patch2 -p0 -b .sav2
%patch3 -p1 -b .sav3
%patch5 -p1 -b .sav5
%patch7 -p0 -b .sav7

cp -p %{SOURCE1} build
cp -p %{SOURCE2} %{_builddir}/%{name}-%{version}/build/
# use the one from docbook-dtds instead of getting it from the net
catalogfile=`%{_bindir}/xmlcatalog /usr/share/sgml/docbook/xmlcatalog "-//OASIS//DTD DocBook XML V4.1.2//EN"`
sed -i -e 's|http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd|'$catalogfile'|' src/docs/index.xml
catalogfile=`%{_bindir}/xmlcatalog /etc/xml/catalog "http://docbook.sourceforge.net/release/xsl/current/html/chunk.xsl" | sed -e 's|file://||'`
sed -i -e 's|http://docbook.sourceforge.net/release/xsl/current/html/chunk.xsl|'$catalogfile'|' src/docs/xsl/mx4j-chunk.xsl

pushd lib
%if %{with_tests}
   ln -sf $(build-classpath junit) .
   ln -sf $(build-classpath xmlunit) .
%endif
   ln -sf $(build-classpath xml-commons-jaxp-1.3-apis) xml-apis.jar
   ln -sf $(build-classpath xerces-j2) xercesImpl.jar
   ln -sf $(build-classpath xalan-j2) xalan.jar
   ln -sf $(build-classpath commons-logging) .
   ln -sf $(build-classpath log4j) .
%if ! %{bootstrap}
#   ln -sf $(build-classpath burlap) .
#   ln -sf $(build-classpath caucho-services) .
#   ln -sf $(build-classpath hessian) .
   ln -sf $(build-classpath axis/axis) .
   ln -sf $(build-classpath axis/jaxrpc) .
   ln -sf $(build-classpath axis/saaj) .
   ln -sf $(build-classpath wsdl4j) .
   ln -sf $(build-classpath jython) .
   ln -sf $(build-classpath xdoclet/xdoclet) .
   ln -sf $(build-classpath xdoclet/xdoclet-jmx-module) .
   ln -sf $(build-classpath xdoclet/xdoclet-mx4j-module) .
   ln -sf $(build-classpath javamail/mailapi) .
   ln -sf $(build-classpath javamail/smtp) .
   ln -sf $(build-classpath jaf) .
   ln -sf $(build-classpath commons-discovery) .
   ln -sf $(build-classpath jetty5/jetty5) org.mortbay.jetty.jar
%endif
   ln -sf $(build-classpath bcel) .
   ln -sf $(build-classpath servletapi5) servlet.jar
   ln -sf $(build-classpath jsse) .
   ln -sf $(build-classpath jsse/jcert) jcert.jar
   ln -sf $(build-classpath jsse/jnet) jnet.jar
   ln -sf $(build-classpath jaas) .
   ln -sf $(build-classpath xml-commons-resolver12) .
popd

%build
export OPT_JAR_LIST="ant/ant-junit junit xmlunit ant/ant-trax jaxp_transform_impl xalan-j2-serializer ant/ant-apache-resolver xml-commons-resolver12"

cd build
%if %{with_tests}
%{ant} -Dbuild.sysclasspath=first compile.jmx compile.rjmx compile.tools tests-report javadocs docs
%else
%{ant} -Dbuild.sysclasspath=first compile.jmx compile.rjmx compile.tools javadocs docs
%endif


%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_javadir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -m 644 dist/lib/%{name}-impl.jar %{buildroot}%{_javadir}/%{name}/mx4j-impl-%{version}.jar
install -m 644 dist/lib/%{name}-jmx.jar %{buildroot}%{_javadir}/%{name}/mx4j-jmx-%{version}.jar
install -m 644 dist/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}/mx4j-%{version}.jar
install -m 644 dist/lib/%{name}-tools.jar %{buildroot}%{_javadir}/%{name}/mx4j-tools-%{version}.jar
install -m 644 dist/lib/%{name}-tools-extra.jar %{buildroot}%{_javadir}/%{name}/mx4j-tools-extra-%{version}.jar
install -m 644 dist/lib/%{name}-rjmx.jar %{buildroot}%{_javadir}/%{name}/mx4j-rjmx-%{version}.jar
install -m 644 dist/lib/%{name}-rimpl.jar %{buildroot}%{_javadir}/%{name}/mx4j-rimpl-%{version}.jar
install -m 644 dist/lib/%{name}-remote.jar %{buildroot}%{_javadir}/%{name}/mx4j-remote-%{version}.jar
install -d -m 755 %{buildroot}%{_javadir}/%{name}/boa
install -m 644 dist/lib/boa/%{name}-rjmx-boa.jar %{buildroot}%{_javadir}/%{name}/boa/%{name}-rjmx-boa-%{version}.jar
install -m 644 dist/lib/boa/%{name}-rimpl-boa.jar %{buildroot}%{_javadir}/%{name}/boa/%{name}-rimpl-boa-%{version}.jar
install -m 644 dist/lib/boa/%{name}-remote-boa.jar %{buildroot}%{_javadir}/%{name}/boa/%{name}-remote-boa-%{version}.jar

pushd %{buildroot}%{_javadir}/%{name}
   for jar in *-%{version}.jar ; do
      ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|.jar|g")
   done
popd

pushd %{buildroot}%{_javadir}/%{name}/boa
   for jar in *-%{version}.jar ; do
      ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|.jar|g")
   done
popd

# poms

mkdir -p %{buildroot}%{_mavenpomdir}
cp -p %{SOURCE3} %{buildroot}%{_mavenpomdir}/JPP.%{name}-mx4j.pom
cp -p %{SOURCE4} %{buildroot}%{_mavenpomdir}/JPP.%{name}-mx4j-remote.pom
%add_to_maven_depmap mx4j mx4j %{version} JPP/%{name} mx4j
%add_to_maven_depmap mx4j mx4j-remote %{version} JPP/%{name} mx4j-remote


install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -r dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}


%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif


%pre
%{__rm} -f %{_javadir}/%{name}.jar

%post
%{_sbindir}/update-alternatives --install %{_javadir}/jmxri.jar jmxri %{_javadir}/%{name}/mx4j-jmx.jar 0

%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%update_maven_depmap

%postun
%update_maven_depmap

if [ "$1" = "0" ]; then
      %{_sbindir}/update-alternatives --remove jmxri %{_javadir}/%{name}/mx4j-jmx.jar
fi

%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/mx4j-%{version}.jar
%{_javadir}/%{name}/mx4j.jar
%{_javadir}/%{name}/mx4j-impl-%{version}.jar
%{_javadir}/%{name}/mx4j-impl.jar
%{_javadir}/%{name}/mx4j-jmx-%{version}.jar
%{_javadir}/%{name}/mx4j-jmx.jar
%{_javadir}/%{name}/mx4j-remote-%{version}.jar
%{_javadir}/%{name}/mx4j-remote.jar
%{_javadir}/%{name}/mx4j-rimpl-%{version}.jar
%{_javadir}/%{name}/mx4j-rimpl.jar
%{_javadir}/%{name}/mx4j-rjmx-%{version}.jar
%{_javadir}/%{name}/mx4j-rjmx.jar
%{_javadir}/%{name}/mx4j-tools-%{version}.jar
%{_javadir}/%{name}/mx4j-tools.jar
%dir %{_javadir}/%{name}/boa
%{_javadir}/%{name}/boa/mx4j-remote-boa-%{version}.jar
%{_javadir}/%{name}/boa/mx4j-remote-boa.jar
%{_javadir}/%{name}/boa/mx4j-rimpl-boa-%{version}.jar
%{_javadir}/%{name}/boa/mx4j-rimpl-boa.jar
%{_javadir}/%{name}/boa/mx4j-rjmx-boa-%{version}.jar
%{_javadir}/%{name}/boa/mx4j-rjmx-boa.jar
%{_mavenpomdir}/JPP.%{name}-mx4j.pom
%{_mavenpomdir}/JPP.%{name}-mx4j-remote.pom
%config %{_mavendepmapfragdir}/%{name}
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/mx4j-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/mx4j-tools-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/mx4j-remote-boa-%{version}.jar.*
%endif

%if ! %{bootstrap}
%files tools-extra
%defattr(0644,root,root,0755)
%{_javadir}/%{name}/mx4j-tools-extra-%{version}.jar
%{_javadir}/%{name}/mx4j-tools-extra.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/mx4j-tools-extra-%{version}.jar.*
%endif
%endif

%if ! %{bootstrap}
%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
%endif

%if ! %{bootstrap}
%files manual
%defattr(0644,root,root,0755)
%doc dist/docs/*
%endif

%changelog
* Wed Feb 22 2012 Andrew Lukoshko <andrew.lukoshko@rosalab.ru> 0:3.0.2-2
- adopted for 2011.0
- spec updated with maven macroses
- RPM5 don't need clean section anymore
- made rpmlint happier

* Thu Oct 07 2010 David Walluck <dwalluck@redhat.com> 0:3.0.2-1
- 3.0.2
- add a couple poms
- add boa symlinks

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:3.0.1-9
- License is ASL 1.1

* Wed Jul 23 2008 David Walluck <dwalluck@redhat.com> 0:3.0.1-8
- remove javadoc scriptlets
- GCJ fixes
- fix file ownership
- update License
- update BuildRoot
- remove Vendor and Distribution
- use macros
- add xalan-j2-serializer to OPT_JAR_LIST

* Tue Feb 13 2007 Ralph Apel <r.apel at r-apel.de> 0:3.0.1-7jpp
- Add bootstrap option: omit tools
- Split out tools-extra subpackage, split mx4j-tools.jar
- Reactivated jetty

* Fri Aug 25 2006 Deepak Bhole <dbhole@redhat.com> 0:3.0.1-6jpp
- Make tests conditional
- Fixed build file to correctly resolve dtds.

* Mon Jul 24 2006 Fernando Nasser <fnasser@redhat.com> 0:3.0.1-5jpp
From Thomas Fitzsimmons <fitzsim@redhat.com>:
- Require xerces-j2

* Tue Jul 18 2006 Fernando Nasser <fnasser@redhat.com> 0:3.0.1-4jpp
- Remove duplicate macros
- Use unversioned burlap and hessian
- Don't use jetty4 as it is not yet available on JPP 1.7
- Re-add Epoch to the versions required
- Split patch for removal of poa
- Add AOT bits

* Tue Mar 14 2006 Fernando Nasser <fnasser@redhat.com> 0:3.0.1-3jpp
- Remove dependencies on non-free JXM packages by building MX4J's own
- Add (re-add?) "java.naming.corba.orb" patch, needed by JOnAS

* Fri Mar 10 2006 Ralph Apel <r.apel@r-apel.de> 0:3.0.1-2jpp
- Activate burlap and hessian support
- Most unit tests now pass with java-1.4.2-sun-1.4.2.10-1jpp

* Fri Apr 22 2005 Fernando Nasser <fnasser@redhat.com> 0:3.0.1-1jpp
- Upgrade to 3.0.1

* Wed Apr 20 2005 Fernando Nasser <fnasser@redhat.com> 0:2.1.0-1jpp
- Upgrade to 2.1.0
- Do not build caucho part because of version incompatibilities
  From Andrew Overholt <overholt@redhat.com>
- add coreutils BuildRequires

* Tue Mar 08 2005 Ralph Apel <r.apel at r-apel.de> 0:2.0.1-3jpp
- Drop spurious Requires: junit

* Fri Sep 24 2004 Ralph Apel <r.apel at r-apel.de> 0:2.0.1-2jpp
- Require xml-commons (jpackage), not xml-common (linux)
- Activate jython- and jetty-related classes
- Activate unit tests, therefore BuildReq xmlunit
- Include compliance test, therefore BuildReq jmx, jmxremote
- Define essential runtime requires
- Use security manager and relaxed policy

* Fri Jun 25 2004 Aizaz Ahmed <aahmed@redhat.com> 1:2.0.1-1jpp
- Updated to use mx4j-2.0.1
- Rebuilt with Ant 1.6.2

* Mon Mar 24 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 1.1.1-4jpp
- jmxri alternative

* Mon Mar 24 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 1.1.1-3jpp
- use own dir
- For jpackage-utils 1.5

* Thu Feb 20 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.1.1-1jpp
- mx4j 1.1.1
- grabed from CVS TAG MX4J_1_1_1

* Wed Sep 18 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.1-3jpp
- added missing xsl/jython resources in mx4j-tools.jar
- correct the build.xml to have correct contents for mx4.jar and mx4j-tools.jar

* Tue Jul 02 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-2jpp
- bzipped additional sources
- section macro
- ant already requires jaxp_parser
- fixed source perms
- fixed compilation with jsse and javamail
- buildrequires jsse >= 1.0.2-6jpp
- buildrequires javamail >= 1.2-5jpp

* Mon Jun 10 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.1-1jpp
- mx4j 1.1
- set correct jpackage tags
- add provide jmxri

* Mon Mar 04 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.0b3-1jpp
- mx4j 1.0b3 (previous name was openjmx)

* Fri Jan 18 2002 Henri Gomez <hgomez@users.sourceforge.net> 1.0b1-1jpp
- first JPackage release
