#
node default {
  include ccgcommon
  include ccgcommon::source
  include ccgapache
  include python
  include postgresql::devel
  include repo::epel
  include repo::ius
  include repo::ccgtesting

  # tests need wxPython and virtual X server, firefox required for selenium
  $packages = [
    'rsync',
    'mysql-devel',
    'wxPython',
    'xorg-x11-server-Xvfb',
    'dbus-x11',
    'firefox']
  package { $packages: ensure => installed }

  ccgdatabase::postgresql { 'mastrms':
    user     => 'mastrms',
    password => 'mastrms',
  }
}
