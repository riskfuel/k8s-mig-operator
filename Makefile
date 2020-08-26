.PHONY: shell
shell:
	docker-compose run shell

.PHONY: build
build:
	docker-compose build shell

.PHONY: test
test:
	@echo "==> Running Main Tests\n"
	docker-compose run test

.PHONY: deploy
deploy:
	docker build -t riskfuel/mig-operator:latest . && docker push riskfuel/mig-operator:latest
