Mastr-MS Server
===============

The Mastr-MS server is a Django application which provides a web
interface for user management, sample management, and access to
experiment data.


Installation
------------

Yum repository setup
~~~~~~~~~~~~~~~~~~~~

Mastr-MS is distributed as RPM, tested on Centos 6.x (x86_64). To
satisfy dependencies, `Epel`_ and `REMI`_ repos need to be enabled::

    sudo rpm -Uvh http://repo.ccgapps.com.au/repo/ccg/centos/6/os/noarch/CentOS/RPMS/ccg-release-6-2.noarch.rpm
    sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    sudo rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm

.. _Epel: http://fedoraproject.org/wiki/EPEL
.. _REMI: http://rpms.famillecollet.com/

Dependencies
~~~~~~~~~~~~

The database and python database driver aren't dependencies of the
Mastr-MS RPM, so have to be installed manually::

    sudo yum install postgresql-server python-psycopg2

.. note:: These instructions are written for PostgreSQL. With minor
   alterations (issue `MAS-32`_) Mastr-MS could work with
   MySQL/MariaDB, but at present only PostgreSQL is supported.

.. _MAS-32:
   https://ccgmurdoch.atlassian.net/browse/MAS-32


Install
~~~~~~~

Install the Mastr-MS RPM, replacing ``X.X.X`` with the desired version::

    sudo yum install mastrms-X.X.X

Server Configuration
--------------------

Database Setup
~~~~~~~~~~~~~~

If starting from a fresh CentOS install, you will need to configure
PostgreSQL::

    service postgresql initdb
    service postgresql start
    chkconfig postgresql on

To enable password authentication in PostgreSQL, you need to edit
``/var/lib/pgsql/data/pg_hba.conf``. As described in `the
documentation`_, add the following line to ``pg_hba.conf``::

    # TYPE  DATABASE    USER        CIDR-ADDRESS          METHOD
    host    all         all         127.0.0.1/32          md5

Then restart postgresql.

.. _the documentation:
   http://www.postgresql.org/docs/8.4/static/auth-pg-hba-conf.html


Database Creation
~~~~~~~~~~~~~~~~~

Create the database in the normal way for Django/PostgreSQL::

    sudo su postgres
    createuser -e -DRS -P mastrms
    createdb -e -O mastrms mastrms
    exit

The default database, username, password are all set to
*mastrms*. These settings can be changed, see (:ref:`django-settings`).

Database Population
~~~~~~~~~~~~~~~~~~~

Run Django syncdb and South migrate::

    sudo mastrms syncdb
    sudo mastrms migrate

Django will prompt to create a superuser. If you choose to create a
superuser, ensure the username and e-mail address are exactly the
same, otherwise you won't be able to log in.

Alternatively, you can use the preconfigured user
``admin@example.com`` with password ``admin`` to log in. Once you have
set up your own users, the ``admin@example.com`` user can be deleted.


Apache Web Server
~~~~~~~~~~~~~~~~~

The Mastr-MS RPM installs an example Apache config file at
``/etc/httpd/conf.d/mastrms.ccg``. This config is designed to work out
of the box with an otherwise unconfigured CentOS Apache
installation. All that is needed is to rename ``mastrms.ccg`` to
``mastrms.conf`` so that Apache will pick it up.

If you have already made changes to the default Apache configuration,
you may need to tweak ``mastrms.conf`` so that the existing setup is
not broken. It may be necessary to consult the `Apache`_ and
`mod_wsgi`_ documentation for this.

.. _Apache: http://httpd.apache.org/docs/2.2/
.. _mod_wsgi: http://code.google.com/p/modwsgi/wiki/ConfigurationGuidelines

..  _sync-user:

User Creation
~~~~~~~~~~~~~

It is a good idea to create a special user and group for data
syncing::

    SYNCUSER=maupload
    adduser $SYNCUSER
    su $SYNCUSER -c "mkdir --mode=700 /home/$SYNCUSER/.ssh"

..  _sync-repo:

Data Repository and Permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the data repository is located at
``/var/lib/mastrms/scratch``.

There should be ample disk space on this filesystem and some data
redundancy would be desirable. If this is not the case, then you could
mount a suitable file system at this path. If the data repository
needs to be at another location, its path can be configured in the
settings file.

The data sync user needs to be able to write to this directory, and
the web server user needs to be able to read from this directory, so::

    DATADIR=/var/lib/mastrms/scratch
    mkdir -p $DATADIR/files $DATADIR/quotes
    chown maupload:maupload $DATADIR $DATADIR/*
    chmod 2770 $DATADIR $DATADIR/*

Also add the web server user to the ``maupload`` group so that it can
read/write the data which ``maupload`` has rsynced in::

    usermod -a -G maupload apache

.. _django-settings:

Django Settings File
~~~~~~~~~~~~~~~~~~~~

The default settings for Mastr-MS are installed at
``/usr/local/webapps/mastrms/defaultsettings/mastrms.py``. In case any
settings need to be overridden, this can be done by creating an
optional appsettings file. To set up the appsettings file, do::

    mkdir -p /etc/ccgapps/appsettings
    touch /etc/ccgapps/appsettings/{__init__,mastrms}.py

The Python variable declarations in
``/etc/ccgapps/appsettings/mastrms.py`` will override the defaults,
which can be seen in `settings.py`_.

.. _settings.py:
   https://bitbucket.org/ccgmurdoch/mastr-ms/src/default/mastrms/mastrms/settings.py

SELinux and Mastr-MS
~~~~~~~~~~~~~~~~~~~~

Mastr-MS does not yet ship with a SELinux policy (issue `MAS-21`_).
For Mastr-MS to function correctly on a CentOS server, SELinux must be
disabled.

The CentOS wiki contains `instructions`_ on how to disable SELinux.

.. _MAS-21:
   https://ccgmurdoch.atlassian.net/browse/MAS-21

.. _instructions:
   http://wiki.centos.org/HowTos/SELinux#head-430e52f7f8a7b41ad5fc42a2f95d3e495d13d348


Upgrading to a new version
--------------------------

New versions of Mastr-MS are made available in the `CCG yum
repository`_.

.. warning:: Some versions will require "database migrations" to
   update the database. While every care is taken to ensure smooth
   upgrades, we still advise to make a backup of the database before
   upgrading. This can be done with a command such as::

       su - postgres -c "pg_dump mastrms | gzip > /tmp/mastrms-$(date +%Y%m%d).sql.gz"


Install the Mastr-MS RPM, replacing ``X.X.X`` with the desired version::

    sudo yum install mastrms-X.X.X

Run Django syncdb and South migrate::

    sudo mastrms syncdb
    sudo mastrms migrate

.. _CCG yum repository:
   http://repo.ccgapps.com.au/

Testing
-------

After changing the configuration or upgrading, start/restart the web
server with::

    service httpd restart

Mastr-MS is available at https://your-web-host/mastrms/. A login page
should be visible at this URL.


.. _administration:

Administration
--------------

There are two levels of administration necessary for Mastr-MS.

 * **Management**

   This involves administrating users, projects, quotes, experiments,
   etc. The URL for management is the normal Mastr-MS address, but
   only users who are in the admin group can see the interface.

   https://your-web-host/mastrms/

   The management interface is described in :ref:`usage`.

 * **Django Admin**

   This involves manipulation of database objects to configure the
   data sync system. Only admin users can access the address:

   https://your-web-host/mastrms/repoadmin/

   The Django Admin site can also be accessed from *Dashboard →
   Repository → Admin*.

.. _nodeclient-setup:

Data Sync Node Client Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configuration of a new site is done by adding a *Node client* using
the **Django Admin**. The fields should be set as follows.

+--------------------+------------------------------------------------+
| Field              | Description                                    |
+====================+================================================+
| Organisation name  | These values determine how the node is visible |
+--------------------+ in the data sync client.                       |
| Site name          |                                                |
+--------------------+                                                |
| Station name       |                                                |
+--------------------+------------------------------------------------+
| Default data path  | This should be a subdirectory of ``$DATADIR``  |
|                    | (see :ref:`sync-repo`).                        |
+--------------------+------------------------------------------------+
| Username           | This should be the data sync user              |
|                    | (see :ref:`sync-user`).                        |
+--------------------+------------------------------------------------+
| Hostname           | The hostname or IP address of the Mastr-MS     |
|                    | server.                                        |
+--------------------+------------------------------------------------+
| Flags              | This controls the options the data sync client |
|                    | will pass to rsync. They should always be set  |
|                    | to ``--protocol=30 -rzv --chmod=ug=rwX``.      |
+--------------------+------------------------------------------------+


.. _adding-keys:

Instrument Method Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before runs can be created, an *Instrument method* must be created
using the **Django Admin**. At present, the Instrument Method object
isn't used, but it must be set. The fields should be set as follows.

+--------------------+------------------------------------------------+
| Field              | Description                                    |
+====================+================================================+
| Title              | Default Method                                 |
+--------------------+------------------------------------------------+
| Method path        | TBD                                            |
+--------------------+------------------------------------------------+
| Method name        | Default Method                                 |
+--------------------+------------------------------------------------+
| Version            | 1                                              |
+--------------------+------------------------------------------------+
| Creator            | *Your own username*                            |
+--------------------+------------------------------------------------+
| Template           | TBD                                            |
+--------------------+------------------------------------------------+
| The other fields   | *Blank*                                        |
+--------------------+------------------------------------------------+

Standard Operating Procedure Documents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you would like to make SOP documents available for viewing, you can
create objects in the Django Admin within the Repository / Standard
operation procedures page.

Once the documents are uploaded, they can be attached to experiments
and viewed through the Experiment Sample Preparation screen.


SSH Key Management
~~~~~~~~~~~~~~~~~~

When the data sync clients hit *Send Key*, it sends the client's
public key via a HTTP post to a URL at the Mastr-MS site, and a view
handles this, saving it to the ``publickeys`` directory on the
server. It then sends an e-mail to the admins configured for the site,
telling them that a new key has been uploaded, and they should append
it on to the ``authorized_keys`` for the data sync user.

To install the key, run::

     cat $DATADIR/files/publickeys/$ORG.$SITE.$STATION_id_rsa.pub \
         >> /home/$SYNCUSER/.ssh/authorized_keys

(Replace ``$DATADIR``, ``$SYNCUSER`` and ``$ORG.$SITE.$STATION`` with
your actual settings and the information from the e-mail.)

Once the key is added, the client should be able to "Handshake" with
the server (see :ref:`client-config`).

If the key isn't working, try checking the `authorized_keys
permissions`_.

.. _authorized_keys permissions:
   http://www.openssh.org/faq.html#3.14
