from fastapi import FastAPI, Response

from utils.http_output import JsonBeautify
from scoring.src.models.dto import AgreementDto

app = FastAPI(
    title='Scoring API',
    summary='Documentation of Fintech Credits API - Scoring',
    description='There will be some description of Fintech API',
    version='1.0.0'
)


@app.post('/score_agreement',
          response_class=JsonBeautify,
          summary='Make agreement scored')
async def score_agreement(
        agreement_to_score: AgreementDto
):
    """
    Make agreement scored
    :param agreement_to_score: agreement to score
    :return: stub
    """
    return Response(
        status_code=200,
        media_type='text/plain',
        content='Stub'
    )
