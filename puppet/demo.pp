# This is a manifest for a demonstration (non-production) of Mastr-MS
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
    'deployment' => 'demo',
    'dbdriver'   => 'django.db.backends.postgresql_psycopg2',
    'dbhost'     => '',
    'dbname'     => 'mastrms_demo',
    'dbuser'     => 'mastrms',
    'dbpass'     => 'ns2bJzhd',
    'memcache'   => $globals::memcache_syd,
    'secretkey'  => 'ouit!ry6lz_@u!6ctd4o)fgnm73eqkp1+rp3bi^=08&6c!+7bq'}

  ccgdatabase::postgresql { $django_config['dbname']:
    user     => $django_config['dbuser'],
    password => $django_config['dbpass'],
  }

  package {'mastrms': ensure => installed, provider => 'yum_nogpgcheck'}

  django::config {'mastrms':
    config_hash => $django_config,
  }

  django::syncdbmigrate{'mastrms':
    dbsync  => true,
    require => [
      Ccgdatabase::Postgresql[$django_config['dbname']],
      Package['mastrms'] ]
  }
}
