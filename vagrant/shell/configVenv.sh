
#create the virtual environment if not exists...
[ -d "/var/apps/djangoapp/venv/bin/" ] ||
	virtualenv /var/apps/djangoapp/venv/

#add the /app/repo folder to virtual environment's PYTHONPATH if not added
[ -e "/var/apps/djangoapp/venv/lib/python2.6/site-packages/repo.pth" ] ||
	echo "/app/repo/" >> "/var/apps/djangoapp/venv/lib/python2.6/site-packages/repo.pth"

#activate the virtual environement, and install Django and Fabric...
source /var/apps/djangoapp/venv/bin/activate
sudo pip install -Ivq Django==1.6.1
sudo pip install -Ivq Fabric==1.8.0

#append the following lines to .profile for expected login behavior
#makes sure to activate venv on login.
grep -q "source /var/apps/djangoapp/venv/bin/activate" /home/vagrant/.profile || 
echo "source /var/apps/djangoapp/venv/bin/activate" >> /home/vagrant/.profile

#make sure to login to /app folder.
grep -q "cd /app" /home/vagrant/.profile || 
echo "cd /app" >> /home/vagrant/.profile
