import random

GIBBER_CONTENT = ["ERR", "#", "$", "NO", "N/A", "DATA", "WARN", "FAIL", "TIME", "SIG", "!", "?", "%"]

def gibber(length: int) -> str:
    random_string = "".join(random.choice(GIBBER_CONTENT) for _ in range(length))
    return random_string[:length]

def is_gibberish(string: str) -> bool:
    count = sum(char in GIBBER_CONTENT for char in string)
    return count >= len(string) / 4