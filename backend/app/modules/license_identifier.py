import requests
 
 
def identify_licenses(dependencies: list, filename: str) -> list:
    results = []
    for dep in dependencies:
        name = dep["name"]
        if filename == "package.json":
            license_info = _fetch_npm_license(name)
        else:
            license_info = _fetch_pypi_license(name)
 
        results.append({
            "name": name,
            "version": dep["version"],
            "license": license_info
        })
    return results
 
 
def _fetch_npm_license(package_name: str) -> str:
    try:
        response = requests.get(
            f"https://registry.npmjs.org/{package_name}/latest",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("license", "UNKNOWN")
    except Exception:
        pass
    return "UNKNOWN"
 
 
def _fetch_pypi_license(package_name: str) -> str:
    try:
        response = requests.get(
            f"https://pypi.org/pypi/{package_name}/json",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("info", {}).get("license", "UNKNOWN") or "UNKNOWN"
    except Exception:
        pass
    return "UNKNOWN"