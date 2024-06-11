#
FROM python:3.10

WORKDIR /scoring

COPY .  scoring

RUN pip install --no-cache-dir --upgrade -r scoring/requirements.txt

EXPOSE $SCORING_PORT

CMD ["uvicorn", "scoring.src.main:app", "--host", "0.0.0.0", "--port", "8150"]