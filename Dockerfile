FROM continuumio/miniconda3:24.7.1-0

RUN apt -y update

RUN conda create -n a001 python=3.9 -y
RUN conda init
RUN echo "conda activate a001" >> ~/.bashrc

RUN apt-get install -y git
RUN echo "rm -rf server_service ; git clone https://github.com/romazomatoma/server_service ; cd server_service ; bash docker_run.sh"> run.sh

CMD ["bash", "run.sh"]