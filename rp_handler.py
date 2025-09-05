import time
import traceback
from typing import Any, Dict

import runpod


def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    output: Dict[str, Any] = {
        "prompt_received": None,
        "seconds_slept": 0,
        "error": None,
    }

    try:
        print("Worker Start")

        # Accept either {input: {...}} or raw payload
        input_data: Any
        if isinstance(event, dict) and "input" in event:
            input_data = event["input"]
        else:
            input_data = event

        # Extract optional fields, but don't fail if missing/invalid
        prompt = None
        loop_count = 0
        if isinstance(input_data, dict):
            loop_count = input_data.get("loop_count", 0)
            prompt = input_data.get("prompt")
            seconds_raw = input_data.get("seconds", 0)
        else:
            seconds_raw = 0

        if (loop_count > 0):
            counter = loop_count
            while counter > 0:
                print(f"Looping {counter} times, sleeping for 5 seconds...")
                time.sleep(5)
                counter -= 1
            return { "input_echo": input_data, "execution_time_seconds": 5 * loop_count }

        seconds = 0.0
        warnings = []
        try:
            seconds = float(seconds_raw or 0)
            if seconds < 0:
                warnings.append("seconds_was_negative; coerced to 0")
                seconds = 0.0
        except Exception as parse_err:  # best-effort parsing
            warnings.append(
                f"seconds_parse_error: {type(parse_err).__name__}: {parse_err}"
            )
            seconds = 0.0

        print(f"Received prompt: {prompt}")
        print(f"Sleeping for {seconds} seconds...")
        time.sleep(seconds)

        output.update(
            {
                "prompt_received": prompt,
                "seconds_slept": seconds,
                "input_echo": input_data,
            }
        )
        if warnings:
            output["warnings"] = warnings
        return output

    except Exception as error:
        output["error"] = f"{type(error).__name__}: {error}"
        output["traceback"] = traceback.format_exc()
        output["event_echo"] = event
        return output


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
