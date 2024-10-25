import pandas as pd
import re


def parse_log_line(line):
    log_pattern = r'(?P<ip>[\d\.]+) - - \[(?P<date>.+?)\] "(?P<method>\S+) (?P<url>\S+) HTTP/\d\.\d" (?P<status>\d{3}) (?P<size>\d+)'
    match = re.match(log_pattern, line)
    if match:
        return match.groupdict()
    return None


def load_logs(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [parse_log_line(line) for line in lines if parse_log_line(line)]


def analyze_logs(logs):
    df = pd.DataFrame(logs)
    df['status'] = df['status'].astype(int)
    
    
    errors_4xx = df[df['status'].between(400, 499)].shape[0]
    errors_5xx = df[df['status'].between(500, 599)].shape[0]
    
    print(f"Liczba błędów 4xx: {errors_4xx}")
    print(f"Liczba błędów 5xx: {errors_5xx}")
    
    
    top_urls = df['url'].value_counts().head(10)
    print("Najczęściej wywoływane URL:")
    print(top_urls)


if __name__ == "__main__":
    log_file = '1.log'  
    logs = load_logs(log_file)
    analyze_logs(logs)
