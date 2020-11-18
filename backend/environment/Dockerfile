FROM python:3.7
COPY ./backend/environment/requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt
RUN pip install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html

COPY . /home/

ENV DBHOST=dva-pamplemousse.postgres.database.azure.com
ENV DBNAME=recipesdb
ENV DBUSER=pamplemousse@dva-pamplemousse 
ENV DBPASS=#edc4rfV
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

ENTRYPOINT [ "python", "home/backend/routes.py"]

EXPOSE 80