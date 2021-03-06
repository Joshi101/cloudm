.PHONY: init init-migration build run db-migrate test tox

init:  build run
	docker-compose exec web cloudm db upgrade
	docker-compose exec web cloudm init
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

db-migrate:
	docker-compose exec web cloudm db migrate

db-upgrade:
	docker-compose exec web cloudm db upgrade

test:
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e test

tox:
	docker-compose run -v $(PWD)/tests:/code/tests:ro web tox -e py37

lint:
	docker-compose run web tox -e lint
