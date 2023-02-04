FROM ubuntu
# RUN apt-get install nginx -y

RUN apt-get update
# ref: https://serverfault.com/a/992421
# TZ= found in /usr/share/zoneinfo Directory is Country, and then Region.
# For example, TZ=America/New_York
# RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN DEBIAN_FRONTEND=noninteractive TZ=America/Los_Angeles apt-get -y install tzdata

RUN apt-get install git -y
RUN apt-get install python3 -y && apt-get install python3-pip -y && apt-get install python3-venv -y
RUN apt-get install sqlite3 libsqlite3-dev -y
RUN apt-get install nano -y

RUN apt-get install nginx -y
RUN service nginx stop
#
RUN mkdir /app
WORKDIR /app
#
RUN git clone https://github.com/jcarter62/intranet.git .
#
COPY ./.env-docker /app/.env
# COPY ./requirements.txt /app
#
COPY /app/nginx.conf /etc/nginx/sites-enabled/default
RUN service nginx start
#
RUN python3 -m venv venv
RUN venv/bin/pip3 install -r ./requirements.txt

# ENTRYPOINT ["python3"]
# CMD ["manage.py", "runserver" ]

#ENTRYPOINT ["bash"]
#CMD [" "]


#RUN mkdir /app/authenticate
#RUN mkdir /app/emp
#RUN mkdir /app/employees
#RUN mkdir /app/home
#RUN mkdir /app/templates
#RUN mkdir /app/static
#
#COPY authenticate/* /app/authenticate
#COPY emp/* /app/emp
#COPY employees/* /app/employees
#COPY home/* /app/home
#COPY templates/* /app/templates
#COPY static/* /app/static
##
#RUN rm -rf /app/*/__pycache__
#RUN rm -rf /app/*/*.cpython*
##
#COPY *.py /app
#COPY start /app
#
#RUN dos2unix /app/.env
#RUN dos2unix /app/*.py
#RUN dos2unix /app/start
#RUN dos2unix /app/*/*
#
#RUN chmod +x /app/start
#
