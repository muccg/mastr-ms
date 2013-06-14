Mastr-MS
--------

Metabolomics Australia Sample Tracking Repository
-------------------------------------------------

Mastr-MS is a collaborative project undertaken by the Australian Bioinformatics Facility (ABF), located at the Centre for Comparative Genomics, for Metabolomics Australia (MA).

Mastr-MS is comprised of a number of modules:

User Management Module Provision of a secure, online user management module for the Metabolomics Australia Data and Sample Management System 
Sample Management Module Provision of a secure, online sample management module allowing users to submit samples, track samples through experimental workflows and receive results
Data Management Module Provision of secure, online metabolomics repository to capture all relevant MA experimental workflows. It includes storage of raw data files as well as all relevant meta data associated with an experiment

ABF Team
--------
Project Director:     Prof. Matthew Bellgard
Project Leader:       Adam Hunter
Software Developers   Rodney Lorrimar, Brad Power, Tamas Szabo, Maciej Radochonski, Nick Takayama, Andrew Macgregor
System Administrator  David Schibeci

MA Team
-------
MA Informatics Group Leader  Dr. Vladimir Likic
Computer Scientist           Dr. Saravanan Dayalan

Installation
------------
MastrMS is distributed as RPM, tested on Centos 6.x (x86_64). To satisfy dependencies, Epel (http://fedoraproject.org/wiki/EPEL) and REMI (http://rpms.famillecollet.com/) repos need to be enabled:

    sudo rpm -Uvh http://repo.ccgapps.com.au/repo/ccg/centos/6/os/noarch/CentOS/RPMS/ccg-release-6-1.noarch.rpm
    sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    sudo rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm

Then install the Mastr-MS RPM:

    sudo yum install mastrms-X.X.X-X

Run Django syncdb and South migrate:

    sudo mastrms syncdb
    sudo mastrms migrate
