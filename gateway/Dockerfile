#
FROM python:3.10

WORKDIR /gateway

COPY .  gateway

RUN pip install --no-cache-dir --upgrade -r gateway/requirements.txt

EXPOSE 60

CMD ["uvicorn", "gateway.src.main:app", "--host", "0.0.0.0", "--port", "60"]