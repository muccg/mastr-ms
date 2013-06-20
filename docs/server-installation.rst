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



Brad's Text
===========

Hi Maceij

Here are some of the more important details about Mastr and the data 
sync client that you might need to refer to in future:

- Sync client installation packages and updates should be uploaded to 
Faramir. They go in /usr/local/python/htdocs/ma
- The rsync account for maupload is on minerva.
     Username: maupload
     Password: tub=gerc
     Obviously all the clients authenticate using public key, so none of 
them know this password. I use it for testing though. The data that gets 
synced to minerva ends up accessible to the webserver somehow - either 
through some network mount or some other sysadmin voodoo. We 
occasionally have had problems with permissions - the sync clients at 
times have not been able to write files or the rsync daemon hasn't been 
able to create directories. This is pretty much a thing of the past and 
I believe it was just configuration that was needed, which Mark O'Shea 
sorted out.
- When the data sync clients hit 'send key' it sends the client's public 
key via a HTTP post to a URL at the mastrms site, and a view handles 
this, saving it to the publickeys directory on the server. It then sends 
an email to the admins configured for the site, telling them that a new 
key has been uploaded, and they should append it on to the 
authorized_keys for the maupload user.
- The Handshake button just does an rsync connection to the server 
without sending any data. It is a good way to test that the public key 
auth is working. Since the initial 'Do you want to trust this host' 
prompt still comes up in a DOS box on the client machines, I normally 
get the client to hit this button during installation - it helps get 
that prompt out of the way.
- Rsync flags: pretty much the minimum set you need when setting up a 
new client is:
     --protocol=30 -rzv --chmod=ug=rwX
you enter this on the server admin under Node Clients - each node client 
has a flags section.
