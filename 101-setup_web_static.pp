# Configures a web server for deployment of web_static using Puppet

$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location / {
        try_files \$uri \$uri/ =404;
    }
}"

package { 'nginx':
  ensure   => 'installed',
  provider => 'apt',
}

file { ['/data',
        '/data/web_static',
        '/data/web_static/releases',
        '/data/web_static/releases/test',
        '/data/web_static/shared']:
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  content => "<html>\n  <head>\n  </head>\n  <body>\n    School\n  </body>\n</html>\n",
  require => File['/data/web_static/releases/test'],
}

file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  force   => true,
  require => File['/data/web_static/releases/test'],
}

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf,
  require => Package['nginx'],
  notify  => Service['nginx'],
}

service { 'nginx':
  ensure    => 'running',
  enable    => true,
  require   => Package['nginx'],
  subscribe => File['/etc/nginx/sites-available/default'],
}
