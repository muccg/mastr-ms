%define __python /usr/bin/python%{pybasever}
# sitelib for noarch packages
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define pyver 27
%define pybasever 2.7

%define app mastrms
%define name %{app}
%define version 1.7.0
%define unmangled_version 1.7.0
%define release 1
%define webapps /usr/local/webapps
%define installdir %{webapps}/%{app}
%define buildinstalldir %{buildroot}%{installdir}
%define logdir %{buildroot}/var/log/%{app}
%define scratchdir %{buildroot}/var/lib/%{app}/scratch
%define mediadir %{buildroot}/var/lib/%{app}/media
%define staticdir %{buildinstalldir}/static

Summary: mastrms
#Name: python%{pyver}-django-%{app}
Name: %{app}
Version: %{version}
Release: %{release}
Source0: %{app}-%{unmangled_version}.tar.gz
License: GNU GPL v2
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{app}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: x86_64
Vendor: Centre for Comparative Genomics <web@ccg.murdoch.edu.au>
BuildRequires: python%{pyver}-virtualenv python-devel openssl-devel
Requires: python%{pyver}-psycopg2 python%{pyver}-mod_wsgi httpd rsync

%description
MastrMS web application

%prep

if [ -d ${RPM_BUILD_ROOT}%{installdir} ]; then
    echo "Cleaning out stale build directory" 1>&2
    rm -rf ${RPM_BUILD_ROOT}%{installdir}
fi

%build
# Nothing, all handled by install

%install
NAME=%{app}

# Build from source dir
cd $CCGSOURCEDIR

# These directories are for persistent data files created by the app
mkdir -p %{logdir}
mkdir -p %{scratchdir}
mkdir -p %{mediadir}

# Create a python prefix with app requirements
mkdir -p %{buildinstalldir}
virtualenv-%{pybasever} %{buildinstalldir}
. %{buildinstalldir}/bin/activate

# Install package into the prefix
pip install ./%{app}

# Fix up paths in virtualenv, enable use of global site-packages
virtualenv-%{pybasever} --relocatable %{buildinstalldir}
find %{buildinstalldir} -name \*py[co] -exec rm {} \;
find %{buildinstalldir} -name no-global-site-packages.txt -exec rm {} \;
sed -i "s|`readlink -f ${RPM_BUILD_ROOT}`||g" %{buildinstalldir}/bin/*

# don't need a copy of python interpreter in the virtualenv
rm %{buildinstalldir}/bin/python*

# undo prelinking
#find $RPM_BUILD_ROOT/opt/pyenv/%{ENVNAME}/bin/ -type f -perm /u+x,g+x -exec /usr/sbin/prelink -u {} \;
# remove rpath from build
#chrpath -d $RPM_BUILD_ROOT/opt/pyenv/%{ENVNAME}/bin/uwsgi
# re-point the lib64 symlink - not needed on newer virtualenv
#rm $RPM_BUILD_ROOT/opt/pyenv/%{ENVNAME}/lib64
#ln -sf /opt/pyenv/%{ENVNAME}/lib $RPM_BUILD_ROOT/opt/pyenv/%{ENVNAME}/lib64

# Create symlinks under install directory to real persistent data directories
APP_SETTINGS_FILE=`find %{buildinstalldir} -path "*/$NAME/settings.py" | sed s:^%{buildinstalldir}::`
APP_PACKAGE_DIR=`dirname ${APP_SETTINGS_FILE}`
ln -sfT /var/log/%{app} %{buildinstalldir}${APP_PACKAGE_DIR}/log
ln -sfT /var/lib/%{app}/scratch %{buildinstalldir}${APP_PACKAGE_DIR}/scratch
ln -sfT /var/lib/%{app}/media %{buildinstalldir}${APP_PACKAGE_DIR}/media
ln -sfT .${APP_PACKAGE_DIR}/static %{staticdir}

# Install WSGI configuration into httpd/conf.d
install -D centos/%{app}.ccg %{buildroot}/etc/httpd/conf.d/%{app}.ccg
install -D centos/django.wsgi %{buildinstalldir}/django.wsgi
mkdir -p %{buildroot}/%{_bindir}
ln -sfT %{installdir}/bin/%{app}-manage.py %{buildroot}/%{_bindir}/%{app}

%post
# Clear out staticfiles data and regenerate
rm -rf %{installdir}/static/*
%{app} collectstatic --noinput > /dev/null
# Remove root-owned logged files just created by collectstatic
rm -rf /var/log/%{app}/*
# Touch the wsgi file to get the app reloaded by mod_wsgi
touch %{installdir}/django.wsgi

%preun
if [ "$1" = "0" ]; then
  # Nuke staticfiles if not upgrading
  rm -rf %{installdir}/static/*
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,apache,apache,-)
/etc/httpd/conf.d/*
%{_bindir}/%{app}
%attr(-,apache,,apache) %{webapps}/%{app}
%attr(-,apache,,apache) /var/log/%{app}
%attr(-,apache,,apache) /var/lib/%{app}

%config /etc/httpd/conf.d/%{app}.ccg
