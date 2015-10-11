# udacity Full Stack Web Developer Nanodegree Project 3 - Item Catalog

## Requirements

install necessary libraries:
```bash
pip install -r req.txt
```

* python
* [flask v0.10.1](http://flask.pocoo.org) 
* [sqlalchemy v2.0](http://www.sqlalchemy.org)
* [SeaSurf v0.2.1](https://flask-seasurf.readthedocs.org)
* [GitHub-Flask v3.0.1](https://github-flask.readthedocs.org/en/latest/)

##Setup
for GitHub OAuth the Client ID and Client Secret have to be changed in application.py: 

```python
app.config['GITHUB_CLIENT_ID'] = 'XXX'
app.config['GITHUB_CLIENT_SECRET'] = 'YYY'
```

for session managment you should change the secret key of the app:
```python
app_secret = 'ZZZ'
```

the callback url should be something like /github-callback
and can be configured in the head of application.py:


reset database:
```bash
rm catalog.db
python addData.py
```

##Usage
start application
```bash
python application.py
```

##JSON endpoints
[GET]
* /
* /catalog/
* /catalog/\<category_name\>/
* /item/\<item_id\>/
* /login
* /logout
* /github-callback

[POST]
* /catalog/\<category_name\>/add/
* /item/\<item_id\>/edit/
* /item/\<item_id\>/delete/

# Project 5 Configurateion

This part is for Project 5 - Configuring Linux Web Servers course.

## Steps
###Launch your Virtual Machine with your Udacity account and ollow the instructions provided to SSH into your server
Done under udacity page
###Create a new user named grader and grant this user sudo permissions.
```bash
[~#]useradd grader
[~#]visudo
```
Then add the following line under User privilege specification

```bash
grader  All=(ALL:ALL) ALL
```

###Update all currently installed packages.

```bash
[~#] apt-get update -y
[~#] apt-get upgrade -y
```

###Configure the local timezone to UTC.

```bash
ln -sf /usr/share/zoneinfo/UTC /etc/localtime
```

### Change the SSH port from 22 to 2200

```bash
nano /etc/ssh/sshd_config
```
change port 22 to port 2200, save and restart ssh and system
```bash
sudo /etc/init.d/ssh restart
sudo restart
```

Reconnect to system
```bash
ssh -p 2200 -i ~/.ssh/udacity_key.rsa root@52.10.102.51
```


### Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)
```bash
sudo ufw enable
sudo ufw allow 2200/tcp
sudo ufw allow 80/tcp
sudo ufw allow 123/udp
```

### Install and configure Apache to serve a Python mod_wsgi application
Install packages
```bash
sudo apt-get install apache2 -y
sudo apt-get install python-setuptools libapache2-mod-wsgi -y
```
Restart apache for mod_wsgi to load
```bash
sudo service apache2 restart
```

### Install git, clone and setup your Catalog App project
Install and configure git
```bash
sudo apt-get install git -y
git config --global user.name "YOUR NAME"
git config --global user.email "YOUR EMAIL ADDRESS"
```
### Deploy Flask Application
Install necessary packages
```bash
sudo apt-get install libapache2-mod-wsgi python-dev -y
sudo apt-get install python-pip -y
sudo pip install virtualenv Flask
```

Enable mod_wsgi

```bash
sudo a2enmod wsgi
```

Move Catalog to /var/www
```bash
cd /var/www
git clone YOUR_PROJECT_URL
```


Setup venv and install packages
```bash
virtualenv catalog_venv
source catalog_venv/bin/activate
pip install -r YOUR_PROJECT/requirement.txt
deactivate
```

Setup wsgi
```bash
sudo nano /var/www/catalog/catalog.wsgi
```

put the following in the file and save, change the secret key as u desire
```bash
 #!/usr/bin/python
  import sys
  import logging
  logging.basicConfig(stream=sys.stderr)
  sys.path.insert(0,"/var/www/catalog/")

  from catalog import app as application
  application.secret_key = 'SECRET'
```

create .htaccess
```bash
sudo nano /var/www/catalog/.htaccess
```
add the following in the file and save
```bash
RedirectMatch 404 /\.git
```

Configure virtual host
```bash
sudo nano /etc/apache2/sites-available/catalog.conf
```
Add the following and change the ip address
```bash
<VirtualHost *:80>
      ServerName PUBLIC-IP-ADDRESS
      ServerAdmin admin@PUBLIC-IP-ADDRESS
      WSGIScriptAlias / /var/www/catalog/catalog.wsgi
      <Directory /var/www/catalog/catalog/>
          Order allow,deny
          Allow from all
      </Directory>
      Alias /static /var/www/catalog/catalog/static
      <Directory /var/www/catalog/catalog/static/>
          Order allow,deny
          Allow from all
      </Directory>
      ErrorLog ${APACHE_LOG_DIR}/error.log
      LogLevel warn
      CustomLog ${APACHE_LOG_DIR}/access.log combined
  </VirtualHost>
```


Restart apache
```bash
service apache2 reload
```

Configure PostgreSQL
```bash
sudo apt-get install postgresql postgresql-contrib -y


```


Change the database engine in database_setup.py to postgresql, e.g.
```python
python engine = create_engine('postgresql://catalog:PASSWORD@localhost/catalog')
```
Create user
```bash
sudo adduser catalog
```
Change to default user postgres:
```bash
sudo su - postgre
```
Connect to the system
```bash
psql
```
Create user
```bash
CREATE USER catalog;
```
Setup database
```bash
ALTER USER catalog CREATEDB;
CREATE DATABASE catalog WITH OWNER catalog;
\c catalog
REVOKE ALL ON SCHEMA public FROM public;
GRANT ALL ON SCHEMA public TO catalog;
\q
```
Then exit
```bash
exit
```
Create database
```bash
python database_setup.py
```
** At this step I had problem installing psql and found solution online 
```bash
sudo apt-get install -y postgis postgresql-9.3-postgis-2.1
pip install psycopg2
```

### login
```bash
ssh -p 2200 -i ~/.ssh/udacity_key.rsa root@52.10.102.51
```