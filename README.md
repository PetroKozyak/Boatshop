# Boatshop
```bash
pip install virtualenv
virtualenv -p /usr/bin/python3.5 venv
source venv/bin/activate
cd boatshop
cp local_settings_example.py local_settings.py
```


```bash
cd ../
pip install -r requirements.txt
./manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin@example.com', 'admin@example.com', 'adminadmin')" | python manage.py shell
./manage.py runserver
POSTMAN: https://documenter.getpostman.com/view/9378010/SW15xbfv?version=latest
```