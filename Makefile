HERE := $(shell pwd)
VENV := $(shell pipenv --venv)
SRC := ${HERE}/src
PYTHONPATH := ${SRC}
TEST_PARAMS := --verbosity 2 --pythonpath "${PYTHONPATH}"
PSQL_PARAMS := --host=localhost --username=alex --password


MANAGE := python src/manage.py


.PHONY: format
format:
	isort --virtual-env="${VENV}" "${HERE}"
	black "${HERE}"


.PHONY: run
run: static
	${MANAGE} runserver 127.0.0.1:8000


.PHONY: beat
beat:
	PYTHONPATH="${PYTHONPATH}" \
	celery \
		--app periodic.app worker \
		--config periodic.celeryconfig \
		--workdir "${SRC}" \
		worker \
		--beat \
		--loglevel=debug


.PHONY: static
static:
	${MANAGE} collectstatic --noinput --clear -v0


.PHONY: migrations
migrations:
	${MANAGE} makemigrations


.PHONY: migrate
migrate:
	${MANAGE} migrate


.PHONY: su
su:
	${MANAGE} createsuperuser


.PHONY: sh
sh:
	${MANAGE} shell


.PHONY: test
test:
	coverage run \
		src/manage.py test ${TEST_PARAMS} \
			applications \
			periodic \
			project \

	coverage report
	isort --virtual-env="${VENV}" --check-only "${HERE}"
	black --check "${HERE}"


.PHONY: report
report:
	coverage html --directory="${HERE}/htmlcov" --fail-under=0
	open "${HERE}/htmlcov/index.html"


.PHONY: clean
clean:
	coverage erase
	rm -rf htmlcov
	find . -type d -name "__pycache__" | xargs rm -rf
	rm -rf ./.static/


.PHONY: resetdb
resetdb:
	psql ${PSQL_PARAMS} \
		--dbname=postgres \
		--echo-all \
		--file="${HERE}/ddl/reset_db.sql" \
		--no-psqlrc \
		--no-readline \


.PHONY: initdb
initdb: resetdb migrate
