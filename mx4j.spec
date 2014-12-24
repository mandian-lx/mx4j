%{?_javapackages_macros:%_javapackages_macros}
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

%define jmx_version 1.2.1

%define section free

%define bootstrap 0

Summary:	Open source implementation of JMX Java API
Name:		mx4j
Version:	3.0.2
Release:	12
License:	Apache License
Group:		Development/Java
Url:		http://mx4j.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/mx4j/MX4J%20Source/3.0.2/mx4j-3.0.2-src.tar.gz
Source1:	%{name}-build.policy
Source2:	CatalogManager.properties
Source3:        http://repo1.maven.org/maven2/mx4j/mx4j/%{version}/mx4j-%{version}.pom
Source4:        http://repo1.maven.org/maven2/mx4j/mx4j-jmx/3.0.1/mx4j-jmx-3.0.1.pom
Source5:        http://repo1.maven.org/maven2/mx4j/mx4j-jmx-remote/3.0.1/mx4j-jmx-remote-3.0.1.pom
Source6:        http://repo1.maven.org/maven2/mx4j/mx4j-remote/%{version}/mx4j-remote-%{version}.pom
Source7:        http://repo1.maven.org/maven2/mx4j/mx4j-tools/3.0.1/mx4j-tools-3.0.1.pom
Source8:        http://repo1.maven.org/maven2/mx4j/mx4j-impl/2.1.1/mx4j-impl-2.1.1.pom
Source9:        http://repo1.maven.org/maven2/mx4j/mx4j-rimpl/2.1.1/mx4j-rimpl-2.1.1.pom
Source10:       http://repo1.maven.org/maven2/mx4j/mx4j-rjmx/2.1.1/mx4j-rjmx-2.1.1.pom

Patch0:		mx4j-javaxssl.patch
Patch2:		mx4j-build.patch
Patch3:		mx4j-docbook.patch
Patch5:		mx4j-caucho-build.patch
Patch7:		mx4j-split-tools.patch
BuildRequires:	jpackage-utils > 0:1.6
BuildRequires:	ant >= 0:1.6
%if ! %{bootstrap}
BuildRequires:	ant-apache-resolver
BuildRequires:	javamail >= 0:1.2
BuildRequires:	wsdl4j
BuildRequires:	jakarta-commons-discovery
%endif
BuildRequires:	bcel >= 0:5.0
BuildRequires:	log4j >= 0:1.2.7
BuildRequires:	jakarta-commons-logging >= 0:1.0.1
# BuildRequires:	jetty5
BuildRequires:	jsse >= 0:1.0.2
BuildRequires:	jce >= 0:1.2.2
BuildRequires:	coreutils
BuildRequires:  dos2unix
BuildRequires:	docbook-style-xsl >= 0:1.61
BuildRequires:	xml-commons-resolver
BuildRequires:	xml-commons-jaxp-1.3-apis
BuildRequires:	xerces-j2
BuildRequires:	libxml2-utils
%if %{with_tests}
BuildRequires:	ant-junit
BuildRequires:	junit >= 0:3.7.1
BuildRequires:	xmlunit
%endif
Buildarch:	noarch
%if ! %{bootstrap}
Requires:	javamail >= 0:1.2
%endif
Requires:	log4j >= 0:1.2.7
Requires:	jakarta-commons-logging >= 0:1.0.1
Requires:	bcel >= 0:5.0
Requires:	jsse >= 0:1.0.2
Requires:	jce >= 0:1.2.2
Requires:	xml-commons-resolver
Requires:	xml-commons-jaxp-1.3-apis
Requires(post,postun):	jpackage-utils
Requires:	jpackage-utils
Requires(pre):	coreutils
Requires(post,postun):	%{_sbindir}/update-alternatives
Provides:	jmxri = %{version}-%{release}

%description
OpenJMX is an open source implementation of the
Java(TM) Management Extensions (JMX).

%if ! %{bootstrap}
%package tools-extra
Group:		Development/Java
Summary:	Additional protocols and scripting for %{name}
BuildRequires:	jython >= 0:2.1
BuildRequires:	axis >= 0:1.1
# BuildRequires:	burlap >= 0:3.0.8
# BuildRequires:	caucho-services
# BuildRequires:	hessian >= 0:3.0.8
Requires:	jython >= 0:2.1
Requires:	axis >= 0:1.1
# Requires:	burlap >= 0:3.0.8
# Requires:	caucho-services
# Requires:	hessian >= 0:3.0.8

%description tools-extra
%{summary}.
%endif

%if ! %{bootstrap}
%package javadoc
Group:		Development/Java
Summary:	Javadoc for %{name}
# Obsoletes:	openjmx-javadoc

%description javadoc
%{summary}.
%endif

%if ! %{bootstrap}
%package manual
Group:		Development/Java
Summary:	Documentation for %{name}

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
   ln -sf $(build-classpath javamail/mailapi) .
   ln -sf $(build-classpath javamail/smtp) .
   ln -sf $(build-classpath commons-discovery) .
   ln -sf $(build-classpath jetty5/jetty5) org.mortbay.jetty.jar
%endif
   ln -sf $(build-classpath bcel) .
   ln -sf $(build-classpath servletapi5) servlet.jar
   ln -sf $(build-classpath jsse) .
   ln -sf $(build-classpath jsse/jcert) jcert.jar
   ln -sf $(build-classpath jsse/jnet) jnet.jar
   ln -sf $(build-classpath jaas) .
   ln -sf $(build-classpath xml-commons-resolver) .
popd

%build
export OPT_JAR_LIST="ant/ant-junit junit xmlunit jaxp_transform_impl xalan-j2-serializer ant/ant-apache-resolver xml-commons-resolver12"

cd build
%if ! %{bootstrap}
%if %{with_tests}
%{ant} -Dbuild.sysclasspath=first compile.jmx compile.rjmx compile.tools tests-report javadocs docs
%else
%{ant} -Dbuild.sysclasspath=first compile.jmx compile.rjmx compile.tools javadocs docs
%endif
%else
%{ant} -Dbuild.sysclasspath=first compile.jmx compile.rjmx
%endif

%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 644 dist/lib/%{name}-impl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-impl.jar
install -m 644 dist/lib/%{name}-jmx.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-jmx.jar
install -m 644 dist/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}.jar
install -m 644 dist/lib/%{name}-tools.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tools.jar
install -m 644 dist/lib/%{name}-rjmx.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-rjmx.jar
install -m 644 dist/lib/%{name}-rimpl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-rimpl.jar
install -m 644 dist/lib/%{name}-remote.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-remote.jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}/boa
install -m 644 dist/lib/boa/%{name}-rjmx-boa.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/boa/%{name}-rjmx-boa.jar
install -m 644 dist/lib/boa/%{name}-rimpl-boa.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/boa/%{name}-rimpl-boa.jar
install -m 644 dist/lib/boa/%{name}-remote-boa.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/boa/%{name}-remote-boa.jar

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{SOURCE3} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}.pom
%add_maven_depmap JPP.%{name}-%{name}.pom %{name}/%{name}.jar
install -pm 644 %{SOURCE4} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-jmx.pom
%add_maven_depmap JPP.%{name}-%{name}-jmx.pom %{name}/%{name}-jmx.jar
install -pm 644 %{SOURCE6} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-remote.pom
%add_maven_depmap JPP.%{name}-%{name}-remote.pom %{name}/%{name}-remote.jar
install -pm 644 %{SOURCE7} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-tools.pom
%add_maven_depmap JPP.%{name}-%{name}-tools.pom %{name}/%{name}-tools.jar

install -pm 644 %{SOURCE8} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-impl.pom
%add_maven_depmap JPP.%{name}-%{name}-impl.pom %{name}/%{name}-impl.jar
install -pm 644 %{SOURCE9} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-rimpl.pom
%add_maven_depmap JPP.%{name}-%{name}-rimpl.pom %{name}/%{name}-rimpl.jar
install -pm 644 %{SOURCE10} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-%{name}-rjmx.pom
%add_maven_depmap JPP.%{name}-%{name}-rjmx.pom %{name}/%{name}-rjmx.jar

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
dos2unix dist/docs/styles.css README.txt LICENSE.txt
cp -r dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%pre
%{__rm} -f %{_javadir}/%{name}.jar

%post
%{_sbindir}/update-alternatives --install %{_javadir}/jmxri.jar jmxri %{_javadir}/%{name}/mx4j-jmx.jar 0

%postun

if [ "$1" = "0" ]; then
      %{_sbindir}/update-alternatives --remove jmxri %{_javadir}/%{name}/mx4j-jmx.jar
fi

%files -f .mfiles
%{_javadir}/%{name}/boa

%files javadoc
%{_javadocdir}/%{name}

%files manual
%doc dist/docs/*

