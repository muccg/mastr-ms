.. _changelog:

Release Notes
=============

This page lists what changed in each Mastr-MS version. For
instructions on how to upgrade the server, see
:ref:`server-upgrade`. For instructions on how to upgrade the datasync
client, see :ref:`client-upgrade`.


.. _1.11.4:

1.11.4 (8th December 2014)
-------------------------

Bug fix release.

 * [MAS-76] - Migration from empty database broke


.. _1.11.3:

1.11.3 (19th November 2014)
-------------------------

Bug fix release.

 * [MAS-74] - Put investigation name in ISA-Tab files


.. _client-0.4.9:

Client 0.4.9 (22nd October 2014)
--------------------------------

  Datasync client bug fix release.

 * [MAS-75] - Datasync client doesn't support quoting in rsync config


.. _1.11.2:

1.11.2 (22nd October 2014)
-------------------------

New feature release.

 * [MAS-73] - Provide a direct URL to the registration screen


.. _1.11.1:

1.11.1 (1st September 2014)
-------------------------

Bug fix release.

 * [MAS-72] - Always output JSON format from API


.. _1.11.0:

1.11.0 (28th August 2014)
-------------------------

New feature release. Contains database migrations.

 * [MAS-69] - ISA-TAB export: Put experiment samples in the same
   investigation if they are the same samples

 * [MAS-71] - Update Django to 1.6.6


.. _1.10.1:

1.10.1 (7th August 2014)
------------------------

Bug fix release. Contains database migrations.

 * [MAS-68] - Handle migration of users with no e-mail address


.. _1.10.0:

1.10.0 (7th August 2014)
------------------------

New feature release.

 * [MAS-66] - Increase length of usernames
 * [MAS-67] - Enable user logging in production again

This release contains database migrations which need to be run after
upgrading the RPM. User e-mail addresses must be unique now. The
migration process will change duplicate e-mail addresses. If any
e-mail addresses were changed, it will say so. You must then clean up
those users from the admin page.

If the database migration fails due to an error with the ``userlog_*``
tables, just drop them and try the migration again::

    # mastrms dbshell
    DROP TABLE "userlog_loginlog";
    DROP TABLE "userlog_failedloginlog";


.. _1.9.4:

1.9.4 (23rd June 2014)
----------------------

Bug fix release.

 * [MAS-65] - Change title MA LIMS to MASTR-MS


.. _1.9.3:

1.9.3 (5th June 2014)
---------------------

Bug fix release.

 * [MAS-64] - Make ISA-Tab output validate with isatools validator


.. _1.9.2:

1.9.2 (29th May 2014)
---------------------

New feature release.

 * [MAS-61] - Produce ISA-Tab study and assay files
 * [MAS-62] - Update Django to 1.6.4
 * [MAS-63] - Improve environment variable config code


.. _1.9.1:

1.9.1 (1st May 2014)
---------------------

New feature release.

 * [MAS-61] - Add ISA-Tab fields for study and assay


.. _1.9.0:

1.9.0 (13th Mar 2014)
---------------------

New feature release.

 * [MAS-59] - ISA-TAB format export


.. _1.8.2:

1.8.2 (20th Feb 2014)
---------------------

Bug fix release. You can now put multiple space-separated values for
``allowed_hosts`` and ``memcache`` in ``/etc/mastrms/mastrms.conf``.

 * [MAS-55] - Missing samples labels etc when cloning experiments
 * [MAS-56] - CSV upload broke with python27-mod_wsgi
 * [MAS-57] - Client code using extjs grid is saving null sample weights
 * [MAS-60] - Settings: multiple memcache servers and allowed hosts


.. _1.8.1:

1.8.1 (31st Jan 2014)
---------------------

Bug fix release. More options were added to the default config files.

 * [MAS-54] - Add wider menu of settings in mastrms.conf


.. _1.8.0:

1.8.0 (30th Jan 2014)
---------------------

New feature and bug fix release.

Mastr-MS now requires the IUS repo. It can be added according to the
instructions in :ref:`yum-repos`. If you get dependency errors on
installation, it is probably because the ius-release_ RPM isn't
installed.

.. _ius-release: http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/repoview/ius-release.html

.. note:: In this version the format of the config file has
   changed. You will need to manually update the settings.

The settings are no longer stored in
``/etc/ccgapps/appsettings``. They are now in ``/etc/mastrms``. After
installing the RPM, edit ``/etc/mastrms/mastrms.conf`` and copy in
just the listed settings from ``/etc/ccgapps/appsettings/mastrms.py``.

After restarting the web server and checking that it works, the old
settings file can be moved into a backup location.

 * [MAS-52] - Switch RPM to new build method
 * [MAS-53] - Fix file extension in worklist


.. _1.7.0:

1.7.0 (19th Dec 2013)
---------------------

New feature release

 * [MAS-49] - General File Extension (Issue 132)
 * [MAS-50] - Renaming files in file manager


.. _1.6.2:

1.6.2 (26th Nov 2013)
---------------------

Bug fix release

 * [MAS-45] - Put run QC data as a subfolder of experiment data


.. _1.6.0:

1.6.0 (25th Nov 2013)
---------------------

New feature release

Bug fixes
 * [MAS-48] - CSV import -- should ignore empty weight values
Improvements
 * [MAS-45] - Put run QC data as a subfolder of experiment data
 * [MAS-47] - Allow creation of own folders within experiment files
