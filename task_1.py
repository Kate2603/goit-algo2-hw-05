import hashlib
from typing import List, Dict

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item: str):
        hashes = []
        item_bytes = item.encode('utf-8')
        for i in range(self.num_hashes):
            hash_digest = hashlib.sha256(item_bytes + str(i).encode()).hexdigest()
            hash_value = int(hash_digest, 16) % self.size
            hashes.append(hash_value)
        return hashes

    def add(self, item: str):
        for h in self._hashes(item):
            self.bit_array[h] = 1

    def __contains__(self, item: str) -> bool:
        return all(self.bit_array[h] for h in self._hashes(item))

def check_password_uniqueness(bloom: BloomFilter, passwords: List[str]) -> Dict[str, str]:
    results = {}
    for pwd in passwords:
        if not isinstance(pwd, str) or pwd.strip() == "":
            results[pwd] = "некоректний"
            continue

        if pwd in bloom:
            results[pwd] = "вже використаний"
        else:
            results[pwd] = "унікальний"
            bloom.add(pwd)
    return results

if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")

