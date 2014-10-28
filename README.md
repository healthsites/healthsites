[![Stories in Ready](https://badge.waffle.io/konekta/healthsites.png?label=ready&title=Ready)](https://waffle.io/konekta/healthsites)

# Setup instructions

```
virtualenv venv
source venv/bin/activate
pip install -r REQUIREMENTS-dev.txt
nodeenv -p --node=0.10.31
npm -g install yuglify
```

# Running collect static

```
virtualenv venv
source venv/bin/activate
cd django_project
python manage.py collectstatic --settings=core.settings.dev_timlinux
```


