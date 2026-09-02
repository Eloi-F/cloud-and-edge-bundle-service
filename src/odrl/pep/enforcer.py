import datetime
from fastapi import HTTPException

from pydantic import BaseModel
from src.odrl.pep.transfer import delegate_to
from src.odrl.odrl_eval import ODRLEvaluator

import logging
from src.logging_config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


POLICY_TO_SERVICE_MAP = {
    "urn:capacity:identification":      "http://localhost:8000/identification",
    "urn:capacity:navigation":          "http://localhost:8001/trajectory_planning",
    "urn:capacity:decision":            "http://localhost:8002/decision",
    "urn:capacity:image-compression":   "http://localhost:8003/resize",
    "urn:capacity:storage":             "http://localhost:8004/storage",
}


def extract_duty_info(duty: dict):
    action_to_perform = None
    for condition in duty["conditions"]:
        if "Action" in condition[0]:
            action_to_perform = condition[2].split("/")[-1].split("#")[-1]
            break
    return action_to_perform


def verify_permissions(evaluator: ODRLEvaluator, bundle_id: str, metadata: dict):
    """
    Check if the action is allowed before executing business logic.
    """
    if not metadata:
        raise HTTPException(status_code=400, detail="Missing ODRL metadata.")

    history = [metadata]
    result = evaluator.evaluate(bundle_id, history)

    if not result["is_valid"]:
        raise HTTPException(
            status_code=401, detail=f"Access denied. Violations: {result['violations']}"
        )

    return history, result["missing_duties"]


def enforce_duties(
    evaluator: ODRLEvaluator,
    bundle_id: str,
    history: list,
    duties: list,
    payload: BaseModel,
):
    """
    Execute duties.
    """
    if not duties:
        logger.debug("No coming duties.")
        return {}

    delegation_responses = {}

    for duty in duties:
        action = extract_duty_info(duty)
        target_uid = duty.get("uid")

        if action == "nextPolicy":
            target_url = POLICY_TO_SERVICE_MAP.get(target_uid)

            if not target_url:
                raise HTTPException(
                    status_code=500, detail=f"URL not found for: {target_uid}"
                )
            logger.debug(f"Performing Nextpolicy towards {target_url}")

            response_data = delegate_to(endpoint=target_url, data=payload)
            delegation_responses[target_uid] = response_data
            is_done = True if response_data is not None else False

            if is_done:
                history.append(
                    {
                        "http://www.w3.org/ns/odrl/2/dateTime": datetime.datetime.now().isoformat(),
                        "http://www.w3.org/ns/odrl/2/Action": "http://www.w3.org/ns/odrl/2/nextPolicy",
                        "http://www.w3.org/ns/odrl/2/uid": target_uid,
                    }
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed nextPolicy execution for {target_uid}",
                )
        else:
            raise HTTPException(status_code=501, detail=f"Unsupported Duty: {action}")
    logger.debug("All duties done.")
    final_result = evaluator.evaluate(bundle_id, history)
    if not final_result["is_valid"] or final_result["missing_duties"]:
        raise HTTPException(
            status_code=401, detail="Duties validation failed after execution."
        )

    return delegation_responses
