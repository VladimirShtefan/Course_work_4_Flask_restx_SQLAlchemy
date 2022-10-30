FROM python:3.10-slim

ENV FLASK_ENV=production \
    FLASK_APP=run.py
WORKDIR /app

RUN apt-get update -y && apt-get install -y --no-install-recommends curl && apt-get autoclean && apt-get autoremove && \
    rm -rf var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY requirements.txt .
RUN python3 -m pip install --no-cache -r requirements.txt

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]