FROM photon

WORKDIR /home/

RUN tdnf update -y && \
	tdnf install -y python3 python3-pip

RUN pip3 install requests beautifulsoup4

#RUN apt-get clean && \
	#rm -rf /var/lib/apt/lists/*