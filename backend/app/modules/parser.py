import json
 
 
def parse_dependencies(content: str, filename: str) -> list:

    if filename == "package.json":

        return _parse_npm(content)

    elif filename == "requirements.txt":

        return _parse_python(content)

    return []
 
 
def _parse_npm(content: str) -> list:

    try:

        data = json.loads(content)

    except json.JSONDecodeError:

        return []
 
    dependencies = {}

    dependencies.update(data.get("dependencies", {}))

    dependencies.update(data.get("devDependencies", {}))
 
    return [

        {"name": name, "version": version.lstrip("^~")}

        for name, version in dependencies.items()

    ]
 
 
def _parse_python(content: str) -> list:

    packages = []

    for line in content.splitlines():

        line = line.strip()

        if not line or line.startswith("#"):

            continue

        if "==" in line:

            name, version = line.split("==", 1)

            packages.append({"name": name.strip(), "version": version.strip()})

        else:

            packages.append({"name": line.strip(), "version": "latest"})

    return packages
 