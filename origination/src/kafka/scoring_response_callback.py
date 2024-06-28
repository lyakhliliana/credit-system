import json

from common.status import AgreementStatus
from origination.src.models.dto import AgreementDto
from origination.src.models.session_maker import get_session
from origination.src.utils.change_agreement_status import change_agreement_status


async def scoring_response_callback(msg):
    result = AgreementDto(**json.loads(msg.value.decode('ascii')))
    async for session in get_session():
        if result.status == AgreementStatus.APPROVED.value:
            await change_agreement_status(agreement_id=result.agreement_id, new_status=AgreementStatus.APPROVED.value,
                                          session=session)
        else:
            await change_agreement_status(agreement_id=result.agreement_id, new_status=AgreementStatus.REJECTED.value,
                                          session=session)
