#
FROM python:3.10

WORKDIR /origination

COPY .  origination

RUN pip install --no-cache-dir --upgrade -r origination/requirements.txt

EXPOSE $ORIGINATION_PORT

CMD ["uvicorn", "origination.src.main:app", "--host", "0.0.0.0", "--port", "40"]