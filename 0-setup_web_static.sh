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

if grep -q "location /hbnb_static" /etc/nginx/sites-available/default; then
    sed -i '/location \/hbnb_static/,/}/d' /etc/nginx/sites-available/default
fi
if grep -q "server_name" /etc/nginx/sites-available/default; then
    sed -i '/server_name/a \    location /hbnb_static {\n        alias /data/web_static/current;\n        index index.html index.htm;\n    }' /etc/nginx/sites-available/default
else
    sed -i '/listen 80/a \    location /hbnb_static {\n        alias /data/web_static/current;\n        index index.html index.htm;\n    }' /etc/nginx/sites-available/default
fi

service nginx restart

exit 0
