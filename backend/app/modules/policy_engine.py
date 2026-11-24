RISKY_LICENSES = ["GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.1", "LGPL-3.0"]
REVIEW_LICENSES = ["MPL-2.0", "CDDL-1.0", "EPL-2.0"]
SAFE_LICENSES = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "0BSD"]
 
 
def evaluate_policy(dependencies: list) -> list:
    results = []
    for dep in dependencies:
        license_id = dep.get("license", "UNKNOWN")
        status, reason, suggestion = _evaluate(license_id)
        results.append({
            "name": dep["name"],
            "version": dep["version"],
            "license": license_id,
            "status": status,
            "reason": reason,
            "suggestion": suggestion
        })
    return results
 
 
def _evaluate(license_id: str):
    if not license_id or license_id == "UNKNOWN":
        return (
            "UNKNOWN",
            "License information could not be identified for this dependency.",
            "Review the package repository manually to determine its license."
        )
 
    normalized = license_id.upper()
 
    for risky in RISKY_LICENSES:
        if risky.upper() in normalized:
            return (
                "FLAGGED",
                f"{license_id} is a copyleft license. It may require your project to be released under the same license.",
                "Consider replacing this dependency or reviewing your project's license obligations."
            )
 
    for review in REVIEW_LICENSES:
        if review.upper() in normalized:
            return (
                "REVIEW",
                f"{license_id} has specific conditions that may require review depending on your use case.",
                "Review the license terms and consult your project's licensing policy."
            )
 
    for safe in SAFE_LICENSES:
        if safe.upper() in normalized:
            return (
                "OK",
                f"{license_id} is a permissive license with minimal restrictions.",
                None
            )
 
    return (
        "REVIEW",
        f"{license_id} is not in the known safe or flagged license list.",
        "Review this license manually before proceeding."
    )