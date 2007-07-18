%define gcj_support 1
%define name        mx4j
%define version     3.0.1
%define section     free

Name:           %{name}
Version:        %{version}
Release:        %mkrel 4.4
Epoch:		0
Summary:        Open source implementation of JMX Java API
License:        Apache License
Group:          Development/Java
Source0:        %{name}-%{version}-src.tar.bz2
Source1:        %{name}-build.policy
Source2:        CatalogManager.properties
Patch0:         mx4j-javaxssl.patch
Patch2:         mx4j-build.patch
Patch3:         mx4j-docbook.patch
Patch5:         mx4j-caucho-build.patch
Patch6:         mx4j-no-iiop.patch
Url:            http://mx4j.sourceforge.net/
BuildRequires:  jpackage-utils > 0:1.5
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-trax, ant-junit, ant-nodeps
BuildRequires:	jaf
BuildRequires:	java-devel
BuildRequires:	javamail >= 0:1.2-5jpp
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
Requires:       /usr/sbin/update-alternatives
Requires:	jaf
Requires:	javamail >= 0:1.2-5jpp
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
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description
OpenJMX is an open source implementation of the
Java(TM) Management Extensions (JMX).

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

%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1

cp %{SOURCE1} build
cp %{SOURCE2} build

pushd lib
   ln -sf $(build-classpath junit) .
   ln -sf $(build-classpath xml-commons-jaxp-1.3-apis) xml-apis.jar
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
   ln -sf $(build-classpath servletapi5) servlet.jar
   #ln -sf $(build-classpath jsse) .
   ln -sf $(build-classpath jaas) .
popd

%build
export ANT_OPTS="-Djava.security.manager -Djava.security.policy=$(pwd)/build/mx4j-build.policy"
export CLASSPATH=$(build-classpath activation javamail/mailapi javamail/smtp \
   jakarta-commons-logging xml-commons-jaxp-1.3-apis bcel jsse jaas jce \
   log4j jaxp_transform_impl axis/axis axis/jaxrpc axis/saaj \
   xml-commons-resolver12 xdoclet/xdoclet xdoclet/xdoclet-jmx-module \
   xdoclet/xdoclet-mx4j-module)

export CLASSPATH=${CLASSPATH}:`pwd`/classes/core:`pwd`/build

export OPT_JAR_LIST="ant/ant-nodeps ant/ant-trax jaxp_transform_impl"

cd build
# FIXME: this seems to connect to the net :(
%ant compile.jmx compile.rjmx compile.tools javadocs #docs

%install
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
cp -r dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%{__perl} -pi -e 's/\r$//g' dist/docs/styles.css

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
rm -f %{_javadir}/%{name}.jar

%post
/usr/sbin/update-alternatives --install %{_javadir}/jmxri.jar jmxri %{_javadir}/%{name}/%{name}-jmx.jar 0
%if %{gcj_support}
%{_bindir}/rebuild-gcj-db
%endif

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/update-alternatives --remove jmxri %{_javadir}/%{name}/%{name}-jmx.jar
fi
%if %{gcj_support}
%{_bindir}/rebuild-gcj-db
%endif

%files
%defattr(-,root,root)
%{_javadir}/%{name}
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}-%{version}

%files manual
%defattr(0644,root,root,0755)
%doc dist/docs/*


