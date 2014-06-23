#
node default {
  include globals
  include ccgcommon
  include ccgcommon::source
  include ccgapache
  include python
  include postgresql::devel
  include repo::epel
  include repo::ius
  include repo::ccgtesting

  # There are some leaked local secrets here we don't care about
  $django_config = {
    deployment       => 'staging',
    dbdriver         => 'django.db.backends.postgresql_psycopg2',
    dbserver         => '',
    dbname           => 'mastrms',
    dbuser           => 'mastrms',
    dbpass           => 'mastrms',
    upload_user      => 'maupload',
    httpd_user       => 'apache',
    repo_user        => 'apache',
    repo_group       => 'maupload',
    repo_files_root  => '/var/lib/mastrms/scratch/files',
    quote_files_root => '/var/lib/mastrms/scratch/quotes',
    memcache         => $globals::memcache_syd,
    secret_key       => 'sdfsdkj*&^*&^hhggHGHG3434'
  }

  # tests need wxPython and virtual X server, firefox required for selenium
  $packages = [
    'python-virtualenv',
    'rsync',
    'wxPython',
    'xorg-x11-server-Xvfb',
    'dbus-x11',
    'firefox']
  package { $packages: ensure => installed }

  ccgdatabase::postgresql { $django_config['dbname']:
    user     => $django_config['dbuser'],
    password => $django_config['dbpass'],
  }

  package { 'mastrms': ensure => installed, provider => 'yum_nogpgcheck'}

  django::config { 'mastrms':
    config_hash => $django_config,
  }

  django::syncdbmigrate{'mastrms':
    dbsync  => true,
    require => [
      Ccgdatabase::Postgresql[$django_config['dbname']],
      Package['mastrms'] ]
  }

  group {$django_config['upload_user']:
    ensure     => present,
    members    => [$django_config['httpd_user']],
    require    => Class['ccgapache']
  } ->

  user {$django_config['upload_user']:
    ensure     => present,
    gid        => $django_config['upload_user'],
    groups     => [$django_config['upload_user'], $django_config['httpd_user']],
    managehome => true,
  } ->

  file {"/home/${upload_user}/.ssh":
    ensure => directory,
    owner  => $django_config['upload_user'],
    group  => $django_config['upload_user'],
    mode   => '0700'
  } ->

  file {'/data':
    ensure => directory,
    mode   => '0755',
  } ->

  file {'/data/mastrms':
    ensure => directory,
    owner  => $django_config['httpd_user'],
    group  => $django_config['upload_user'],
    mode   => '2770',
  } ->

  file {'/data/mastrms/files':
    ensure => directory,
    owner  => $django_config['httpd_user'],
    group  => $django_config['upload_user'],
    mode   => '2770',
  } ->

  file {'/data/mastrms/quotes':
    ensure => directory,
    owner  => $django_config['httpd_user'],
    group  => $django_config['upload_user'],
    mode   => '2770',
  }
}
