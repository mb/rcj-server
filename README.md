# RCJ Server

## Setup

This project currently runs on [PythonAnywhere](https://pythonanywhere.com)

Test setup using apache2 on debian/ubuntu:

```bash
sudo apt install apache2 libapache2-mod-wsgi-py3
sudo a2enmod wsgi 
```

``/etc/apache2/envvars``:

```
export APACHE_RUN_USER=rcj
export APACHE_RUN_GROUP=rcj
```

``/etc/apache2/sites-available/000-default.conf``:

```
<VirtualHost *:80>
        WSGIScriptAlias / /home/rcj/rcj-server/rcj_pythonanywhere_com_wsgi.py

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        <Directory /home/rcj/rcj-server/>
                Require all granted
        </Directory>
</VirtualHost>
```

```
sudo adduser rcj
sudo passwd -d rcj
sudo -iu rcj
git clone https://github.com/mb/rcj-server
```

```bash
sudo systemctl restart apache2
```

