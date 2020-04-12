BRANCH := $(shell git branch --quiet --no-color | grep '*' | sed -e 's/^\*\ //g')
HERE := $(shell pwd)
UNTRACKED := $(shell git status --short | grep -e '^[ ?]' | wc -l | sed -e 's/\ *//g')
UNTRACKED2 := $(shell git status --short | awk '{print substr($$0, 2, 2)}' | grep -e '\w\+' | wc -l | sed -e 's/\ *//g')
VENV := $(shell pipenv --venv)

.PHONY: format
format:
	pipenv run isort --virtual-env ${VENV} --recursive --apply ${HERE}
	pipenv run black ${HERE}


.PHONY: run
run: static
	pipenv run python src/manage.py runserver


.PHONY: runa
runa: static
	PYTHONPATH="${HERE}/src" pipenv run uvicorn project.asgi:application


.PHONY: static
static:
	pipenv run python src/manage.py collectstatic --noinput --clear -v0


.PHONY: migrations
migrations:
	pipenv run python src/manage.py makemigrations


.PHONY: migrate
migrate:
	pipenv run python src/manage.py migrate


.PHONY: su
su:
	pipenv run python src/manage.py createsuperuser


.PHONY: test
test:
	pipenv run \
		coverage run \
			src/manage.py test -v2 \
				apps \
				project \

	pipenv run coverage report
	pipenv run isort --virtual-env ${VENV} --recursive --check-only ${HERE}


.PHONY: report
report:
	pipenv run coverage html --directory=${HERE}/htmlcov --fail-under=0
	open "${HERE}/htmlcov/index.html"


.PHONY: deploy
deploy: format test clean
	@echo 'test branch...'
	test "${BRANCH}" = "master"
	@echo 'test untracked...'
	test "${UNTRACKED}" = "0"
	@echo 'test untracked 2...'
	test "${UNTRACKED2}" = "0"
	git commit --message "autodeploy" --edit
	git push origin master


.PHONY: install
install:
	pipenv install --dev


.PHONY: clean
clean:
	pipenv run coverage erase
	find . -type d -name "__pycache__" | xargs rm -rf
	rm -rf Pipfile.lock
	rm -rf ./.static/

