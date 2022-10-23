FROM python:3.8-slim

WORKDIR /bot
RUN apt update
RUN apt -y install libcups2-dev python3-dev gcc

COPY Pipfile .
RUN pip install pipenv && \
    pip install pipfile-requirements
RUN pipfile2req Pipfile > requirements.txt
RUN pip install -r requirements.txt

COPY bot.py *.json *.pickle /bot/
COPY config config
COPY modules modules

VOLUME /bot/config
RUN useradd -m HomeBot && chown HomeBot -R /bot && apt install curl jq -y
USER HomeBot
WORKDIR /bot

CMD [ "python", "-u", "./bot.py" ]
