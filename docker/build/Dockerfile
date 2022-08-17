FROM photon

WORKDIR /home/

RUN tdnf update -y && \
	tdnf install -y python3 python3-pip

RUN python3.9 -m pip install --upgrade pip

RUN pip3 install requests beautifulsoup4 lxml tqdm alive-progress

#RUN apt-get clean && \
	#rm -rf /var/lib/apt/lists/*