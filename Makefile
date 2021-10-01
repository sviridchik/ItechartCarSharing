run:
	docker-compose up
build:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml -f docker-compose.migration.yml build
start:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml -f docker-compose.migration.yml build && docker-compose -f docker-compose.yml -f docker-compose.prod.yml -f docker-compose.migration.yml up
test:
	docker-compose -f docker-compose.yml  -f docker-compose.test.yml build && docker-compose -f docker-compose.yml -f docker-compose.test.yml up --abort-on-container-exit
safe_start:
	docker-compose -f docker-compose.yml  -f docker-compose.test.yml -f  docker-compose.prod.yml build && docker-compose -f docker-compose.yml -f docker-compose.test.yml -f docker-compose.prod.yml up
try:
	echo "Hello world!"
