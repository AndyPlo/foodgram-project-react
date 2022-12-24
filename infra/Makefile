setup:
	sudo docker-compose exec backend python manage.py migrate
	sudo docker-compose exec backend python manage.py collectstatic --no-input
	sudo docker cp fixtures.json andy_plo_backend_1:/app
	sudo docker cp recipes/ andy_plo_backend_1:/app/media/
	sudo docker-compose exec backend python manage.py loaddata fixtures.json