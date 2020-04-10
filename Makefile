BRANCH := $(shell git branch --quiet --no-color | grep '*' | sed -e 's/^\*\ //g')
HERE := $(shell pwd)
UNTRACKED := $(shell git status --short | grep -e '^[ ?]' | wc -l | sed -e 's/\ *//g')
UNTRACKED2 := $(shell git status --short | awk '{print substr($$0, 2, 2)}' | grep -e '\w\+' | wc -l | sed -e 's/\ *//g')
VENV := $(shell pipenv --venv)

.PHONY: format run runa static test deploy install clean


format:
	pipenv run isort --virtual-env ${VENV} --recursive --apply ${HERE}
	pipenv run black ${HERE}


run: static
	DJANGO_DEBUG=TRUE pipenv run python src/manage.py runserver


runa: static
	PYTHONPATH="${HERE}/src" pipenv run uvicorn project.asgi:application


static:
	DJANGO_DEBUG=TRUE pipenv run python src/manage.py collectstatic --noinput --clear -v0


test:
	DJANGO_DEBUG=TRUE \
	pipenv run \
		coverage run \
			src/manage.py test -v2 \
				apps \
				project \

	pipenv run coverage report
	pipenv run isort --virtual-env ${VENV} --recursive --check-only ${HERE}


deploy: format test clean
	@echo 'test branch...'
	test "${BRANCH}" = "master"
	@echo 'test untracked...'
	test "${UNTRACKED}" = "0"
	@echo 'test untracked 2...'
	test "${UNTRACKED2}" = "0"
	git commit --message "autodeploy" --edit
	git push origin master


install:
	pipenv update --dev


clean:
	pipenv run coverage erase
	find . -type d -name "__pycache__" | xargs rm -rf
	rm -rf Pipfile.lock
	rm -rf ./.static/

