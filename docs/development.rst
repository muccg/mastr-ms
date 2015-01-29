Mastr-MS Development
====================

This document is intended for developers who wish to change Mastr-MS
or see how it works.

Mastr-MS is Django web application and works with both PostgreSQL and
MySQL.


Source Code
-----------

The Mastr-MS code is hosted at BitBucket.

    https://bitbucket.org/ccgmurdoch/mastr-ms

Git_ is required to check out the code.

.. _Git: http://git-scm.com/


Issue Tracking
--------------

All new bugs/feature requests should be submitted to the issue tracker:

    https://bitbucket.org/ccgmurdoch/mastr-ms/issues/new

If all significant changes have a ticket associated, then release
notes can be accurately generated.

Mastr-MS was originally hosted on Google Code, where there still
remains a small bug list:

    http://code.google.com/p/mastr-ms/issues/list


Development Environment
-----------------------

We develop on Ubuntu. Installing the following packages is
recommended::

    sudo apt-get install postgresql-server \
        ipython python-pip python-sphinx \
        python-wxgtk2.8 xvfb xserver-xephyr


Packages helpful but not really required::

        python-django \
        python-werkzeug python-django-extensions \
        python-selenium chromium-chromedriver \


Building a CentOS RPM
---------------------

The RPM build is unlikely to work unless done under CentOS. Assuming
the Mastr-MS source code is checked out at ``/usr/local/src``, you can
build an RPM in more-or-less the normal way by running these
commands::

    CCGSOURCEDIR=/usr/local/src
    export CCGSOURCEDIR
    cd $CCGSOURCEDIR && rpmbuild -bb centos/mastrms.spec

The spec file requires ``CCGSOURCEDIR`` to be set. It will download
all the python dependencies with ``pip``, create the RPM, and output
it to ``~/rpmbuild/RPMS`` (or the location you have configured in
``~/.rpmrc``).

How to build the sync client
----------------------------

The support libraries and binaries are in the
``mdatasync_client/client/supportwin32`` directory.

You should be able to build the client on a 32-bit Windows XP box, by
installing these resources as described below.

Initial Setup of build environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Copy client and supportwin32 over to the windows machine.
#. Install Python27 (utf8 encoding for json is broken in earlier versions)
#. Install wx for python 2.7
#. Install py2exe for python 2.7
#. Install NSIS
#. Install 7Zip
#. Extract the ``EnvVarUpdate`` extension
#. Copy the extension into ``c:\program files\nsis\include``
#. Open a shell
#. Change dir to the ``client`` dir

Building the code
~~~~~~~~~~~~~~~~~

First, make sure you have updated the version number in ``version.py``
to be unique, and sequentially higher than previous ones.

On Windows box, get the latest client dir. Run::

    c:\Python27\python.exe setup.py bdist_esky

Then unzip the build you just did (in ``dist/``) so that the files are
available to the installer.

If you then ran the ``nsi`` file (right click on the file and choose
'Compile with NSIS'), it would make an installer, using the build you
just did (in ``/dist``) as a source. So that is how you make an
installer.

If you want to publish just the update, you take the ``.zip`` that is
generated in the ``dist`` directory, and ``scp`` it to the
distribution URL. Currently, this is on S3, under
http://repo.ccgapps.com.au/ma/

As long as the ``version.py`` version was incremented, a new version
will be available to esky.

Errors
~~~~~~

When building with Esky, if you get the message ``cannot access
../main.py. The file is in use by another process/``, this probably
means your python code fails a syntax check or has some other runtime
error.


Running Tests
-------------

Testing requirements:
   * wxpython
   * Xvfb
   * selenium
   * chrome/firefox webdriver
   * splinter
   * dingus
   * python xvfbwrapper

Command to run::

    ./manage.py test --exclude=yaphc --exclude=esky --exclude=httplib2

Testing
-------

Mastr-MS contains some system tests as well as unit tests. The current
test classes are:

    * :class:`mastrms.mdatasync_client.client.test.tests.BasicClientTests`
    * :class:`mastrms.mdatasync_client.client.test.tests.DataSyncServerTests`
    * :class:`mastrms.mdatasync_server.tests.SyncTests`
    * :class:`mastrms.mdatasync_server.tests.AdminTests`


The WxPython client is tested using the :class:`TestClient`
class. :class:`TestClient` runs the client in a thread and allows
"clicking" on GUI buttons by calling the associated event handlers.

.. autoclass:: mastrms.mdatasync_client.client.test.TestClient
   :members:

To generate sample data files like the lab instrument software would
create, use the :class:`Simulator` class. Simulator can be run as a
standalone WxPython GUI, or operated programmatically through
:class:`Worklist`.

.. autoclass:: mastrms.mdatasync_client.client.Simulator.Simulator
   :members:

.. autoclass:: mastrms.mdatasync_client.client.Simulator.WorkList

For testing you usually don't want to do actual file transfers, but
you do want to check that ``rsync`` was called. For this, we put a
mock command into the ``PATH`` which can be queried from the test cases.

.. autoclass:: mastrms.mdatasync_client.client.test.fake_rsync.FakeRsync

Documentation
-------------

The documentation is in :ref:`Sphinx <sphinx:contents>` format under
the ``docs`` subdirectory of the source. To build it, simply run::

    make html


Product Overview
----------------

This list, written by Brad, may be useful in understanding the system.

Goals of MASTR
~~~~~~~~~~~~~~

 * To provide a web based tool for experimental design, sample
   metadata configuration, and sample data acquisition.

 * To enable researchers and scientists from geographically separate
   institutions to work together on experiments, analysis, and to be
   able to share results and outcomes.

 * To enable institutions to provide quotes for analysis work to
   third-parties, with automatic linkage through to the relevant
   projects and experiments.

Features of MASTR
~~~~~~~~~~~~~~~~~

 * User / Group administration
 * Experimental design, catering for:
    * User roles and access control
    * Sample origin metadata
    * Sample timeline and treatment metadata
    * Sample tracking
    * Sample information import / export via CSV
    * Standard Operating Procedure upload
    * Run creation, generating worklists for the purposes of
      instrument automation.
    * Fully customisable rules system for worklist generation
    * Sample blocks, order, randomisation, and solvents/blanks can be
      specified as a programmable template.
    * Worklist rulesets can be rolled out per individual, or shared
      with groups or the entire institution
    * Rulesets can be branched and cloned
    * Runs and Experiments can also be cloned for convenience.

 * Data acquisition, consisting of:
    * A program which runs on the computer connected to the instrument
      which processes MASTR worklists
    * The program will check periodically for filesets related to
      experiment runs being performed for MASTR
    * The sample data is compressed and uploaded to the
      MASTR-connected storage, and optionally archived on the client
      machine.
    * The sample data is then securely available to relevant users
      through the MASTR web interface for viewing or download.
    * Full end-to-end data acquisition, from experimental design to
      sample file access.

 * Quote requests and tracking
    * A system for third parties to request quotes for analysis work
      of any of the institutions in MASTR
    * Institution Administrators or Node Representatives can review
      the requests and service replies, with optional PDF attachments.
    * Full quote event history is maintained.
    * Quotes in the system can be linked to Projects / Experiments

 * Modern technologies
    * Able to be accessed in all major web browsers
    * Lightweight and powerful UI
    * Open data formats and transports used (rsync, json)
    * Open Source code repository


Auto-generated Documentation
----------------------------

.. toctree::
    tests
