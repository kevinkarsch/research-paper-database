# research-paper-database

This repo contains a template for hosting your own research paper collection, centered around bibtex. You can add bibtex entries and links, and search them from a simple web dashboard. Here's an example of [my database running live](https://paperdb.kevinkarsch.com).

### Setup and local testing

Make sure you have python3 and pip(3) installed. Feel free to run this in a virtualenv.

Install dependencies and initialize the database:

```
pip3 install -r requirements.txt
cd paperserver
python3 manage.py makemigrations papers
python3 manage.py migrate
```

Create an admin user for adding/removing/editing the paper database:

```
python3 manage.py createsuperuser
```

Run the server locally:

```
python3 manage.py runserver
```

Open up a browser to [127.0.0.1:8000](http://127.0.0.1:8000) to test.


### Deployment

The instructions below outline how to host this app on a free Google Cloud Compute Engine instance, which has worked well for my use case.

Create a Compute Engine instance on Google Cloud Platform. At the time of writing, f1-micro instances in us-west (Oregon-1) are free.

I used an Ubuntu 18.04 instance, but probably any Linux-based one will do. Make sure you allow http/https traffic during instance creation.

Log into your instance and run the following to grab dependencies:
```
sudo apt update
sudo apt -y install git python3-dev python3-pip
sudo pip3 install virtualenv
```

Clone this repo:
```
git clone https://github.com/kevinkarsch/research-paper-database.git
cd research-paper-database
```

Install requirements in a virtual environment:
```
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
```

Initialize the database:
```
python3 paperserver/manage.py makemigrations papers
python3 paperserver/manage.py migrate
```

Create an admin user:
```
python3 paperserver/manage.py createsuperuser
```

You can now back out of the virtualenv:
```
deactivate
```

[Optional] At this point, you can test the server by running the app with gunicorn (note that this requires opening port 8000, which isn't done by default).
```
cd paperserver
../env/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 admin.wsgi:application
```

Install nginx and create a few scripts to run the web service. First, see `deploy.sh` and modify `SERVER_NAME_OR_IP` as appropriate:
```
sudo apt -y install nginx
sudo ./deploy.sh
```

Your app should now be live at the IP/hostname provided in `deploy.sh`.

If you want to add HTTPS, I recommend using Certbot and Let's Encrypt. [This is a great article on using both](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04).
