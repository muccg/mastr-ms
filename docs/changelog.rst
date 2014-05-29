.. _changelog:

Release Notes
=============

This page lists what changed in each Mastr-MS version. For
instructions on how to upgrade the server, see
:ref:`server-upgrade`. For instructions on how to upgrade the datasync
client, see :ref:`client-upgrade`.

.. _1.9.2:

1.9.2 (29th May 2014)
---------------------

New feature release.

 * [MAS-61] - Produce ISA-Tab study and assay files
 * [MAS-62] - Update Django to 1.6.4


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
