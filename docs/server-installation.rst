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

Install the Mastr-MS RPM, replacing ``X.X.X`` with the desired version::

    sudo yum install python-psycopg2 mastrms-X.X.X

Run Django syncdb and South migrate::

    sudo mastrms syncdb
    sudo mastrms migrate


Server Configuration
--------------------

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

It is a good idea to create a special user for data syncing::

    SYNCUSER=maupload
    sudo adduser $SYNCUSER
    sudo su $SYNCUSER -c "mkdir --mode=700 /home/$SYNCUSER/.ssh"

..  _sync-repo:

Data Repository and Permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the data repository is located at
``/var/lib/mastrms/scratch``.

There should be ample disk space on this filesystem and some data
redundancy would be desirable. If this is not the case, then you could
mount a suitable file system at this path.

The data sync user needs to be able to write to this directory, and
the web server user needs to be able to read from this directory, so::

    DATADIR=/var/lib/mastrms/scratch
    sudo chown maupload:apache $DATADIR
    sudo chmod 750 $DATADIR

If the data repository needs to be at another location, its path can
be configured in the settings file.

Django Settings File
~~~~~~~~~~~~~~~~~~~~

The default settings for Mastr-MS are installed at
``/usr/local/webapps/mastrms/defaultsettings/mastrms.py``. In case any
settings need to be overridden, this can be done by creating an
optional appsettings file. To set up the appsettings file, do::

    sudo mkdir -p /etc/ccgapps/appsettings
    sudo touch /etc/ccgapps/appsettings/{__init__,mastrms}.py

The Python variable declarations in
``/etc/ccgapps/appsettings/mastrms.py`` will override the defaults,
which can be seen in `settings.py`_.

.. _settings.py:
   https://bitbucket.org/ccgmurdoch/mastr-ms/src/default/mastrms/mastrms/settings.py


Testing
-------

After changing the configuration, start/restart the web server with::

    service httpd restart

Mastr-MS is available at https://your-web-host/mastrms/. A login page
should be visible at this URL.


Administration
--------------

There are two levels of administration necessary for Mastr-MS.

 * **Management**

   This involves administrating users, projects, quotes, experiments,
   etc. The URL for management is the normal Mastr-MS address, but
   only users who are in the admin group can see the interface.

   https://your-web-host/mastrms/

 * **Django Admin**

   This involves manipulation of database objects to configure the
   data sync system. Only admin users can access the address:

   https://your-web-host/mastrms/repoadmin/


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
| Hostname           | The hostname of the Mastr-MS server.           |
+--------------------+------------------------------------------------+
| Flags              | This controls the options the data sync client |
|                    | will pass to rsync. They should always be set  |
|                    | to ``--protocol=30 -rzv --chmod=ug=rwX``.      |
+--------------------+------------------------------------------------+


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
