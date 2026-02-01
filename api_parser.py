import yaml
import json

def parse_openapi(file):
    with open(file) as f:
        data = yaml.safe_load(f) if file.endswith(".yaml") else json.load(f)

    endpoints = []
    for path, methods in data["paths"].items():
        for method, details in methods.items():
            endpoints.append((method.upper(), path, details))
    return endpoints
