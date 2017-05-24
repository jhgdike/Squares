WITH_ENV = env `cat .env 2>/dev/null | xargs`
WITH_TEST_ENV = env `cat .env tests/.env 2>/dev/null | xargs`

COMMANDS = help clean install-deps unittest lint initdb
.PHONY: $(COMMANDS)

help:
	@echo "commands: $(COMMANDS)"

clean:
	@find `pwd` \( -name '*.pyc' -o -name '*.ptlc' \) -type f -delete
	@find . -name '__pycache__' -type d -delete
	@find . -type d -empty -delete
	@rm -rf build dist htmlcov *.egg-info

server:
	@$(WITH_ENV) python manage.py runserver

install-deps:
	@[ -n "$(VIRTUAL_ENV)" ] || (echo 'out of virtualenv'; exit 1)
	@pip install -r requirements.txt

test: unittest apitest behavetest

unittest:
	@$(WITH_TEST_ENV) py.test --cov=ganymede.models --cov=ganymede.utils.counter --capture=no --exitfirst tests/$(name)

apitest:
	@$(WITH_TEST_ENV) py.test --capture=no --exitfirst --cov=ganymede.views.api.book apitests/$(name)

behavetest:
	@$(WITH_TEST_ENV) py.test --cov=ganymede.views.api.book behaves/$(name) --capture=no --exitfirst --cov-config=.coveragerc_behavetest

fillup:
	@$(WITH_ENV) python -W ignore -m tests.init.add_user
	@$(WITH_ENV) python -W ignore -m tests.init.add_basic_data

lint:
	@$(WITH_ENV) flake8

initdb:
	@$(WITH_TEST_ENV) python -W ignore -m tests.init.add_basic_data
	@$(WITH_TEST_ENV) python -W ignore tests/init/alter_table_engine_to_memory.py

shell:
	@$(WITH_ENV) python manage.py shell

upgrade:
	@$(WITH_ENV) python manage.py db upgrade

downgrade:
	@$(WITH_ENV) python manage.py db downgrade

migrate:
	@$(WITH_ENV) python manage.py db migrate
