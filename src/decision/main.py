import uvicorn
import os
import datetime

from fastapi import FastAPI, HTTPException
from app.api.schemas import DecisionRequest, DecisionResponse

from app.core.speed_logic import calculate_speed
from odrl.odrl_eval import ODRLEvaluator
from odrl.pep.transfer import transfer_to

app = FastAPI()

evaluator = ODRLEvaluator("./policies")


def extract_duty_info(duty: dict):
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


@app.post("/decision", response_model=DecisionResponse)
def read_root(data: DecisionRequest):
    history = [data.metadata]
    result = evaluator.evaluate(history)

    if not result["is_valid"]:
        raise HTTPException(status_code=401, detail="Forbidden by ODRL policy.")

    if result["missing_duties"]:
        for duty in result["missing_duties"]:
            action, params = extract_duty_info(duty)

            if action in ["distribute", "transfer"]:
                is_done = transfer_to(endpoint=params["recipient"], data=data.metadata)

                if is_done:
                    history.append(
                        {
                            "http://www.w3.org/ns/odrl/2/dateTime": datetime.datetime.now().isoformat(),
                            "http://www.w3.org/ns/odrl/2/Action": f"http://www.w3.org/ns/odrl/2/{action}",
                            "http://example.com/recipient": params.get("recipient"),
                            "http://example.com/event": params.get(
                                "event", "endOfUsage"
                            ),
                        }
                    )
                else:
                    raise HTTPException(
                        status_code=500, detail="Duty execution failed."
                    )
            else:
                raise HTTPException(
                    status_code=501, detail=f"Unsupported duty: {action}"
                )

        final_result = evaluator.evaluate(history)
        if not final_result["is_valid"] or final_result["missing_duties"]:
            raise HTTPException(status_code=401, detail="Duties validation failed.")

    speed = calculate_speed(data.front, data.state)
    return DecisionResponse(speed=speed)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8002)),
        reload=True,
    )
