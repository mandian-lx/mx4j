# Copyright (c) 2000-2007, JPackage Project
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
%define _without_tests 0
%define with_tests %{!?_without_tests:1}%{?_without_tests:0}
%define without_tests %{?_without_tests:1}%{!?_without_tests:0}

%define gcj_support 1
%define section     free


Name:           mx4j
Version:        3.0.1
Release:        %mkrel 2.0.1
Epoch:		0
Summary:        Open source implementation of JMX Java API
License:        Apache License
Group:          Development/Java
Source0:        %{name}-%{version}-src.tar.gz
Source1:        %{name}-build.policy
Source2:        CatalogManager.properties
Patch0:         mx4j-javaxssl.patch
Patch1:         mx4j-%{version}.patch
Patch2:         mx4j-build.patch
Patch3:         mx4j-docbook.patch
Patch4:         mx4j-no-poa.patch
Patch5:         mx4j-caucho-build.patch
Patch6:         mx4j-no-iiop.patch
Patch7:         mx4j-split-tools.patch
Url:            http://mx4j.sourceforge.net/
BuildRequires:  java-rpmbuild > 0:1.5
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-trax, ant-junit, ant-nodeps
BuildRequires:	geronimo-jaf-1.0.2-api
BuildRequires:	java-devel
BuildRequires:	geronimo-javamail-1.3.1-api
BuildRequires:	log4j >= 0:1.2.7
BuildRequires:	jakarta-commons-logging >= 0:1.0.1
BuildRequires:  xml-commons-jaxp-1.3-apis
BuildRequires:  bcel >= 0:5.0
BuildRequires:	jsse
BuildRequires:	jce
BuildRequires:  coreutils
BuildRequires:  xjavadoc
BuildRequires:  xdoclet
BuildRequires:  axis >= 0:1.1
BuildRequires:  wsdl4j
BuildRequires:  jakarta-commons-discovery
BuildRequires:  docbook-dtd412-xml >= 0:1.0
BuildRequires:  docbook-style-xsl >= 0:1.61
BuildRequires:  xml-commons-resolver12
BuildRequires:  xml-commons
BuildRequires:  jaxp_transform_impl
BuildRequires:  xalan-j2
Requires:       update-alternatives
Requires:	geronimo-jaf-1.0.2-api
Requires:	geronimo-javamail-1.3.1-api
Requires:	log4j >= 0:1.2.7
Requires:	jakarta-commons-logging >= 0:1.0.1
Requires:  	xml-commons-jaxp-1.3-apis
Requires:  	bcel >= 0:5.0
Requires:	jsse
Requires:	jce
Requires:  	axis >= 0:1.1
Requires:  	xml-commons-resolver12
Requires:  	xml-commons
Buildroot:      %{_tmppath}/%{name}-%{version}-buildroot
Obsoletes:      openjmx
Provides:	jmxri
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%endif

%description
OpenJMX is an open source implementation of the
Java(TM) Management Extensions (JMX).

%package tools-extra
Group:          Development/Java
Summary:        Additional protocols and scripting for %{name}
BuildRequires:  jython >= 2.1
BuildRequires:  axis >= 0:1.1
#BuildRequires:  burlap >= 3.0.8
#BuildRequires:  caucho-services
#BuildRequires:  hessian >= 3.0.8
Requires:       jython >= 2.1
Requires:       axis >= 0:1.1
#Requires:       burlap >= 3.0.8
#Requires:       caucho-services
#Requires:       hessian >= 3.0.8

%description    tools-extra
%{summary}.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Obsoletes:      openjmx-javadoc

%description javadoc
Javadoc for %{name}.

%package manual
Group:          Development/Java
Summary:        Documentation for %{name}

%description    manual
Documentation for %{name}.

%prep
%setup -q

# FIXME To enable iiop when rmic becomes available for GCJ
# turn off patch6 and turn on patch4
# Patch4 is a backport of upstream changes (MX4J) and may go
# away on future releases
%patch0 -p1 -b .sav0
%patch1 -p0 -b .sav1
%patch2 -b .sav2
%patch3 -p1 -b .sav3
%if ! %{gcj_support}
%patch4 -p0 -b .sav4
%else
%patch5 -p1 -b .sav5
%patch6 -p1 -b .sav6
%endif
%patch7 -p0

cp %{SOURCE1} build
cp %{_sourcedir}/CatalogManager.properties %{_builddir}/%{name}-%{version}/build/

pushd lib
%if %{with_tests}
   ln -sf $(build-classpath junit) .
   ln -sf $(build-classpath xmlunit) .
%endif
   ln -sf $(build-classpath xml-commons-apis) xml-apis.jar
   ln -sf $(build-classpath xerces-j2) xercesImpl.jar
   ln -sf $(build-classpath xalan-j2) xalan.jar
   ln -sf $(build-classpath commons-logging) .
   ln -sf $(build-classpath log4j) .
   #ln -sf $(build-classpath burlap) .
   #ln -sf $(build-classpath caucho-services) .
   #ln -sf $(build-classpath hessian) .
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
   ln -sf $(build-classpath geronimo-jaf-1.0.2-api) .

   ln -sf $(build-classpath commons-discovery) .
   ln -sf $(build-classpath jetty5/jetty5) org.mortbay.jetty.jar
   ln -sf $(build-classpath bcel) .
   ln -sf $(build-classpath servletapi5) servlet.jar
   ln -sf $(build-classpath jsse) .
   ln -sf $(build-classpath jsse/jcert) jcert.jar
   ln -sf $(build-classpath jsse/jnet) jnet.jar
   ln -sf $(build-classpath jaas) .
   ln -sf $(build-classpath xml-commons-resolver) .
popd


%build
export OPT_JAR_LIST="ant/ant-junit junit xmlunit ant/ant-trax jaxp_transform_impl ant/ant-apache-resolver xml-commons-resolver xalan-j2-serializer"

cd build
%if %{with_tests}
%{ant} -Dbuild.sysclasspath=first compile.jmx compile.rjmx compile.tools tests-report javadocs docs
%else
%{ant} -Dbuild.sysclasspath=first compile.jmx compile.rjmx compile.tools javadocs docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 644 dist/lib/%{name}-impl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-impl-%{version}.jar
install -m 644 dist/lib/%{name}-jmx.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-jmx-%{version}.jar
install -m 644 dist/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-%{version}.jar
install -m 644 dist/lib/%{name}-tools.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tools-%{version}.jar
install -m 644 dist/lib/%{name}-tools-extra.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tools-extra-%{version}.jar
install -m 644 dist/lib/%{name}-rjmx.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-rjmx-%{version}.jar
install -m 644 dist/lib/%{name}-rimpl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-rimpl-%{version}.jar
install -m 644 dist/lib/%{name}-remote.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-remote-%{version}.jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}/boa
install -m 644 dist/lib/boa/%{name}-rjmx-boa.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/boa/%{name}-rjmx-boa-%{version}.jar
install -m 644 dist/lib/boa/%{name}-rimpl-boa.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/boa/%{name}-rimpl-boa-%{version}.jar
install -m 644 dist/lib/boa/%{name}-remote-boa.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/boa/%{name}-remote-boa-%{version}.jar

pushd $RPM_BUILD_ROOT%{_javadir}/%{name}
   for jar in *-%{version}.jar ; do
      ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|.jar|g")
   done
popd

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -r dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
export CLASSPATH=$(build-classpath gnu-crypto)
%{_bindir}/aot-compile-rpm
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%pre
rm -f %{_javadir}/%{name}.jar

%post
/usr/sbin/update-alternatives --install %{_javadir}/jmxri.jar jmxri %{_javadir}/%{name}/%{name}-jmx.jar 0
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/update-alternatives --remove jmxri %{_javadir}/%{name}/%{name}-jmx.jar
fi
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root)
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/%{name}-%{version}.jar
%{_javadir}/%{name}/%{name}.jar
%{_javadir}/%{name}/%{name}-impl-%{version}.jar
%{_javadir}/%{name}/%{name}-impl.jar
%{_javadir}/%{name}/%{name}-jmx-%{version}.jar
%{_javadir}/%{name}/%{name}-jmx.jar
%{_javadir}/%{name}/%{name}-remote-%{version}.jar
%{_javadir}/%{name}/%{name}-remote.jar
%{_javadir}/%{name}/%{name}-rimpl-%{version}.jar
%{_javadir}/%{name}/%{name}-rimpl.jar
%{_javadir}/%{name}/%{name}-rjmx-%{version}.jar
%{_javadir}/%{name}/%{name}-rjmx.jar
%{_javadir}/%{name}/%{name}-tools-%{version}.jar
%{_javadir}/%{name}/%{name}-tools.jar
%{_javadir}/%{name}/boa/*.jar

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/mx4j-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/mx4j-tools-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/mx4j-remote-boa-%{version}.jar.*
%endif

%files tools-extra
%defattr(-,root,root)
%{_javadir}/%{name}/%{name}-tools-extra-%{version}.jar
%{_javadir}/%{name}/%{name}-tools-extra.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/mx4j-tools-extra-3.0.1.jar.*
%endif

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}-%{version}

%files manual
%defattr(0644,root,root,0755)
%doc dist/docs/*



