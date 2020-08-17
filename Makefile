.PHONY: build_shell
build_shell:
	docker build \
        --tag ansible-operator-shell \
        --file ./Dockerfile.dev \
        .

.PHONY: shell
shell:
	docker run -it \
	-w /home/app_user/app \
	-v ${PWD}:/home/app_user/app \
	-v ${PWD}:/home/app_user/app \
	-v /var/run/docker.sock:/var/run/docker.sock \
	--name ansible-operator-shell \
	--rm ansible-operator-shell

.PHONY: deploy
deploy: 
	operator-sdk build riskfuel/mig-operator:latest
	docker push riskfuel/mig-operator-test:latest

.PHONY: deploymig
deploymig:
	docker build -t riskfuel/mig-operator-test:$(shell cat version) -f ./build/Dockerfile.mig . && docker push riskfuel/mig-operator-test:$(shell cat version)
