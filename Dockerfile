FROM ubuntu

RUN apt-get update
# ref: https://serverfault.com/a/992421
# TZ= found in /usr/share/zoneinfo Directory is Country, and then Region.
# For example, TZ=America/New_York
# RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN DEBIAN_FRONTEND=noninteractive TZ=America/Los_Angeles apt-get -y install tzdata

RUN apt-get install git -y
RUN apt-get install python3.10 -y && apt-get install python3-pip -y && apt-get install python3-venv -y
RUN apt-get install sqlite3 libsqlite3-dev -y
RUN apt-get install nano -y
#
RUN mkdir /app
WORKDIR /app
#
RUN apt-get install nginx -y
RUN service nginx stop
#
RUN git clone https://github.com/jcarter62/intranet.git .
#
COPY .env /app/.env
RUN mkdir /app/logs
#
COPY nginx.conf /etc/nginx/sites-enabled/default
#
RUN python3 -m venv venv
RUN venv/bin/pip3 install -r ./requirements.txt
RUN mv start start.sh
RUN chmod +x start.sh

CMD ["bash", "start.sh"]
