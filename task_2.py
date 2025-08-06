import re
import time
import hyperloglog
from typing import List

def extract_ips(filename: str) -> List[str]:
    ip_regex = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    ips = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            match = ip_regex.search(line)
            if match:
                ips.append(match.group())
    return ips

def exact_count(ips: List[str]) -> int:
    return len(set(ips))

def hyperloglog_count(ips: List[str], precision=14) -> int:
    hll = hyperloglog.HyperLogLog(0.01)  # 1% похибка
    for ip in ips:
        hll.add(ip)
    return int(len(hll))

def benchmark():
    log_file = "lms-stage-access.log"

    print("Завантаження даних...")
    ips = extract_ips(log_file)

    print("Початок точного підрахунку...")
    start_exact = time.time()
    exact = exact_count(ips)
    end_exact = time.time()

    print("Початок HyperLogLog підрахунку...")
    start_hll = time.time()
    approx = hyperloglog_count(ips)
    end_hll = time.time()

    print("\nРезультати порівняння:")
    print(f"{'Метод':<25}{'Унікальні елементи':<25}{'Час виконання (сек.)'}")
    print(f"{'Точний підрахунок':<25}{exact:<25}{end_exact - start_exact:.4f}")
    print(f"{'HyperLogLog':<25}{approx:<25}{end_hll - start_hll:.4f}")

if __name__ == "__main__":
    benchmark()
