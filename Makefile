run:
	docker-compose up
build:
	docker-compose -f docker-compose.yml  -f docker-compose.migration.yml -f docker-compose.prod.yml build && docker-compose -f docker-compose.yml -f docker-compose.migration.yml  -f docker-compose.prod.yml up
start:
	docker-compose -f docker-compose.yml -f docker-compose.migration.yml -f docker-compose.prod.yml build && docker-compose -f docker-compose.yml -f docker-compose.migration.yml -f docker-compose.prod.yml up
test:
	docker-compose -f docker-compose.yml  -f docker-compose.test.yml build && docker-compose -f docker-compose.yml -f docker-compose.test.yml up --abort-on-container-exit
safe_start:
	docker-compose -f docker-compose.yml  -f docker-compose.test.yml -f  docker-compose.migration.yml build && docker-compose -f docker-compose.yml -f docker-compose.test.yml -f docker-compose.migration.yml up
try:
	echo "Hello world!"
start_no_migrations:
	docker-compose -f docker-compose.yml -f docker-compose.prodnomigration.yml build && docker-compose -f docker-compose.yml -f docker-compose.prodnomigration.yml up
