Mastr-MS Server
===============

The Mastr-MS server is a Django application which provides a web
interface for user management, sample management, and access to
experiment data.

Mastr-MS is distributed as a RPM for Redhat systems and as a ``deb``
package for Debian and Ubuntu systems.

Installation on Debian/Ubuntu
-----------------------------

The ``deb`` package is known to work on Debian 8 (Jessie) and Ubuntu
14.04 LTS (Trusty Tahr).

.. _apt-repos:

Apt repository setup
~~~~~~~~~~~~~~~~~~~~

To get started, put the following lines in
``/etc/apt/sources.list.d/ccg.list``::

    # Centre for Comparative Genomics Ubuntu package repository
    deb http://repo.ccgapps.com.au/repo/ccg/ubuntu ccg ccg
    deb-src http://repo.ccgapps.com.au/repo/ccg/ubuntu ccg ccg

Then run (as root)::

    curl http://repo.ccgapps.com.au/repo/ccg/ubuntu/ccg-archive.asc | apt-key add -
    apt-get update

Database Setup
~~~~~~~~~~~~~~

The database server package isn't a dependency of the Mastr-MS
package, because it's possible to run the database on another
host. The database therefore needs to be installed manually::

    apt-get install postgresql
    service postgresql start
    update-rc.d postgresql enable

In order to benefit from automatic database initialization, the
database needs to be installed and running before installing Mastr-MS.

Install
~~~~~~~

To download and install Mastr-MS, run::

    apt-get install mastr-ms

Your database and web server will be automatically configured using
the Debconf system.

Manual database initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If using a remote database or otherwise manually setting up the
database, you should edit ``/etc/mastr-ms/database.conf`` and enter
the correct settings.

To then initialize an empty database for Mastr-MS, run::

    mastr-ms syncdb && mastr-ms migrate

Configuration
~~~~~~~~~~~~~

You can customize ``/etc/mastr-ms/mastr-ms.conf`` as needed for your
site. Each setting is documented in settings_.

After changing ``SELF_URL_PATH``, you must run this to update the database::

    mastr-ms set_site

The Apache config file is installed in
``/etc/apache2/conf-available/mastr-ms.conf`` and can be adjusted as
required.

Mastr-MS generally requires SSL to be enabled on the web server. If
this is not possible, add the following line to ``/etc/mastr-ms/settings.py``::

    SSL_FORCE = False


Testing
~~~~~~~

Reload the web server::

    service apache2 restart

Mastr-MS is available at https://your-web-host/mastr-ms/. A login page
should be visible at this URL.

Data Repository and Syncing
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default data repository location is
``/var/cache/mastr-ms/scratch``. This can be changed in the settings_
file or redirected with a symlink.

For production use, there should be ample disk space on this
filesystem and it should be backed up.

The package creates a user called ``mastr-ms`` which owns the data
repository directories.

To support data syncing, the ``mastr-ms`` user should be enabled and a
password-less SSH key pair generated for it.

Upgrading to a new version
~~~~~~~~~~~~~~~~~~~~~~~~~~

New versions of Mastr-MS are made available in the `CCG Apt
repository`_.

Before upgrading, please check the :ref:`changelog` for any
special information relating the new version.

Install the latest version, run::

    apt-get update && apt-get install mastr-ms

If there are any database migrations required, they will be run
automatically. A precautionary database backup will be created in
``/var/cache/dbconfig-common/backups``.

If you would like to manually migrate the database, just run::

    mastr-ms migrate

.. _CCG Apt repository:
   http://repo.ccgapps.com.au/


Installation on CentOS
----------------------

..  _yum-repos:

Yum repository setup
~~~~~~~~~~~~~~~~~~~~

The Mastr-MS RPM is made for on Centos 6.x (x86_64). To satisfy
dependencies, `Epel`_ and `IUS`_ repos need to be enabled::

    sudo rpm -Uvh http://repo.ccgapps.com.au/repo/ccg/centos/6/os/noarch/CentOS/RPMS/ccg-release-6-2.noarch.rpm
    sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    sudo rpm -Uvh http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-11.ius.centos6.noarch.rpm

.. _Epel: http://fedoraproject.org/wiki/EPEL
.. _IUS: http://iuscommunity.org

Dependencies
~~~~~~~~~~~~

The database server package isn't a dependency of the Mastr-MS RPM, so
it has to be installed manually::

    sudo yum install postgresql-server

.. note:: These instructions are written for PostgreSQL. With minor
   alterations (issue `MAS-32`_) Mastr-MS could work with
   MySQL/MariaDB, but at present only PostgreSQL is supported.

.. _MAS-32:
   https://ccgmurdoch.atlassian.net/browse/MAS-32


Install
~~~~~~~

Install the Mastr-MS RPM, replacing ``X.X.X`` with the desired version::

    sudo yum install mastrms-X.X.X


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

The config file for Mastr-MS is installed at
``/etc/mastrms/mastrms.conf``. It contains basic settings_ that need
to be changed for most sites, for example the database password.

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


.. _server-upgrade:

Upgrading to a new version
~~~~~~~~~~~~~~~~~~~~~~~~~~

New versions of Mastr-MS are made available in the `CCG yum
repository`_.

.. warning:: Some versions will require "database migrations" to
   update the database. While every care is taken to ensure smooth
   upgrades, we still advise to make a backup of the database before
   upgrading. This can be done with a command such as::

       su - postgres -c "pg_dump mastrms | gzip > /tmp/mastrms-$(date +%Y%m%d).sql.gz"

Before upgrading, please check the :ref:`changelog` for any
special information relating the new version.

Install the Mastr-MS RPM, replacing ``X.X.X`` with the desired version::

    sudo yum install mastrms-X.X.X

Run Django syncdb and South migrate::

    sudo mastrms syncdb
    sudo mastrms migrate

.. _CCG yum repository:
   http://repo.ccgapps.com.au/

Testing
~~~~~~~

After changing the configuration or upgrading, start/restart the web
server with::

    service httpd restart

Mastr-MS is available at https://your-web-host/mastrms/. A login page
should be visible at this URL.

.. _settings:

Mastr-MS Settings File
----------------------

The Mastr-MS settings file is called ``mastr-ms.conf`` or
``mastrms.conf`` depending on the system.

The following settings are customizable. There are also comments and
example values for each setting within the settings file.

+---------------------------+-----------------------------------------------------+
| Option                    | Description                                         |
+===========================+=====================================================+
| ``dbtype``                | Database backend -- always use ``pgsql``.           |
+---------------------------+-----------------------------------------------------+
| ``dbname``                | The rest are standard database connection           |
+---------------------------+ options.                                            |
| ``dbuser``                |                                                     |
+---------------------------+                                                     |
| ``dbpass``                |                                                     |
+---------------------------+-----------------------------------------------------+
| ``dbserver``              | Optional settings for remote database               |
+---------------------------+ connection.                                         |
| ``dbport``                |                                                     |
+---------------------------+-----------------------------------------------------+
| ``memcache``              | Optional connection string(s) for ``memcached``.    |
|                           | Multiple servers are separated by spaces.           |
+---------------------------+-----------------------------------------------------+
| ``allowed_hosts``         | Space-separated list of address permitted to access |
|                           | the server.  Wildcards can be used as in the        |
|                           | `ALLOWED_HOSTS`_ docs.                              |
+---------------------------+-----------------------------------------------------+
| ``server_email``          | "From" e-mail address for server-generated error    |
|                           | mails.                                              |
+---------------------------+-----------------------------------------------------+
| ``email_host``            | Details for SMTP server. User and password are      |
+---------------------------+ optional.                                           |
| ``email_port``            |                                                     |
+---------------------------+                                                     |
| ``email_host_user``       |                                                     |
+---------------------------+                                                     |
| ``email_host_password``   |                                                     |
+---------------------------+-----------------------------------------------------+
| ``alert_email``           | Where error messages are sent.                      |
+---------------------------+-----------------------------------------------------+
| ``return_email``          | The "From" address on e-mail sent by mastr-ms.      |
+---------------------------+-----------------------------------------------------+
| ``logs_to_email``         | E-mail address to receive datasync client log       |
|                           | notifications.                                      |
+---------------------------+-----------------------------------------------------+
| ``keys_to_email``         | E-mail address to receive datasync key upload       |
|                           | notifications.                                      |
+---------------------------+-----------------------------------------------------+
| ``registration_to_email`` | E-mail address to receive registration              |
|                           | requests.                                           |
+---------------------------+-----------------------------------------------------+
| ``repo_user``             | Mastr-MS will attempt to change ownership of data   |
+---------------------------+ files to this user and group.                       |
| ``repo_group``            |                                                     |
+---------------------------+-----------------------------------------------------+
| ``repo_files_root``       | Location of data files for experiments and quotes.  |
+---------------------------+                                                     |
| ``quote_files_root``      |                                                     |
+---------------------------+-----------------------------------------------------+
| ``secret_key``            | Needs to be a secret random string, can be          |
|                           | generated by a `key generator program`_.            |
+---------------------------+-----------------------------------------------------+
| ``self_url_path``         | This is the public URL which Mastr-MS is served     |
|                           | from. It is used for links and redirects.           |
+---------------------------+-----------------------------------------------------+

.. _`ALLOWED_HOSTS`: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
.. _`key generator program`: http://www.miniwebtool.com/django-secret-key-generator/

More advanced options appear in ``settings.py``. Any of the `Django
Settings`_ can be changed in this file.

.. _`Django Settings`: https://docs.djangoproject.com/en/1.6/ref/settings/


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
| Method path        | A folder path on the lab machine, e.g.         |
|                    | ``D:\mastrms``                                 |
+--------------------+------------------------------------------------+
| Method name        | Default Method                                 |
+--------------------+------------------------------------------------+
| Version            | 1                                              |
+--------------------+------------------------------------------------+
| Creator            | *Your own username*                            |
+--------------------+------------------------------------------------+
| Template           | CSV                                            |
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

.. _adding-keys:

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
