from fastapi import FastAPI, Response

from scoring.src.models.dto import AgreementDto

app = FastAPI(
    title='Scoring API',
    summary='Documentation of Fintech Credits API - Scoring',
    description='There will be some description of Fintech API',
    version='1.0.0'
)


@app.post('/score_agreement',
          summary='Make agreement scored')
async def score_agreement(_: AgreementDto):
    """
    Make agreement scored
    :param _: agreement to score
    :return: stub
    """
    return Response(
        status_code=200,
        media_type='text/plain',
        content='Stub'
    )
