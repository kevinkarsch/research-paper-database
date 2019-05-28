#! /bin/bash

# mostly follows https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

SERVER_NAME_OR_IP="paperdb.kevinkarsch.com" # Change this to your IP or server name
SERVER_NAME_WWW="www.paperdb.kevinkarsch.com" # Optional (remove/leave blank if not available)

VIRTUALENV_DIR=${THIS_DIR}/env #This is the path from the README, update this if you changed it

PROJECT_ROOT=${THIS_DIR}/paperserver #This should NOT be changed

# Require sudo
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

echo "Writing server configuration files..."
cat <<EOM >/etc/systemd/system/gunicorn.socket
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOM

cat <<EOM >/etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=${PROJECT_ROOT}
ExecStart=${VIRTUALENV_DIR}/bin/gunicorn \
 --access-logfile - \
 --workers 3 \
 --bind unix:/run/gunicorn.sock \
 admin.wsgi:application

[Install]
WantedBy=multi-user.target
EOM

cat <<EOM >/etc/nginx/sites-available/${SERVER_NAME_OR_IP}
server {
    listen 80;
    listen [::]:80;

    server_name ${SERVER_NAME_OR_IP} ${SERVER_NAME_WWW};

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /static/ {
        root ${PROJECT_ROOT};
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOM

echo "Enabling systemd services..."
systemctl start gunicorn.socket
systemctl enable gunicorn.socket

echo "Preparing nginx..."
ln -s /etc/nginx/sites-available/${SERVER_NAME_OR_IP} /etc/nginx/sites-enabled/${SERVER_NAME_OR_IP}
service nginx restart
ufw allow 'Nginx Full' #Open up ports

echo "Done! Go to http://${SERVER_NAME_OR_IP} to see the site."
