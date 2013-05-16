
#create the virtual environment if not exists...
[ -d "/var/apps/djangoapp/venv/bin/" ] ||
	virtualenv /var/apps/djangoapp/venv/

#add the /app/repo folder to virtual environment's PYTHONPATH if not added
[ -e "/var/apps/djangoapp/venv/lib/python2.6/site-packages/repo.pth" ] ||
	echo "/app/repo/" >> "/var/apps/djangoapp/venv/lib/python2.6/site-packages/repo.pth"

#activate the virtual environement
source /var/apps/djangoapp/venv/bin/activate

#make sure to install the proper requirements files into the venv.
if [ -f "/app/repo/requirements.txt" ]
then
	pip install -r /app/repo/requirements.txt
else
	pip install -r /app/quick_start/templates/project_template/requirements.txt
fi

#append the following lines to .profile for expected login behavior
#makes sure to activate venv on login.
grep -q "source /var/apps/djangoapp/venv/bin/activate" /home/vagrant/.profile || 
echo "source /var/apps/djangoapp/venv/bin/activate" >> /home/vagrant/.profile

#make sure to login to /app folder.
grep -q "cd /app" /home/vagrant/.profile || 
echo "cd /app" >> /home/vagrant/.profile
