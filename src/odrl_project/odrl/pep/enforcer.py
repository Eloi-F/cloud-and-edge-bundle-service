import datetime
from fastapi import HTTPException

from odrl.odrl_eval import ODRLEvaluator
from odrl.pep.transfer import transfer_to

evaluator = ODRLEvaluator("./policies")

POLICY_TO_SERVICE_MAP = {
    "urn:capacity:cap-3": "http://cap3-service:8000/api",
    "urn:capacity:cap-4": "http://cap4-service:8000/api",
    "urn:capacity:cap-6": "http://cap6-service:8000/api",
}


def extract_duty_info(duty: dict):
    action_to_perform = None
    parameters = {}
    for condition in duty["conditions"]:
        key = condition[0]
        value = condition[2]
        if "Action" in key:
            action_to_perform = value.split("/")[-1].split("#")[-1]
        elif "uid" not in key:
            param_name = key.split("/")[-1].split("#")[-1]
            parameters[param_name] = value
    return action_to_perform, parameters


def enforce_odrl_policy(metadata: dict):
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
            print(f"Action to do: {duty}")
            action, _ = extract_duty_info(duty)

            target_uid = duty.get("uid")

            if action == "nextPolicy":
                target_url = POLICY_TO_SERVICE_MAP.get(target_uid)
                print(f"Calling the URL {target_url}")

                if not target_url:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Service URL not found for capacity: {target_uid}",
                    )

                is_done = transfer_to(endpoint=target_url, data=metadata)

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
                        detail=f"Failed to execute nextPolicy for {target_uid}.",
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
