def evaluate_and_enforce(metadata: dict) -> bool:
    """
    Complete PEP workflow: evaluates, executes duties if needed, and re-verifies.
    Returns True if access is allowed (or became allowed), False otherwise.
    """
    print("First ODRL Evaluation")

    # Initial history contains only the action requested by the client (the "use")
    history = [metadata]

    result = evaluator.evaluate(history)

    # 1. If the policy is purely and simply violated (e.g. outdated firmware)
    if not result["is_valid"]:
        print("DENIED:")
        for v in result["violations"]:
            print(v)
        return False

    # 2. If allowed, but there are duties (obligations)
    if result["missing_duties"]:
        print("ALLOWED UNDER CONDITION. Executing duties...")

        for d in result["missing_duties"]:
            action_to_perform = None
            parameters = {}

            # Decode duty parameters
            for condition in d["conditions"]:
                key = condition[0]
                value = condition[2]

                if "Action" in key:
                    action_to_perform = value.split("/")[-1].split("#")[-1]
                else:
                    param_name = key.split("/")[-1].split("#")[-1]
                    parameters[param_name] = value

            print(f"Required execution: {action_to_perform}() with {parameters}")

            # --- BUSINESS LOGIC EXECUTION (PEP Enforcement) ---
            if action_to_perform == "distribute":
                # Execute the action requested by the policy
                done = pep.transfer_to(parameters["recipient"], data=metadata)

                # CRUCIAL: Create a log to prove to the evaluator we performed the action
                if done:
                    duty_log = {
                        "http://www.w3.org/ns/odrl/2/dateTime": datetime.datetime.now().isoformat(),
                        "http://www.w3.org/ns/odrl/2/Action": f"http://www.w3.org/ns/odrl/2/{action_to_perform}",
                        "http://example.com/recipient": parameters.get("recipient"),
                        "http://example.com/event": parameters.get(
                            "event", "endOfUsage"
                        ),
                    }

                    # Add this proof to the history
                    history.append(duty_log)

        # 3. Re-evaluation after duty execution
        print("Second ODRL Evaluation (Verification of proofs)")
        final_result = evaluator.evaluate(history)

        if final_result["is_valid"] and not final_result["missing_duties"]:
            print("SUCCESS: All conditions have been fulfilled and verified.")
            return True
        else:
            print("FAILURE: Conditions were not properly resolved.")
            return False

    # 4. Directly allowed (no duty)
    print("ALLOWED (No duty).")
    return True
