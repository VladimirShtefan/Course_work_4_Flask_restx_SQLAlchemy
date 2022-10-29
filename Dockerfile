FROM python:3.10-slim

WORKDIR /app

RUN apt-get update -y && apt-get install -y --no-install-recommends curl && apt-get autoclean && apt-get autoremove && \
    rm -rf var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY requirements.txt .
RUN python3 -m pip install --no-cache -r requirements.txt

COPY . .

ENV FLASK_ENV=production \
    FLASK_APP=run.py

ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
CMD ["docker", "run", "-p", "80:80", "painassasin/node_cource_project"]