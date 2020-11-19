FROM python:3.7
COPY ./backend/environment/requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt
RUN pip install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html

COPY . /home/DVA_Project

ENV DBHOST=dva-pamplemousse.postgres.database.azure.com
ENV DBNAME=recipesdb
ENV DBUSER=pamplemousse@dva-pamplemousse
ENV DBPASS=#edc4rfV
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV FLASK_APP=/home/DVA_Project/backend/routes.py
ENV FLASK_RUN_HOST=0.0.0.0

# Frontend requirements
RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get install -y nodejs

WORKDIR /home/DVA_Project/web-app
RUN npm install && npm run build

CMD flask run
EXPOSE 5000