import datetime
from fastapi import HTTPException

from odrl.odrl_eval import ODRLEvaluator
from odrl.pep.transfer import transfer_to

evaluator = ODRLEvaluator("./policies")

POLICY_TO_SERVICE_MAP = {
    "urn:policy:coordination:cap3-cloud": "http://aggregator-service:8000/aggregate",
}


def extract_duty_info(duty: dict):
    """Parse Duty information from the JSON structure."""
    action_to_perform = None
    parameters = {}
    for condition in duty["conditions"]:
        key = condition[0]
        value = condition[2]
        if "Action" in key:
            action_to_perform = value.split("/")[-1].split("#")[-1]
        else:
            param_name = key.split("/")[-1].split("#")[-1]
            parameters[param_name] = value
    return action_to_perform, parameters


def enforce_odrl_policy(metadata: dict):
    """
    Core PEP function. Evaluates policy, enforces duties, and re-verifies.
    Raises HTTPException if access is denied.
    """
    if not metadata:
        raise HTTPException(status_code=400, detail="Missing ODRL metadata in request.")

    history = [metadata]
    result = evaluator.evaluate(history)

    if not result["is_valid"]:
        raise HTTPException(
            status_code=401, detail=f"Access denied. Violations: {result['violations']}"
        )

    if result["missing_duties"]:
        for duty in result["missing_duties"]:
            action, params = extract_duty_info(duty)

            if action == "nextPolicy":
                target_urn = params.get("target", "")
                target_url = POLICY_TO_SERVICE_MAP.get(target_urn)

                if not target_url:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Service URL not found for policy: {target_urn}",
                    )

                is_done = transfer_to(endpoint=target_url, data=metadata)

                if is_done:
                    duty_log = {
                        "http://www.w3.org/ns/odrl/2/dateTime": datetime.datetime.now().isoformat(),
                        "http://www.w3.org/ns/odrl/2/Action": "http://www.w3.org/ns/odrl/2/nextPolicy",
                        "http://www.w3.org/ns/odrl/2/target": target_urn,
                    }
                    history.append(duty_log)
                else:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to execute the required nextPolicy Duty.",
                    )

            else:
                raise HTTPException(
                    status_code=501, detail=f"Unsupported Duty: {action}"
                )

        final_result = evaluator.evaluate(history)
        if not final_result["is_valid"] or final_result["missing_duties"]:
            raise HTTPException(
                status_code=401,
                detail="Conditions were not validated after duty execution.",
            )

    return True
