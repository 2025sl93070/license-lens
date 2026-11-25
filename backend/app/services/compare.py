import uuid
from datetime import datetime, timezone
from typing import List

from app.parsers.file_parser import parse_file
from app.services.analyzer import analyze_project, RISK_ORDER


def compare_projects(
    project_name: str,
    file1_name: str,
    content1: str,
    file2_name: str,
    content2: str,
    policy_id: str = "enterprise-safe",
) -> dict:
    deps1, eco1 = parse_file(file1_name, content1)
    deps2, eco2 = parse_file(file2_name, content2)

    result1 = analyze_project(f"{project_name} (baseline)", eco1, deps1, policy_id)
    result2 = analyze_project(f"{project_name} (current)", eco2, deps2, policy_id)

    map1 = {d["name"]: d for d in result1["dependencies"]}
    map2 = {d["name"]: d for d in result2["dependencies"]}
    names1 = set(map1)
    names2 = set(map2)

    added = [map2[n] for n in sorted(names2 - names1)]
    removed = [map1[n] for n in sorted(names1 - names2)]

    license_changed = []
    risk_increased = []
    risk_decreased = []

    for name in sorted(names1 & names2):
        d1 = map1[name]
        d2 = map2[name]
        if d1["license"] != d2["license"]:
            license_changed.append({
                "name": name,
                "oldLicense": d1["license"],
                "newLicense": d2["license"],
                "oldRisk": d1["riskLevel"],
                "newRisk": d2["riskLevel"],
                "riskReasons": d2["riskReasons"],
                "version": d2["version"],
            })
        elif RISK_ORDER[d2["riskLevel"]] > RISK_ORDER[d1["riskLevel"]]:
            risk_increased.append({
                "name": name,
                "license": d2["license"],
                "oldRisk": d1["riskLevel"],
                "newRisk": d2["riskLevel"],
                "version": d2["version"],
            })
        elif RISK_ORDER[d2["riskLevel"]] < RISK_ORDER[d1["riskLevel"]]:
            risk_decreased.append({
                "name": name,
                "license": d2["license"],
                "oldRisk": d1["riskLevel"],
                "newRisk": d2["riskLevel"],
                "version": d2["version"],
            })

    # Conflicts
    def conflict_key(c: dict) -> str:
        return f"{min(c['dep1'], c['dep2'])}|{max(c['dep1'], c['dep2'])}"

    old_conflict_keys = {conflict_key(c) for c in result1["conflicts"]}
    new_conflict_keys = {conflict_key(c) for c in result2["conflicts"]}

    new_conflicts = [c for c in result2["conflicts"] if conflict_key(c) not in old_conflict_keys]
    resolved_conflicts = [c for c in result1["conflicts"] if conflict_key(c) not in new_conflict_keys]

    # Policy violations
    old_viol_keys = {v["dependencyName"] for v in result1["policyViolations"]}
    new_viol_keys = {v["dependencyName"] for v in result2["policyViolations"]}

    new_violations = [v for v in result2["policyViolations"] if v["dependencyName"] not in old_viol_keys]
    resolved_violations = [v for v in result1["policyViolations"] if v["dependencyName"] not in new_viol_keys]

    # Overall risk change
    r1 = result1["overallRisk"]
    r2 = result2["overallRisk"]
    if RISK_ORDER[r2] > RISK_ORDER[r1]:
        risk_direction = "increased"
    elif RISK_ORDER[r2] < RISK_ORDER[r1]:
        risk_direction = "decreased"
    else:
        risk_direction = "unchanged"

    return {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "projectName": project_name,
        "policyId": policy_id,
        "baseline": {
            "filename": file1_name,
            "ecosystem": eco1,
            "totalDependencies": result1["totalDependencies"],
            "directDependencies": result1["directDependencies"],
            "transitiveDependencies": result1["transitiveDependencies"],
            "overallRisk": r1,
        },
        "current": {
            "filename": file2_name,
            "ecosystem": eco2,
            "totalDependencies": result2["totalDependencies"],
            "directDependencies": result2["directDependencies"],
            "transitiveDependencies": result2["transitiveDependencies"],
            "overallRisk": r2,
        },
        "riskDirection": risk_direction,
        "added": added,
        "removed": removed,
        "licenseChanged": license_changed,
        "riskIncreased": risk_increased,
        "riskDecreased": risk_decreased,
        "newConflicts": new_conflicts,
        "resolvedConflicts": resolved_conflicts,
        "newViolations": new_violations,
        "resolvedViolations": resolved_violations,
        "summary": {
            "added": len(added),
            "removed": len(removed),
            "licenseChanged": len(license_changed),
            "riskIncreased": len(risk_increased),
            "riskDecreased": len(risk_decreased),
            "newConflicts": len(new_conflicts),
            "resolvedConflicts": len(resolved_conflicts),
            "newViolations": len(new_violations),
            "resolvedViolations": len(resolved_violations),
        },
    }
