FROM python:3.7

# Frontend requirements
RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get install -y nodejs

COPY ./environment/requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt
RUN pip install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html

ENV DBHOST=dva-pamplemousse.postgres.database.azure.com
ENV DBNAME=recipesdb
ENV DBUSER=recipeapp@dva-pamplemousse
ENV DBPASS=findther3c1pes
ENV FLASK_APP=/home/app/backend/routes.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY . /home/app
WORKDIR /home/app/web-app
RUN npm install && npm run build

CMD flask run -p 80
EXPOSE 80