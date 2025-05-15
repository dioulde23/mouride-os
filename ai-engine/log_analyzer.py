# ai-engine/log_analyzer.py

def detect_anomalies(log_lines):
    anomalies = []
    keywords = ["ERROR", "FAIL", "CRITICAL", "WARNING"]

    for line in log_lines:
        if any(keyword in line.upper() for keyword in keywords):
            anomalies.append(line.strip())

    return anomalies
 
 
 
import re

SUSPICIOUS_PATTERNS = [
    r"error", r"failed", r"unauthorized", r"denied", r"attack", r"injection", r"malware"
]

def detect_anomalies(log_line):
    anomalies = []
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, log_line, re.IGNORECASE):
            anomalies.append(pattern)
    return anomalies
