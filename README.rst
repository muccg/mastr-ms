Mastr-MS
========

Mastr-MS is a web-based tool for experimental design, sample metadata configuration, and sample data acquisition. Developed at the Centre for Comparative Genomics (https://ccg.murdoch.edu.au/) in partnership with Metabolomics Australia (https://www.metabolomics.com.au/).

Documentation
-------------

Full documentation is available at https://mastr-ms.readthedocs.org/
or within the ``docs`` subdirectory of this source distribution.

Licence
-------

GNU GPL v3. Please contact the Centre for Comparative Genomics if you
require a licence other than GPL for legal or commercial reasons.

For developers
--------------

We do our development using Docker containers. See: https://www.docker.com/.
You will have to set up Docker on your development machine.

All the development tasks can be done by using the ``develop.sh`` shell script in this directory.
Please run it without any arguments for help on its usage. The script is a convenience wrapper around docker-compose,
so naturally docker-compose (or docker for that matter) can be used directly. The script will echo all the docker-compose
commands it executes.

We typically run a local squid proxy (https://github.com/muccg/docker-squid-deb-proxy) and pypi proxy (https://github.com/muccg/docker-devpi)
in our dev environment. You can remove this dependency by editing the ``.env`` file in the top level directory. Specifically
the variables CCG_PIP_PROXY and CCG_HTTP_PROXY control usage of the local proxies during builds.

Some typical usages of the convenience develop.sh script are:

- ./develop.sh build base builder dev
        To build all the docker containers needed for dev.

- ./develop.sh up
        To start up all the docker containers needed for dev. 
        You can access the Mastrms application on http://localhost:8000.
        You can login with *admin@example.com/admin*, *staff@example.com/staff*, *client@example.com/client*.

- ./develop.sh run-unittests
        Starts up all the docker containers and runs all our tests against them.

Our production Docker image (``Dockerfile-prod``) is built by creating a tarball of the application and placing it the base image (``Dockerfile-base``)
which is a Debian image and dependencies. Steps for building prod image:

- ./develop.sh build base builder
        Build base image and builder image.

- ./develop.sh run-builder
        Run the builder image to make a tarball of the application.

- ./develop.sh build prod
        Build the prod image.

The prod image exposes the application via uwsgi, we typically deploy that behind nginx. We've also done RPM + Apache + mod_wsgi deployments but are not
actively updating RPM deployments and will likely remove that from the REPO in the near future.

Contributing
------------

1. Fork next_release branch
2. Make changes on a feature branch
3. Submit pull request

Latest Releases
---------------

1.14.0_  (27th May 2016)
  New feature release. Contains database migrations.

.. _1.14.0: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.14.0


1.13.0_  (4th August 2015)
  Initial Debian/Ubuntu package release.

.. _1.13.0: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.13.0


1.12.3_  (16th June 2015)
  Bug fix release.

.. _1.12.3: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.12.3


1.12.2_  (6th March 2015)
  Brown paper bag release.

.. _1.12.2: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.12.2


1.12.1_  (6th March 2015)
  Bug fix release. Contains database migrations.

.. _1.12.1: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.12.1


1.12.0_  (5th March 2015)
  Bug fix release. Contains database migrations.

.. _1.12.0: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.12.0


1.11.4_  (8th December 2014)
  Bug fix release.

.. _1.11.4: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.11.4


1.11.3_  (19th November 2014)
  Bug fix release.

.. _1.11.3: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.11.3


client-0.4.9_ (22nd October 2014)
  Datasync client bug fix release.

.. _client-0.4.9: http://mastr-ms.readthedocs.org/en/latest/changelog.html#client-0.4.9


1.11.2_  (22nd October 2014)
  New feature release.

.. _1.11.2: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.11.2


1.11.1_  (1st September 2014)
  Bug fix release.

.. _1.11.1: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.11.1


1.11.0_  (28th August 2014)
  New feature release. Contains database migrations.

.. _1.11.0: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.11.0


1.10.1_ (7th August 2014)
  Bug fix release.

.. _1.10.1: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.10.1


1.10.0_ (7th August 2014)
  New feature release. Contains database migrations.

.. _1.10.0: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.10.0


1.9.4_ (23rd June 2014)
  Bug fix release.

.. _1.9.4: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.9.4


1.9.3_ (5th June 2014)
  Bug fix release.

.. _1.9.3: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.9.3


1.9.2_ (29th May 2014)
  New feature release.

.. _1.9.2: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.9.2


1.9.1_ (1st May 2014)
  New feature release.

.. _1.9.1: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.9.1


1.9.0_ (13th Mar 2014)
  New feature release.

.. _1.9.0: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.9.0


1.8.2_ (20th Feb 2014)
  Bugfix release. Contains config file changes.

.. _1.8.2: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.8.2


1.8.1_ (31st Jan 2014)
  Bugfix release. Contains config file changes.

.. _1.8.1: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.8.1


1.8.0_ (30th Jan 2014)
  New feature and bugfix release. Contains config file changes.

.. _1.8.0: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.8.0


1.7.0_ (19th Dec 2013)
  New feature release

.. _1.7.0: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.7.0


1.6.2_ (28th Nov 2013)
  Bug fix release

.. _1.6.2: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.6.2


1.6.0_ (25th Nov 2013)
  New feature release

.. _1.6.0: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.6.0


1.5.2_ (18th Nov 2013)
  Bug fix release

.. _1.5.2: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.5.2


1.5.1_ (11th Nov 2013)
  New feature release

.. _1.5.1: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.5.1


1.4.1_ (13th Sep 2013)
  Bug fix release

.. _1.4.1: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.4.1


1.5.0_ (14th Oct 2013)
  Bug fix release

.. _1.5.0: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.5.0


1.4.0_ (12th Sep 2013)
  Bug fix release

.. _1.4.0: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.4.0


1.3.1_ (4th Sep 2013)
  Bug fix release with schema migrations

.. _1.3.1: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.3.1


client-0.4.8_ (26th Aug 2013)
  Datasync client bug fix release

.. _client-0.4.8: http://mastr-ms.readthedocs.org/en/latest/changelog.html#client-0.4.8


client-0.4.7_ (14th Aug 2013)
  Datasync client bug fix release

.. _client-0.4.7: http://mastr-ms.readthedocs.org/en/latest/changelog.html#client-0.4.7


1.2.6_ (13th Aug 2013)
  New feature and bug fix release

.. _1.2.6: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.2.6


client-0.4.6_ (15th Jul 2013)
  Datasync client bug fix release

.. _client-0.4.6: http://mastr-ms.readthedocs.org/en/latest/changelog.html#client-0.4.6


1.2.5_ (12th Jul 2013)

.. _1.2.5: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.2.5


1.2.4_ (1st Jul 2013)

.. _1.2.4: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.2.4


client-0.4.5_ (14th Jun 2013)
  Datasync client bug fix release

.. _client-0.4.5: http://mastr-ms.readthedocs.org/en/latest/changelog.html#client-0.4.5


1.2.3_ (13th Jun 2013)

.. _1.2.3: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.2.3


1.2.2_ (3rd Jun 2013)

.. _1.2.2: http://mastr-ms.readthedocs.org/en/latest/changelog.html#1.2.2
