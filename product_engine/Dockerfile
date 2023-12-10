#
FROM python:3.10

WORKDIR /product_engine

COPY .  product_engine

RUN pip install --no-cache-dir --upgrade -r product_engine/requirements.txt

EXPOSE 30

CMD ["uvicorn", "product_engine.src.main:app", "--host", "0.0.0.0", "--port", "30"]