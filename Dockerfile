FROM python:slim-buster

WORKDIR /app

COPY . .

RUN pip install --user -r requirements.txt

CMD [ "python", "bot.py" ]
