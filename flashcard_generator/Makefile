all: install 

install:
	brew install redis
	export CMAKE_ARGS="-DLLAMA_METAL=on" && \
	export FORCE_CMAKE=1 && \
	poetry update

start-redis:
	brew services start redis
start-celery:
	poetry run celery -A app.celery worker -P solo --loglevel=info