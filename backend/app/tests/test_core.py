import pytest
from app.modules.parser import parse_dependencies
from app.modules.policy_engine import evaluate_policy
 
 
def test_parse_npm():
    content = '{"dependencies": {"express": "^4.18.0"}, "devDependencies": {"jest": "^29.0.0"}}'
    result = parse_dependencies(content, "package.json")
    assert len(result) == 2
    assert result[0]["name"] == "express"
 
 
def test_parse_python():
    content = "requests==2.31.0\nflask==3.0.0\n# a comment\n"
    result = parse_dependencies(content, "requirements.txt")
    assert len(result) == 2
    assert result[0]["name"] == "requests"
    assert result[0]["version"] == "2.31.0"
 
 
def test_parse_python_ignores_comments():
    content = "# this is a comment\nrequests==2.31.0\n"
    result = parse_dependencies(content, "requirements.txt")
    assert len(result) == 1
 
 
def test_policy_ok():
    deps = [{"name": "some-lib", "version": "1.0.0", "license": "MIT"}]
    result = evaluate_policy(deps)
    assert result[0]["status"] == "OK"
 
 
def test_policy_flagged():
    deps = [{"name": "some-lib", "version": "1.0.0", "license": "GPL-3.0"}]
    result = evaluate_policy(deps)
    assert result[0]["status"] == "FLAGGED"
 
 
def test_policy_review():
    deps = [{"name": "some-lib", "version": "1.0.0", "license": "MPL-2.0"}]
    result = evaluate_policy(deps)
    assert result[0]["status"] == "REVIEW"
 
 
def test_policy_unknown():
    deps = [{"name": "some-lib", "version": "1.0.0", "license": "UNKNOWN"}]
    result = evaluate_policy(deps)
    assert result[0]["status"] == "UNKNOWN"
 
 
def test_parse_invalid_json():
    content = "this is not valid json"
    result = parse_dependencies(content, "package.json")
    assert result == []