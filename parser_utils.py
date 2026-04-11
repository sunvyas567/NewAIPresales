# parser_utils.py

import json
import re

def parse_to_payload(content):

    if isinstance(content, dict):
        return content

    if isinstance(content, str):
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)

        if json_match:
            try:
                return json.loads(json_match.group(1))
            except:
                pass

    try:
        parsed = json.loads(content)
        if "sections" in parsed:
            return parsed
    except:
        pass

    sections = []

    parts = content.split("\n\n")

    for i, p in enumerate(parts):
        if p.strip():
            sections.append({
                "title": f"Section {i+1}",
                "content": p.strip()
            })

    return {"sections": sections}