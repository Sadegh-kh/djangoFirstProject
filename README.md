# djangoFirstProject

## project setup

1- SetUp venv
```
virtualenv -p python3.10 venv
or
python -m venv .venv
then
source .venv/bin/activate (in linux)
.venv/Scripts/activate (in windows)


```

2- install Dependencies
```
pip install -r requirements.txt
```


3- Create tables
```
python manage.py migrate
```

4- run the project
```
python manage.py runserver
```
