import os
import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.api.schemas import TrajectoryRequest

from app.core.trajectory_logic import build_trajectory_map
from odrl.odrl_eval import ODRLEvaluator
from odrl.pep.transfer import transfer_to

app = FastAPI()

evaluator = ODRLEvaluator("./policies")


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


@app.post("/trajectory_planning")
async def navigation_endpoint(data: TrajectoryRequest):
    """Handle trajectory planning requests."""

    history = [data.metadata]
    result = evaluator.evaluate(history)

    if not result["is_valid"]:
        raise HTTPException(
            status_code=401,
            detail=f"Access denied. Violations: {result['violations']}",
        )

    if result["missing_duties"]:
        for duty in result["missing_duties"]:
            action, params = extract_duty_info(duty)

            if action == "transfer":
                is_done = transfer_to(endpoint=params["recipient"], data=data.metadata)

                if is_done:
                    duty_log = {
                        "http://www.w3.org/ns/odrl/2/dateTime": datetime.datetime.now().isoformat(),
                        "http://www.w3.org/ns/odrl/2/Action": f"http://www.w3.org/ns/odrl/2/{action}",
                        "http://example.com/recipient": params.get("recipient"),
                        "http://example.com/event": params.get("event", "endOfUsage"),
                    }
                    history.append(duty_log)
                else:
                    raise HTTPException(
                        status_code=500,
                        detail="Failed to execute the required Duty.",
                    )
            else:
                raise HTTPException(
                    status_code=501,
                    detail=f"Unknown or unsupported Duty for this PEP: {action}",
                )

        final_result = evaluator.evaluate(history)

        if not final_result["is_valid"] or final_result["missing_duties"]:
            raise HTTPException(
                status_code=401,
                detail="The conditions were not validated by the evaluator after execution.",
            )

    folium_map = build_trajectory_map(data.start_address, data.destination_address)
    map_file = "map.html"
    folium_map.save(map_file)

    return FileResponse(map_file, media_type="file", filename=map_file)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True,
    )
