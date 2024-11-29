clean:
	rm -rf *.egg-info .pytest_cache
	rm -rf htmlcov
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

coverage:
	pytest --cov=django_ip_access tests

report:
	pytest --cov=django_ip_access --cov-report=html tests

install:
	pip install -r test_requirements.txt
	pre-commit install

release:
	git tag -a $(shell python -c "from django_ip_access import __version__; print(__version__)") -m "$(m)"
	git push origin --tags

release_test:
	- rm -rf build && rm -rf dist && rm -rf *.egg-info
	- python setup.py sdist bdist_wheel
	- python -m twine upload --repository testpypi dist/*

release_prod:
	- rm -rf build && rm -rf dist && rm -rf *.egg-info
	- python setup.py sdist bdist_wheel
	- python -m twine upload dist/*

bandit:
	bandit -c pyproject.toml -r .
