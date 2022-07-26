# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: iostancu <iostancu@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/07/26 19:44:04 by iostancu          #+#    #+#              #
#    Updated: 2022/07/26 20:14:54 by iostancu         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

BLUE	=\033[0;35m
GREEN	=\033[0;36m
YELLOW	=\033[0;33m

CONTAINER = spider_container
COMPOSE	= ./docker/docker-compose.yml
COMP_CMD = docker-compose ps -a 

all:	up	exe

list:
	@echo "${BLUE}All containers:"
	@echo "------------------------------"
	@docker-compose -f $(COMPOSE) ps -a
	@echo "${GREEN}Not running:"
	@echo "------------------------------"
	@docker-compose -f $(COMPOSE) ps
	@echo "${YELLOW}Existing images:"
	@echo "----------------------------------------------"
	@docker-compose -f $(COMPOSE) images

up:
	docker-compose up -d

down:
	docker-compose down

exec:
	docker exec -it ${CONTAINER} bash

help:
	@echo "${BLUE}GENERAL COMMANDS:\033[2;37m"
	@echo "[make] builds main image, and run a container with compose and execute it with bash"
	@echo "[exec] execute container with bash"
	@echo "[list] shows images and all containers with compose"
	@echo "[down] stops containers and delete them and the images too"