import json
import re
from typing import List, Tuple
import httpx
from app.data.licenses import normalize_license

KNOWN_NPM_LICENSES = {
    "express": "MIT",
    "react": "MIT",
    "react-dom": "MIT",
    "react-router-dom": "MIT",
    "react-scripts": "MIT",
    "axios": "MIT",
    "lodash": "MIT",
    "moment": "MIT",
    "mongoose": "MIT",
    "jsonwebtoken": "MIT",
    "bcrypt": "MIT",
    "bcryptjs": "MIT",
    "dotenv": "BSD-2-Clause",
    "jest": "MIT",
    "eslint": "MIT",
    "webpack": "MIT",
    "typescript": "Apache-2.0",
    "babel-core": "MIT",
    "@babel/core": "MIT",
    "@babel/preset-env": "MIT",
    "prettier": "MIT",
    "nodemon": "MIT",
    "cors": "MIT",
    "helmet": "MIT",
    "morgan": "MIT",
    "body-parser": "MIT",
    "multer": "MIT",
    "uuid": "MIT",
    "chalk": "MIT",
    "commander": "MIT",
    "yargs": "MIT",
    "inquirer": "MIT",
    "socket.io": "MIT",
    "next": "MIT",
    "vue": "MIT",
    "angular": "MIT",
    "jquery": "MIT",
    "bootstrap": "MIT",
    "tailwindcss": "MIT",
    "vite": "MIT",
    "vitest": "MIT",
    "mocha": "MIT",
    "chai": "MIT",
    "sinon": "BSD-3-Clause",
    "supertest": "MIT",
    "knex": "MIT",
    "sequelize": "MIT",
    "typeorm": "MIT",
    "prisma": "Apache-2.0",
    "redis": "MIT",
    "ioredis": "MIT",
    "mysql2": "MIT",
    "pg": "MIT",
    "sqlite3": "BSD-3-Clause",
    "rxjs": "Apache-2.0",
    "redux": "MIT",
    "mobx": "MIT",
    "immer": "MIT",
    "zod": "MIT",
    "joi": "BSD-3-Clause",
    "ajv": "MIT",
    "date-fns": "MIT",
    "luxon": "MIT",
    "dayjs": "MIT",
    "sharp": "Apache-2.0",
    "jimp": "MIT",
    "puppeteer": "Apache-2.0",
    "playwright": "Apache-2.0",
    "cypress": "MIT",
    "graphql": "MIT",
    "apollo-server": "MIT",
    "passport": "MIT",
    "jsonschema": "MIT",
    "cheerio": "MIT",
    "got": "MIT",
    "node-fetch": "MIT",
    "cross-fetch": "MIT",
}


def _fetch_npm_license(name: str) -> str:
    # Source 1: npm registry (almost always has the license field)
    try:
        r = httpx.get(f"https://registry.npmjs.org/{name}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            lic = data.get("license") or ""
            if lic and isinstance(lic, str) and lic.strip():
                return normalize_license(lic.strip())
            latest = data.get("dist-tags", {}).get("latest", "")
            if latest:
                ver_lic = data.get("versions", {}).get(latest, {}).get("license", "")
                if ver_lic and isinstance(ver_lic, str) and ver_lic.strip():
                    return normalize_license(ver_lic.strip())
    except Exception:
        pass

    # Source 2: Repology
    repology_result = _fetch_from_repology(f"js:{name.lower()}")
    if repology_result != "UNKNOWN":
        return repology_result

    # Source 3: local fallback table
    return KNOWN_NPM_LICENSES.get(name, "UNKNOWN")


# Well-known Python packages whose licenses are stable and not in PyPI metadata
KNOWN_PIP_LICENSES = {
    "fastapi": "MIT",
    "uvicorn": "BSD-3-Clause",
    "starlette": "BSD-3-Clause",
    "pydantic": "MIT",
    "pydantic-core": "MIT",
    "httpx": "BSD-3-Clause",
    "requests": "Apache-2.0",
    "pytest": "MIT",
    "pytest-asyncio": "Apache-2.0",
    "sqlalchemy": "MIT",
    "alembic": "MIT",
    "python-dotenv": "BSD-3-Clause",
    "python-multipart": "Apache-2.0",
    "psycopg2": "LGPL-3.0",
    "psycopg2-binary": "LGPL-3.0",
    "reportlab": "BSD-3-Clause",
    "flask": "BSD-3-Clause",
    "django": "BSD-3-Clause",
    "numpy": "BSD-3-Clause",
    "pandas": "BSD-3-Clause",
    "scipy": "BSD-3-Clause",
    "matplotlib": "BSD-3-Clause",
    "pillow": "MIT",
    "click": "BSD-3-Clause",
    "boto3": "Apache-2.0",
    "botocore": "Apache-2.0",
    "cryptography": "Apache-2.0",
    "certifi": "MPL-2.0",
    "urllib3": "MIT",
    "aiohttp": "Apache-2.0",
    "anyio": "MIT",
    "typing-extensions": "MIT",
    "packaging": "Apache-2.0",
    "setuptools": "MIT",
    "wheel": "MIT",
}


def _fetch_from_repology(repology_name: str) -> str:
    try:
        r = httpx.get(
            f"https://repology.org/api/v1/project/{repology_name}",
            timeout=8,
        )
        if r.status_code == 200:
            from collections import Counter
            licenses = []
            for item in r.json():
                if item.get("licenses"):
                    licenses.extend(item["licenses"])
            most_common = Counter(licenses).most_common(1)
            if most_common:
                return normalize_license(most_common[0][0])
    except Exception:
        pass
    return "UNKNOWN"


def _github_repo_from_pypi(name: str) -> str | None:
    try:
        r = httpx.get(f"https://pypi.org/pypi/{name}/json", timeout=5)
        if r.status_code != 200:
            return None
        info = r.json().get("info", {})
        urls = list((info.get("project_urls") or {}).values())
        home = info.get("home_page") or ""
        for url in urls + [home]:
            # match github.com/owner/repo — stop before /issues /tree /blob etc.
            m = re.search(r'github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:[/#?]|\.git|$)', str(url))
            if m:
                return m.group(1)
    except Exception:
        pass
    return None


def _fetch_pypi_license(name: str) -> str:
    # Source 1: PyPI license field + classifiers
    try:
        r = httpx.get(f"https://pypi.org/pypi/{name}/json", timeout=5)
        if r.status_code == 200:
            info = r.json().get("info", {})
            # license_expression is the newer SPDX field (more reliable)
            for field in ("license_expression", "license"):
                raw = info.get(field) or ""
                if raw and raw.strip() and raw.strip().lower() not in ("unknown", ""):
                    result = normalize_license(raw.strip())
                    if result != "UNKNOWN":
                        return result
            for clf in info.get("classifiers", []):
                if clf.startswith("License ::"):
                    parts = clf.split(" :: ")
                    if len(parts) >= 3:
                        result = normalize_license(parts[-1].strip())
                        if result != "UNKNOWN":
                            return result
    except Exception:
        pass

    # Source 2: GitHub license API via project_urls
    try:
        repo = _github_repo_from_pypi(name)
        if repo:
            r = httpx.get(
                f"https://api.github.com/repos/{repo}/license",
                timeout=5,
                headers={"Accept": "application/vnd.github+json"},
            )
            if r.status_code == 200:
                spdx = r.json().get("license", {}).get("spdx_id", "") or ""
                if spdx and spdx != "NOASSERTION":
                    return normalize_license(spdx)
    except Exception:
        pass

    # Source 3: Repology (aggregates licenses from Alpine, Debian, Fedora etc.)
    repology_result = _fetch_from_repology(f"python:{name.lower()}")
    if repology_result != "UNKNOWN":
        return repology_result

    # Source 4: local fallback table
    normalized_name = name.lower().replace("_", "-")
    return KNOWN_PIP_LICENSES.get(normalized_name, "UNKNOWN")


ParsedDep = dict  # {name, version, license, direct}


def parse_npm_package_json(content: str) -> List[ParsedDep]:
    pkg = json.loads(content)
    deps = []

    def add(section, direct: bool):
        if not section:
            return
        for name, version in section.items():
            deps.append({
                "name": name,
                "version": str(version).lstrip("^~>=<"),
                "license": _fetch_npm_license(name),
                "direct": direct,
            })

    add(pkg.get("dependencies"), True)
    add(pkg.get("devDependencies"), False)
    add(pkg.get("peerDependencies"), False)
    return deps


def parse_npm_package_lock(content: str) -> List[ParsedDep]:
    lock = json.loads(content)
    deps = []
    top_deps = set(lock.get("dependencies", {}).keys())
    packages = lock.get("packages") or lock.get("dependencies") or {}

    for name, info in packages.items():
        if not name:
            continue
        pkg_name = name.replace("node_modules/", "")
        if not pkg_name:
            continue
        deps.append({
            "name": pkg_name,
            "version": info.get("version", "0.0.0"),
            "license": normalize_license(info.get("license")),
            "direct": pkg_name in top_deps,
        })
    return deps


def parse_pip_requirements(content: str) -> List[ParsedDep]:
    deps = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        m = re.match(r"^([A-Za-z0-9_.\-]+)([><=!]=?)?([0-9.*]+)?", line)
        if m:
            name = m.group(1)
            deps.append({
                "name": name,
                "version": m.group(3) or "latest",
                "license": _fetch_pypi_license(name),
                "direct": True,
            })
    return deps


def parse_pipfile_lock(content: str) -> List[ParsedDep]:
    lock = json.loads(content)
    deps = []

    def add(section, direct: bool):
        if not section:
            return
        for name, info in section.items():
            if name == "_meta":
                continue
            version = info if isinstance(info, str) else info.get("version", "unknown")
            deps.append({
                "name": name,
                "version": version.lstrip("=<>!"),
                "license": _fetch_pypi_license(name),
                "direct": direct,
            })

    add(lock.get("default"), True)
    add(lock.get("develop"), False)
    return deps


def detect_ecosystem(filename: str) -> str:
    name = filename.lower()
    if name in ("package.json", "package-lock.json"):
        return "npm"
    if name in ("requirements.txt", "pipfile.lock"):
        return "pip"
    if name == "pom.xml":
        return "maven"
    if name in ("build.gradle", "build.gradle.kts"):
        return "gradle"
    return "unknown"


def parse_file(filename: str, content: str) -> Tuple[List[ParsedDep], str]:
    ecosystem = detect_ecosystem(filename)
    name = filename.lower()

    if name == "package-lock.json":
        return parse_npm_package_lock(content), ecosystem
    elif name == "package.json":
        return parse_npm_package_json(content), ecosystem
    elif name == "requirements.txt":
        return parse_pip_requirements(content), ecosystem
    elif name == "pipfile.lock":
        return parse_pipfile_lock(content), ecosystem
    else:
        raise ValueError(f"Unsupported file: {filename}. Supported: package.json, package-lock.json, requirements.txt, Pipfile.lock")
