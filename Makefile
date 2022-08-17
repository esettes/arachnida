# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: iostancu <iostancu@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/07/26 19:44:04 by iostancu          #+#    #+#              #
#    Updated: 2022/08/17 19:53:32 by iostancu         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

CYAN	=\033[1;36m
RED		=\033[0;31m
LILA 	=\033[0;35m
BLUE	=\033[1;34m
GREEN	=\033[2;32m
YELLOW	=\033[1;33m
END		=\033[1;37m

DOCKER_PATH = ./docker/build/Dockerfile

OS	:=	$(shell uname -s) 

APPNAME = arachnida:latest
CONTAINER = spider_container

all:	header up exec
	
info: header

define HEADER
			
                 ║
        ▄█▀▄     ║      ▄▀▄▄
       ▀    ▀▄   ║    ▄▀    ▀
       ▄▄▄    █▄▄▄▄▄▄█    ▄▄▄
     ▄▀   ▀█ █▀  ▐▌  ▀█ █▀   ▀▄
            ██  ▀▐▌▀  ██
       ▄█▀▀▀████████████▀▀▀▄▄
      █      ██████████      █
      █    █▀  ▀▀▀▀▀▀  ▀█    █
       ▀   █            █   ▀
             ▀        ▀
			 
endef
export HEADER

header:
	clear
	@echo "$(RED)$$HEADER$(END)"

ifeq  ($(OS),Darwin)
COMP_CMD = docker-compose
COMPOSE = ./docker/docker-compose.yml
else
COMP_CMD = docker compose
COMPOSE = ./docker/docker-compose.yml
endif

list:
	@echo "${BLUE}> Compose running containers: --------------------------"
	@$(COMP_CMD) -f $(COMPOSE) ps -a
	@echo "${LILA}> Running containers: \t--------------------------------${END}"
	@docker ps -a
	@echo "${LILA}> Existing docker images: ------------------------------${END}"
	@docker images 
	
up:
	@$(COMP_CMD) -f $(COMPOSE) up -d

build:
	@docker build -f $(DOCKER_PATH) . -t $(APPNAME)

down:
	@echo "$(RED) If image is not deleted. Run [ make del ]"
	@${COMP_CMD} -f $(COMPOSE) down

delete: down
	docker rm -fv $(CONTAINER)
	docker rmi -f $(DOCKER_PATH) $(APPNAME)
	
#Check why delete cause error 
del:
	docker rmi -f $(DOCKER_PATH) $(APPNAME)

exec:
	@docker exec -it $(CONTAINER) /bin/sh -c bash

help:
	@echo ""
	@echo "${BLUE}GENERAL COMMANDS:\033[2;37m"
	@echo "\t[ list ] \tShows images and all containers with compose."
	@echo "\t[ make ] \tExecutes 'up' and 'exec'."
	@echo "\t[ up ] \t\tBuilds images and run containers."
	@echo "\t[ exec ] \tExecutes container with bash."
	@echo "\t[ delete ] \tStop and delete containers and images."
	@echo "\t[ build ] \tBuild the image."
	@echo ""
	@echo "\tA normal workflow would be: [ make build ] + [ make ] "
	@echo ""
	@echo "\tThen you can [ make list ] to se all existing images and containers and"
	@echo "\tto delete the images and containers related, execute [ make delete ] "
