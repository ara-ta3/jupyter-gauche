FROM tarata/jupyter-gauche:origin

RUN mkdir /notebooks
ENV PATH /usr/local/python/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENTRYPOINT jupyter notebook --NotebookApp.port=8888 '--NotebookApp.ip=*' --NotebookApp.notebook_dir=/notebooks
EXPOSE 8888
