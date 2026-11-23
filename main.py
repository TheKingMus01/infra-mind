
import argparse
import json
from pathlib import Path

from infra_mind.analyzer import analyze_log


def main():
    parser = argparse.ArgumentParser(
        description="InfraMind - Infrastructure Log Analyzer"
    )

    parser.add_argument(
        "logfile",
        help="Path to the infrastructure log file"
    )

    parser.add_argument(
        "--output",
        default="reports/incident-report.json",
        help="Path where the report will be saved"
    )

    args = parser.parse_args()

    try:
        report = analyze_log(args.logfile)

        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)

        output.write_text(
            json.dumps(report, indent=4),
            encoding="utf-8"
        )

        print("\n=== InfraMind Incident Analysis ===")
        print(f"Source: {report['source']}")
        print(f"Findings: {report['total_findings']}")
        print(f"Severity: {report['severity_summary']}")
        print(f"\nReport saved to: {output}")

        for finding in report["findings"]:
            print(
                f"\n[{finding['severity']}] {finding['issue']}"
                f"\nLine: {finding['line']}"
                f"\nCause: {finding['possible_cause']}"
                f"\nRecommendation: {finding['recommendation']}"
            )

    except (FileNotFoundError, OSError) as error:
        print(f"Error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
