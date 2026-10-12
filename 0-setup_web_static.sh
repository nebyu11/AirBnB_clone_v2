#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

apt-get update -y
apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

cat << 'EOF' > /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    School
  </body>
</html>
EOF

rm -rf /data/web_static/current
ln -s /data/web_static/releases/test /data/web_static/current

chown -R ubuntu:ubuntu /data/

if ! grep -q "location /hbnb_static" /etc/nginx/sites-available/default; then
    sed -i '/server_name _;/a \    location /hbnb_static/ {\n        alias /data/web_static/current/;\n    }' /etc/nginx/sites-available/default
fi

service nginx restart

exit 0
