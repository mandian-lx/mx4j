# Copyright (c) 2000-2005, JPackage Project
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

%define with_tests 0

Name:           mx4j
Version:        3.0.1
Release:        12
Summary:        Open source implementation of JMX Java API
License:        ASL 1.1
Group:          Development/Java
Source0:        %{name}-%{version}-src.tar.gz
Source1:        %{name}-build.policy
Source2:        CatalogManager.properties
Patch0:         mx4j-javaxssl.patch
Patch1:         mx4j-%{version}.patch
Patch2:         mx4j-build.patch
Patch3:         mx4j-docbook.patch
Patch5:         mx4j-caucho-build.patch
Patch6:         mx4j-no-iiop.patch
URL:            http://mx4j.sourceforge.net/
BuildRequires:  jpackage-utils > 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-nodeps
BuildRequires:  ant-apache-resolver
BuildRequires:  javamail >= 0:1.2-5jpp
BuildRequires:  log4j >= 0:1.2.7
BuildRequires:  apache-commons-logging >= 0:1.0.1
BuildRequires:  xml-commons-apis
BuildRequires:  bcel >= 0:5.0
BuildRequires:  jsse >= 0:1.0.2-6jpp
BuildRequires:  jce >= 0:1.2.2
BuildRequires:  coreutils
BuildRequires:  xjavadoc
BuildRequires:  xdoclet
BuildRequires:  axis >= 0:1.1
BuildRequires:  wsdl4j
BuildRequires:  apache-commons-discovery
BuildRequires:  docbook-dtd43-xml 
BuildRequires:  docbook-style-xsl >= 0:1.61
BuildRequires:  xml-commons-resolver
BuildRequires:  xml-commons
BuildRequires:  xerces-j2
BuildRequires:  dos2unix
%if %{with_tests}
BuildRequires:  ant-junit
BuildRequires:  burlap >= 3.0.8
BuildRequires:  caucho-services
BuildRequires:  hessian >= 3.0.8
BuildRequires:  junit >= 0:3.7.1
BuildRequires:  xmlunit
%endif
Buildarch:      noarch
Requires(pre):  /bin/rm
Requires(post):       %{_sbindir}/update-alternatives
Requires(postun):       %{_sbindir}/update-alternatives
Requires:       javamail >= 0:1.2-5jpp
Requires:       log4j >= 0:1.2.7
Requires:       apache-commons-logging >= 0:1.0.1
Requires:       xml-commons-apis
Requires:       bcel >= 0:5.0
Requires:       jsse >= 0:1.0.2-6jpp
Requires:       jce >= 0:1.2.2
Requires:       axis >= 0:1.1
Requires:       xml-commons-resolver
Requires:       xml-commons
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot

%description
OpenJMX is an open source implementation of the
Java(TM) Management Extensions (JMX).

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package manual
Group:          Development/Java
Summary:        Documentation for %{name}

%description    manual
Documentation for %{name}.

%prep
%setup -q

# FIXME To enable iiop when rmic becomes available
# turn off patch6 and turn on patch4
# Patch4 is a backport of upstream changes (MX4J) and may go
# away on future releases
%patch0 -p1
%patch1 -p0
%patch2 -p0 -b .sav
%patch3 -p1
%patch5 -p1
%patch6 -p1

cp %{SOURCE1} build
cp %{_sourcedir}/CatalogManager.properties %{_builddir}/%{name}-%{version}/build/

pushd lib
%if %{with_tests}
   ln -sf $(build-classpath junit) .
   ln -sf $(build-classpath xmlunit) .
   ln -sf $(build-classpath burlap) .
   ln -sf $(build-classpath caucho-services) .
   ln -sf $(build-classpath hessian) .
%endif
   ln -sf $(build-classpath xml-commons-apis) xml-apis.jar
   ln -sf $(build-classpath xerces-j2) xercesImpl.jar
   ln -sf $(build-classpath xalan-j2) xalan.jar
   ln -sf $(build-classpath commons-logging) .
   ln -sf $(build-classpath log4j) .
   ln -sf $(build-classpath bcel) .
   ln -sf $(build-classpath axis/axis) .
   ln -sf $(build-classpath axis/jaxrpc) .
   ln -sf $(build-classpath axis/saaj) .
   ln -sf $(build-classpath wsdl4j) .
   ln -sf $(build-classpath commons-discovery) .
   ln -sf $(build-classpath servlet25) servlet.jar
#   ln -sf $(build-classpath jython) .
   ln -sf $(build-classpath jsse) .
   ln -sf $(build-classpath jsse/jcert) jcert.jar
   ln -sf $(build-classpath jsse/jnet) jnet.jar
   ln -sf $(build-classpath jaas) .
   ln -sf $(build-classpath javamail/mail) .
   ln -sf $(build-classpath xml-commons-resolver) .
   ln -sf $(build-classpath xdoclet/xdoclet) .
   ln -sf $(build-classpath xdoclet/xdoclet-jmx-module) .
   ln -sf $(build-classpath xdoclet/xdoclet-mx4j-module) .
popd

%build

export OPT_JAR_LIST="ant/ant-junit junit xmlunit ant/ant-nodeps jaxp_transform_impl ant/ant-apache-resolver xml-commons-resolver xalan-j2-serializer"

cd build
%if %{with_tests}
ant -Dbuild.sysclasspath=first compile.jmx compile.rjmx compile.tools tests-report javadocs docs
%else
ant -Dbuild.sysclasspath=first compile.jmx compile.rjmx compile.tools javadocs docs
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m 644 dist/lib/%{name}-impl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-impl-%{version}.jar
install -m 644 dist/lib/%{name}-jmx.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-jmx-%{version}.jar
install -m 644 dist/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-%{version}.jar
install -m 644 dist/lib/%{name}-tools.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-tools-%{version}.jar
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
dos2unix dist/docs/styles.css README.txt LICENSE.txt
cp -r dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
rm -f %{_javadir}/%{name}.jar

%post
%{_sbindir}/update-alternatives --install %{_javadir}/jmxri.jar jmxri %{_javadir}/%{name}/%{name}-jmx.jar 0

%postun
if [ "$1" = "0" ]; then
  %{_sbindir}/update-alternatives --remove jmxri %{_javadir}/%{name}/%{name}-jmx.jar
fi

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}
%doc LICENSE.txt
%doc README.txt

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files manual
%defattr(-,root,root,-)
%doc dist/docs/*

