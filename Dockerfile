FROM python:3.10-slim

RUN apt update && apt install nginx -y

COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

WORKDIR /Taskify

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x run.sh

CMD ["./run.sh"]
