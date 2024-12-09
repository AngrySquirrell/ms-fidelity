FROM python:3.9-slim as backend-builder

WORKDIR /app

COPY ./src/ .
RUN pip install --no-cache-dir -r req

EXPOSE 5000

RUN chmod +x init.sh
CMD ["./init.sh"]