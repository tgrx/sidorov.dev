test:
	pipenv run python src/manage.py test -v1 project


init:
	pip install pipenv --upgrade
	pipenv install --dev
