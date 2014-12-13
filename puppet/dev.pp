#
node default {
  include ccgcommon
  include ccgcommon::source
  include ccgapache
  include python
  include ccgdatabase::postgresql::devel
  include repo
  include repo::upgrade
  include repo::repo::ius
  include repo::repo::ccgtesting
  class { 'yum::repo::pgdg93':
    stage => 'setup',
  }

  # tests need wxPython and virtual X server, firefox required for selenium
  $packages = [
    'rsync',
    'mysql-devel',
    'wxPython',
    'xorg-x11-server-Xvfb',
    'dbus-x11',
    'firefox']
  package { $packages: ensure => installed }

  ccgdatabase::postgresql::db { 'mastrms':
    user     => 'mastrms',
    password => 'mastrms',
  }
}
