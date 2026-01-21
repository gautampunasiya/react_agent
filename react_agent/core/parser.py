import re
import json

def parse_react_output(text: str):
    if "Final Answer:" in text:
        return {
            "type": "final",
            "output": text.split("Final Answer:")[1].strip()
        }

    action_match = re.search(r"Action:\s*(\w+)", text)
    input_match = re.search(r"Action Input:\s*(\{.*\})", text, re.S)

    if action_match and input_match:
        return {
            "type": "action",
            "tool": action_match.group(1),
            "input": json.loads(input_match.group(1))
        }

    return {
        "type": "direct",
        "output": text.strip()
    }


