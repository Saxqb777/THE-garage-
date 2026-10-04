"""Part key validation against the naming spec and the parts contract.

Spec: docs/part-naming.md. Contract: src/data/parts.m1.json.
"""
import json
import os
import re

SYSTEMS = ("BODY", "DOOR", "GLASS", "WHEEL", "SUSP", "BRAKE", "ENG", "COOL", "EXH",
           "TRANS", "DRIVE", "ELEC", "INT", "AC", "LIGHT", "TRIM")
KEY_RE = re.compile(r"^(%s)_(\d{4})_([a-z0-9]+(?:_[a-z0-9]+)*?)(?:_(L|R|F|RR))?$" % "|".join(SYSTEMS))

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONTRACT = os.path.join(REPO, "src", "data", "parts.m1.json")


def parse(key):
    m = KEY_RE.match(key)
    if not m:
        return None
    system, group, name, side = m.groups()
    return {"system": system, "groupCode": group, "name": name, "side": side}


def load_contract(path=CONTRACT):
    with open(path) as f:
        data = json.load(f)
    return {p["key"]: p for p in data["parts"]}


def validate_contract(parts):
    """Return a list of problems in the contract itself (empty when clean)."""
    problems = []
    for key, p in parts.items():
        parsed = parse(key)
        if parsed is None:
            problems.append(f"{key}: does not match the naming pattern")
            continue
        if parsed["system"] != p["system"]:
            problems.append(f"{key}: system field {p['system']} disagrees with key")
        if parsed["groupCode"] != p["groupCode"]:
            problems.append(f"{key}: groupCode field {p['groupCode']} disagrees with key")
        if p["groupCode"] == "0000" and p.get("groupStatus") != "unknown":
            problems.append(f"{key}: code 0000 must have groupStatus unknown")
        if p.get("parent") and p["parent"] not in parts:
            problems.append(f"{key}: parent {p['parent']} is not in the contract")
    return problems


if __name__ == "__main__":
    parts = load_contract()
    issues = validate_contract(parts)
    print(f"{len(parts)} parts in contract, {len(issues)} problems")
    for i in issues:
        print("  ", i)
    unknown = sorted(k for k, p in parts.items() if p["groupCode"] == "0000")
    print(f"{len(unknown)} parts flagged with group code 0000")
