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
