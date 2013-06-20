Mastr-MS Development
====================

1. copy and paste e-mails

2. jira

3. old link to google code

Mastrms was orignially hosted on google code.

https://code.google.com/p/mastr-ms/

Recently it was pushed to bit bucket:

https://bitbucket.org/ccgmurdoch/mastr-ms

4. checking out

5. building rpm

6. running tests
   Testing requirements:
   * wxpython
   * Xvfb
   * selenium
   * chrome webdriver


Brad's Description of Mastr-MS
==============================

Goals of MASTR

* To provide a web based tool for experimental design, sample metadata
configuration, and sample data acquisition.
* To enable researchers and scientists from geographically separate
institutions to work together on experiments, analysis, and to be able
to share results and outcomes.
* To enable institutions to provide quotes for analysis work to
third-parties, with automatic linkage through to the relevant projects
and experiments.

Features of MASTR
* User / Group administration
* Experimental design, catering for:
* User roles and access control
* Sample origin metadata
* Sample timeline and treatment metadata
* Sample tracking
* Sample information import / export via CSV
* Standard Operating Procedure upload
* Run creation, generating worklists for the purposes of instrument
automation.
* Fully customisable rules system for worklist generation
* Sample blocks, order, randomisation, and solvents/blanks can
be specified as a programmable template.
* Worklist rulesets can be rolled out per individual, or shared
with groups or the entire institution
* Rulesets can be branched and cloned
* Runs and Experiments can also be cloned for convenience.

* Data acquisition, consisting of:
* A program which runs on the computer connected to the instrument
which processes MASTR worklists
* The program will check periodically for filesets related to
experiment runs being performed for MASTR
* The sample data is compressed and uploaded to the MASTR-connected
storage, and optionally archived on the client machine.
* The sample data is then securely available to relevant users
through the MASTR web interface for viewing or download.
* Full end-to-end data acquisition, from experimental design to
sample file access.

* Quote requests and tracking
* A system for third parties to request quotes for analysis work of
any of the institutions in MASTR
* Institution Administrators or Node Representatives can review the
requests and service replies, with optional PDF attachments.
* Full quote event history is maintained.
* Quotes in the system can be linked to Projects / Experiments

* Modern technologies
* Able to be accessed in all major web browsers
* Lightweight and powerful UI
* Open data formats and transports used (rsync, json)
* Open Source code repository


Documentation which needs merging
=================================

  INSTALL        --> client-install.rst
  BUILD_HOWO     --> dev-client-build-howto.rst
  WXPYTHON_HOWTO --> dev-wxpython-howto.rst
