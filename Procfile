% prepara el repositorio para su despliegue.
release: sh -c 'cd youroom && python manage.py migrate'
% especifica el comando para lanzar Youroom
web: sh -c 'cd youroom && gunicorn youroom.wsgi --log-file -'