all: launch-card-generator

install-cg-env:
	brew install redis
	export CMAKE_ARGS="-DLLAMA_METAL=on" && \
	export FORCE_CMAKE=1 && \
	poetry install

start-redis:
	brew services start redis

start-celery:
	poetry run celery -A app.celery worker -P solo --loglevel=info

launch-card-generator-app:
	poetry run python flashcard_generator/app.py

launch-card-generator: install-cg-env start-redis start-celery launch-card-generator-app