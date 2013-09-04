.. _usage:

Using the System
================

The experiment design and sample management features of Mastr-MS are
accessed through a web browser.

User Registration
-----------------

The preferred way to create users is to have the user request an
account. This can be done from the Login screen.

When someone requests an account, they are added to the Pending user
list, and the registration contact is e-mailed. This e-mail address is
configured with the ``REGISTRATION_TO_EMAIL`` setting (see
:ref:`django-settings`).

The user can then be enabled by the "Admin Requests" screen.

.. tip:: User management is described in the *Admin screencast:
         Accepting/Rejecting users*.

An administrator user can also create users through the *Users*
section of the Django Admin interface (see
:ref:`administration`). When using this interface, be careful to
ensure that the username and e-mail address are the same, and all
users are at least members of the *User* group.

User Roles
----------

Users can have different roles which determine what they can see and
change in the system.

 * **Administrators** can do see all data and perform any action in
   the Mastr-MS system. Such users also have permission to edit
   objects in the *Django Admin* (see :ref:`administration`).

 * **Node Reps** can edit the list of nodes and organisations. They
   can also grant user account requests and edit users in their node.

 * **Mastr Administrators** can edit users and edit all aspects of
   projects and experiments.

 * **Project Leaders** can edit users and edit all aspects of projects
   and experiments.

 * **Mastr Staff** can edit all aspects of projects and experiments.

If users do not have any of these roles, then they are considered to
be **Clients**. Clients can only download experiment files.


Node Management
---------------

*Nodes* are a way of managing groups of users and directing quote
requests to the correct group.

Users can view and answer quote requests sent to their node.

The list of nodes can be edited through the *Admin → Node Management*
screen.

The pre-configured nodes can be deleted and replaced with one or more
nodes specific to your site.

Experiments
-----------

Experiments are grouped in *Projects* which have a designated client
user, as well as optional project manager users.

Rule Generators
---------------

Rule generators control the addition of QC, blank and sweep components
to experiment runs.

These components can be added at the beginning, end, or for every *n*
samples.

If the *Apply Sweep Rule* option is ticked for the rule generator, the
run builder will add a sweep component after each sample unless it is
a blank or sweep.

Rule generators cannot be changed once in use, in order not to corrupt
previously run experiments. You can however clone rule generators or
create new versions. Unwanted rule generators can be disabled.

At least one rule generator must exist before a run can be created.

Samples
-------

An experiment run requires information about the samples that will
constitute that run. Samples are typically generated from sample
classes or imported from CSV files.

Runs
----

Runs are created by selecting a set of samples and clicking *Add
Selected Samples to Run*. Previously created runs can also be cloned
into new runs.

Once you are happy with the run parameters and samples, you can start
the run by clicking the *Generate Worklist* button.

This will display a CSV worklist in a new browser window. The worklist
can then be copied and pasted into the lab instrument software.

.. note:: One important thing to note is that any web browser popup
   blocker must be disabled for the Mastr-MS web site.

   Otherwise you will not be able to see CSV worklists, which are
   opened in a new window.

   Most new web browsers have popup blockers enabled by default, but
   certain web addresses can be excluded from blocking.

After generating the worklist, the run is maked as "In Progress".


Data Sync
---------

The Mastr-MS data sync client periodically uploads new data found on
the lab machine into the data management system. The data sync client
is told by the Mastr-MS server which filenames to look for.

Once the samples data files are uploaded, the client marks that sample
as complete. The percentage of complete samples is shown in the
progress bar on the *Runs* page.

When all samples in a run are completed, the run is marked as
complete.

Getting the data
----------------

Sample data can be seen from the *Files* page of the
experiment. PBQCs, QCs and sweeps can be downloaded from the *Runs*
page.

To download the data files, expand the *Files* tree and click the
filename.

Importing metadata from file
----------------------------

Run and sample data can be imported from a `CSV`_ file. CSV files can
be created with a text editor or spreadsheet program and usually end
with the file extension ``.csv``.

.. _CSV: https://en.wikipedia.org/wiki/Comma-separated_values

Sample CSV Import
~~~~~~~~~~~~~~~~~

To import samples, first create a CSV file which looks something like
this::

    Label,Weight,Comment
    smplbla,1.234,Comment about the sample
    smplblb,2.345,Another sample

Click the *Upload CSV file* button on the *Samples* page, then choose
the file.

If you would like to update existing samples, first download the
sample CSV file (which contains an ``ID`` column), edit the fields,
then upload it again.

Completed Run Sample Data Import
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have sample data on the lab machine which was not created
through a worklist designed in Mastr-MS, and would like to add it to
the data management system, you can import it from the *Runs* page.

Set up a CSV file with a single column ``Filename`` and list the
filenames for the run.

Then click the *Capture Completed External Run* button and upload this
file. You also need to specify a name for this run and which machine
the data is on.
