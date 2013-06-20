Mastr-MS Server
===============

Yum repository setup
--------------------

Mastr-MS is distributed as RPM, tested on Centos 6.x (x86_64). To
satisfy dependencies, `Epel`_ and `REMI`_ repos need to be enabled::

    sudo rpm -Uvh http://repo.ccgapps.com.au/repo/ccg/centos/6/os/noarch/CentOS/RPMS/ccg-release-6-1.noarch.rpm
    sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    sudo rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm

.. _Epel: http://fedoraproject.org/wiki/EPEL
.. _REMI: http://rpms.famillecollet.com/


Installation/Upgrade
--------------------

Install the Mastr-MS RPM, replacing X-X-X with the desired version::

    sudo yum install mastrms-X.X.X

Run Django syncdb and South migrate::

    sudo mastrms syncdb
    sudo mastrms migrate


Server Configuration
--------------------

Apache config
~~~~~~~~~~~~~

/etc/httpd/conf.d/mastrms.ccg

User creation
~~~~~~~~~~~~~

maupload

Data Repository and Permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Settings file
~~~~~~~~~~~~~

/etc/ccg/mastrms/appsettings.py  ??? fixme

Link to example config on bitbucket.



Testing
-------

https://your-web-host/mastrms/


Administration
--------------

https://your-web-host/mastrms/repoadmin/


.. _nodeclient-setup:

Data Sync Node Client Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. _adding-keys:

SSH Key Management
------------------

1. e-mail

2. uploaded key location 

3. authorized_keys

   /home/maupload/.ssh/authorized_keys

