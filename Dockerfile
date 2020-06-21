
FROM python:3.7.5-slim
#FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev
RUN pip install pip
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install flask_sqlalchemy
RUN pip install flask_bcrypt
RUN pip install flask_login
RUN pip install flask_wtf
RUN pip install flask_login
RUN pip install wtforms
RUN pip install email_validator
RUN pip install datetime
RUN pip install numpy
RUN pip install pandas
#RUN pip3 install shutil
RUN pip install pillow
#RUN pip install functools
COPY . /app
WORKDIR /app
#EXPOSE 5000 
#ENTRYPOINT [ "python" ] 
CMD ["python", "run.py" ] 
