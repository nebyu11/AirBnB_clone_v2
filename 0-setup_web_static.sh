#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

apt-get update -y
apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

cat > /data/web_static/releases/test/index.html << 'EOF'
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

python3 -c "
import re
conf = '/etc/nginx/sites-available/default'
with open(conf) as f:
    c = f.read()
c = re.sub(r'\n?[ \t]*location /hbnb_static/[^}]*\}', '', c, flags=re.DOTALL)
c = re.sub(
    r'([ \t]*server_name[^\n]+\n)',
    r'\1\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n',
    c, count=1
)
with open(conf, 'w') as f:
    f.write(c)
"

service nginx restart
exit 0
