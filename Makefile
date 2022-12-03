setup:
	docker-compose exec admin python manage.py makemigrations
	docker-compose exec admin python manage.py migrate
	docker-compose exec admin python manage.py compilemessages -l en -l ru	
	docker-compose exec admin python manage.py collectstatic --no-input

admin:
	docker-compose exec admin python manage.py createsuperuser

load_data:
	docker-compose exec admin python manage.py migrate_data

redis:
	docker-compose exec redis redis-cli