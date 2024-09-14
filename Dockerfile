FROM ubuntu:23.04

RUN apt -y update

RUN apt-get install -y wget

# minicondaのインストール
# https://qiita.com/kuboko-jp/items/6388c186e16028d3e699
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3
RUN rm -r Miniconda3-latest-Linux-x86_64.sh
ENV PATH /opt/miniconda3/bin:$PATH

RUN conda create -n a001 python=3.9 -y
RUN conda init
RUN echo "conda activate a001" >> ~/.bashrc

RUN apt-get install -y git
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN echo "git clone https://github.com/romazomatoma/server_service ; cd server_service ; bash docker_run.sh"> run.sh

CMD ["bash", "run.sh"]