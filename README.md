Healthsites is a framework for capturing, publishing and sharing critical
health and sanitation related data to help make these facilities more 
accessible and relevant to the communities they serve. Our framework does not 
limit our endeavours to these domains and in the future we plan to support 
additional domains where it is helpful in humanitarian work.


Tests status: [![Build Status](https://travis-ci.org/konektaz/healthsites.svg)](https://travis-ci.org/konektaz/healthsites)

Coverage status: [![Coverage Status](https://img.shields.io/coveralls/konektaz/healthsites.svg)](https://coveralls.io/r/konektaz/healthsites?branch=develop)

Development status: [![Stories in Ready](https://badge.waffle.io/konektaz/healthsites
.png?label=ready&title=Ready)](https://waffle.io/konektaz/healthsites)




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
python manage.py collectstatic --noinput --settings=core.settings.dev_timlinux
```


