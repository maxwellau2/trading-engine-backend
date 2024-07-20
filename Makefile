install:
	pip install -r requirements.txt

test-pq:
	python test_db.py

run-dev:
	fastapi dev main.py

update-dependencies:
	pip freeze >> "requirements.txt"