import re
import hashlib

COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123",
    "password1", "letmein", "111111", "iloveyou", "admin",
    "welcome", "monkey", "dragon"
}

seen_hashes = set()  # stand-in for a "database" of previously used passwords


def is_sequential(pw):
    sequences = ["0123456789", "abcdefghijklmnopqrstuvwxyz"]
    lower = pw.lower()
    for seq in sequences:
        for i in range(len(seq) - 3):
            if seq[i:i+4] in lower:
                return True
    return False


def is_repetitive(pw):
    return bool(re.search(r'(.)\1{3,}', pw))


def check_password(pw):
    checks = {
        "12+ characters": len(pw) >= 12,
        "lowercase letter": bool(re.search(r'[a-z]', pw)),
        "uppercase letter": bool(re.search(r'[A-Z]', pw)),
        "number": bool(re.search(r'[0-9]', pw)),
        "symbol": bool(re.search(r'[^A-Za-z0-9]', pw)),
        "not a common password": pw.lower() not in COMMON_PASSWORDS,
        "no repeated/sequential runs": not is_repetitive(pw) and not is_sequential(pw),
    }
    score = sum(checks.values())
    return checks, score


def strength_label(score, max_score):
    pct = score / max_score
    if pct < 0.45:
        return "Weak"
    elif pct < 0.8:
        return "Medium"
    else:
        return "Strong"


def suggest_password():
    import random
    words = ["harbor", "ember", "quartz", "ridge", "lantern", "copper",
             "falcon", "meadow", "signal", "anchor", "birch", "tundra"]
    w1, w2 = random.sample(words, 2)
    num = random.randint(10, 99)
    sym = random.choice("!#$%&*")
    return f"{w1.capitalize()}-{w2}{num}{sym}"


def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def main():
    print("=== Password Strength Analyzer ===")
    while True:
        pw = input("\nEnter a password to test (or 'quit'): ")
        if pw.lower() == "quit":
            break

        checks, score = check_password(pw)
        max_score = len(checks)
        label = strength_label(score, max_score)

        print(f"\nStrength: {label}  ({score}/{max_score} checks passed)")
        for name, passed in checks.items():
            mark = "✔️" if passed else "✘"
            print(f"  {mark} {name}")

        if label != "Strong":
            print(f"\nSuggested alternative: {suggest_password()}")

        pw_hash = hash_password(pw)
        if pw_hash in seen_hashes:
            print("\n⚠️ This password was already tested in this session — try a different one.")
        else:
            seen_hashes.add(pw_hash)


if __name__ == "__main__":
    main()
        
