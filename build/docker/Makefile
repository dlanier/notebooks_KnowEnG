CUR_DATE=`date +'%m_%d_%Y'`

all: build_docker_image login_to_dockerhub push_to_dockerhub

build_docker_image:
	docker build --no-cache -t knowengdev/notebooks_knoweng:$(CUR_DATE) .

login_to_dockerhub:
	docker login --username=$(username) --email=$(email)

push_to_dockerhub:
	docker push knowengdev/notebooks_knoweng:$(CURR_DATE)

build_base_hub:
	docker build --no-cache -f Dockerfile.base_image -t knowengdev/notebooks_knoweng:base_hub .
