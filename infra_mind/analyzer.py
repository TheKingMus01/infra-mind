
import re
from pathlib import Path
from collections import Counter

PATTERNS = {
    "OUT_OF_MEMORY": {
        "regex": r"out of memory|oom.?killed|killed process",
        "severity": "CRITICAL",
        "cause": "The system may be running out of available memory.",
        "recommendation": "Inspect memory usage, running processes and container memory limits."
    },
    "DISK_FULL": {
        "regex": r"no space left on device|disk full|filesystem full",
        "severity": "CRITICAL",
        "cause": "The filesystem may have exhausted its available storage.",
        "recommendation": "Check disk usage, large files, logs and storage allocation."
    },
    "CONNECTION_FAILURE": {
        "regex": r"connection refused|connection reset|failed to connect",
        "severity": "HIGH",
        "cause": "A service may be unavailable or refusing connections.",
        "recommendation": "Check service health, network connectivity and listening ports."
    },
    "TIMEOUT": {
        "regex": r"connection timed out|request timeout|deadline exceeded",
        "severity": "HIGH",
        "cause": "A service or network request may be taking too long.",
        "recommendation": "Investigate service latency, network conditions and dependencies."
    },
    "PERMISSION_ERROR": {
        "regex": r"permission denied|access denied|unauthorized",
        "severity": "MEDIUM",
        "cause": "A process may lack the required permissions.",
        "recommendation": "Review user permissions, IAM policies and access configuration."
    },
    "SERVICE_FAILURE": {
        "regex": r"crashloopbackoff|service unavailable|fatal error",
        "severity": "HIGH",
        "cause": "An application or infrastructure service may have failed.",
        "recommendation": "Inspect service logs, health checks and recent deployments."
    },
    "TLS_ERROR": {
        "regex": r"certificate expired|ssl handshake failed|tls handshake error",
        "severity": "HIGH",
        "cause": "A TLS certificate or handshake issue may be affecting connectivity.",
        "recommendation": "Verify certificate validity, certificate chains and TLS configuration."
    },
}


def redact_sensitive_data(message):
    """Hide common secrets before including log snippets in reports."""
    patterns = [
        r"(?i)(password|passwd|token|api[_-]?key|secret)\s*[:=]\s*\S+",
        r"(?i)(authorization:\s*bearer)\s+\S+",
    ]

    for pattern in patterns:
        message = re.sub(pattern, "[REDACTED]", message)

    return message[:240]


def analyze_log(file_path):
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Log file not found: {path}")

    findings = []

    with path.open("r", encoding="utf-8", errors="replace") as log_file:
        for line_number, line in enumerate(log_file, start=1):
            for issue, details in PATTERNS.items():
                if re.search(details["regex"], line, re.IGNORECASE):
                    findings.append({
                        "issue": issue,
                        "severity": details["severity"],
                        "line": line_number,
                        "message": redact_sensitive_data(line.strip()),
                        "possible_cause": details["cause"],
                        "recommendation": details["recommendation"]
                    })

    return {
        "source": path.name,
        "total_findings": len(findings),
        "severity_summary": dict(
            Counter(item["severity"] for item in findings)
        ),
        "findings": findings
    }
