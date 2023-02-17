# Project Image - Interview 
This is a Django project upload image.

## Prerequisites
Before you start, make sure you have the following installed:

> Python (version 3.8 or higher)

## Inastallation
1. Clone the repository:
```shell
git clone https://github.com/MatRos-sf/Image_dj.git
```
2. Install the requirements:
```shell
pip install -r requirements.txt
```
3. Create a `.env` file and add your secret key.
4. Migrate the database:
```shell
python manage.py migrate
```
4. If you want create default tier runsever and go to `/tier/first_run/`
5. Run the development server:
```shell
python manage.py runserver
```
You should now be able to access the development server at http://localhost:8000/.

## Deployment 
When you are ready to deploy the project, you will need to:

1. Set `DEBUG = False` in `settings.py`.
2. Add your production domain to the `ALLOWED_HOSTS` list in `settings.py`.
3. You will also need to configure your web server to serve media files.