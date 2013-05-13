virtualenv /var/apps/djangoapp/venv/
source /var/apps/djangoapp/venv/bin/activate

if [ -f "/app/repo/requirements.txt" ]
then
	pip install -r /app/repo/requirements.txt
else
	pip install -r /app/quick_start/templates/project_template/requirements.txt
fi

#make sure to activate venv on login.
grep -q "source /var/apps/djangoapp/venv/bin/activate" /home/vagrant/.profile || 
echo "source /var/apps/djangoapp/venv/bin/activate" >> /home/vagrant/.profile

#make sure to login to /app folder.
grep -q "cd /app" /home/vagrant/.profile || 
echo "cd /app" >> /home/vagrant/.profile
