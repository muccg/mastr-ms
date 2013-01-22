%define name wardabdr
%define version 1.0.0
%define unmangled_version 1.1.0
%define unmangled_version 1.1.0
%define release 1
%define webapps /usr/local/webapps
%define installdir %{webapps}/%{name}
%define buildinstalldir %{buildroot}/%{installdir}
%define settingsdir %{buildinstalldir}/settings
%define logsdir %{buildinstalldir}/logs
%define scratchdir %{buildinstalldir}/scratch
%define staticdir %{buildinstalldir}/static

# Turn off brp-python-bytecompile because it makes it difficult to generate the file list
# We still byte compile everything by passing in -O paramaters to python
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Summary: Masterms
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: UNKNOWN
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: x86_64
Vendor: Centre for Comparative Genomics <web@ccg.murdoch.edu.au>
BuildRequires: python-setuptools
Requires: httpd mod_wsgi mysql-libs

%description
Master MS

%prep
#%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
# Nothing, all handled by install

%install
NAME=%{name}

# Make sure the standard target directories exist
mkdir -p %{settingsdir}
mkdir -p %{logsdir}
mkdir -p %{scratchdir}
mkdir -p %{staticdir}

# Create a python prefix
mkdir -p %{buildinstalldir}/{lib,bin,include}

# Install package into the prefix
cd $CCGSOURCEDIR
export PYTHONPATH=%{buildinstalldir}/lib
easy_install -O1 --prefix %{buildinstalldir} --install-dir %{buildinstalldir}/lib .

# Create settings symlink so we can run collectstatic with the default settings
touch %{settingsdir}/__init__.py
ln -fs ..`find %{buildinstalldir} -path "*/$NAME/settings.py" | sed s:^%{buildinstalldir}::` %{settingsdir}/settings.py

# Install WSGI configuration into httpd/conf.d
install -D centos/%{name}_mod_wsgi_daemons.conf %{buildroot}/etc/httpd/conf.d/%{name}_mod_wsgi_daemons.conf
install -D centos/%{name}_mod_wsgi.conf %{buildroot}/etc/httpd/conf.d/%{name}_mod_wsgi.conf
install -D centos/django.wsgi %{buildinstalldir}/django.wsgi
install -m 0755 -D centos/%{name}-manage.py %{buildroot}/%{_bindir}/%{name}

# At least one python package has hardcoded shebangs to /usr/local/bin/python
find %{buildinstalldir} -name '*.py' -type f | xargs sed -i 's:^#!/usr/local/bin/python:#!/usr/bin/python:'
find %{buildinstalldir} -name '*.py' -type f | xargs sed -i 's:^#!/usr/local/python:#!/usr/bin/python:'

%post
wardabdr collectstatic --noinput > /dev/null

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/etc/httpd/conf.d/*
%{_bindir}/%{name}
%attr(-,apache,,apache) %{webapps}/%{name}

