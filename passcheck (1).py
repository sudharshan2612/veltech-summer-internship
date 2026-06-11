#!/usr/bin/env python3
"""
Simple Password Strength Checker for Kali Linux
Usage: python3 passcheck.py [password]
       python3 passcheck.py (interactive)
"""

import sys, re, math

# Common passwords (short list - add more if needed)
COMMON = {"password","123456","12345678","qwerty","admin","letmein","welcome","monkey","123123","kali"}

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def entropy(pwd):
    charset = 0
    if re.search(r'[a-z]', pwd): charset += 26
    if re.search(r'[A-Z]', pwd): charset += 26
    if re.search(r'\d', pwd): charset += 10
    if re.search(r'[^a-zA-Z0-9]', pwd): charset += 32
    return len(pwd) * math.log2(charset) if charset else 0

def check(pwd):
    score = 0
    feedback = []

    if len(pwd) >= 12: score += 2
    elif len(pwd) >= 8: score += 1
    else: feedback.append("Use at least 8 characters (12+ recommended)")

    if re.search(r'[a-z]', pwd): score += 1
    else: feedback.append("Add lowercase letters")
    
    if re.search(r'[A-Z]', pwd): score += 1
    else: feedback.append("Add uppercase letters")
    
    if re.search(r'\d', pwd): score += 1
    else: feedback.append("Add numbers")
    
    if re.search(r'[^a-zA-Z0-9]', pwd): score += 1
    else: feedback.append("Add special characters (!@#$%)")

    if pwd.lower() in COMMON:
        score = 0
        feedback.append("Password is too common!")

    ent = entropy(pwd)
    
    if score <= 2: strength = f"{RED}WEAK{RESET}"
    elif score <= 4: strength = f"{YELLOW}MEDIUM{RESET}"
    else: strength = f"{GREEN}STRONG{RESET}"

    print(f"\n{BOLD}Password:{RESET} {'*' * len(pwd)}")
    print(f"{BOLD}Length:{RESET} {len(pwd)} | {BOLD}Entropy:{RESET} {ent:.1f} bits")
    print(f"{BOLD}Strength:{RESET} {strength} ({score}/6)")
    
    if feedback:
        print(f"{BOLD}Fix:{RESET}")
        for f in feedback: print(f"  - {f}")
    else:
        print(f"{GREEN}✓ Looks good!{RESET}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pwd = sys.argv[1]
    else:
        import getpass
        pwd = getpass.getpass("Enter password: ")
    
    if not pwd:
        print("No password provided")
        sys.exit(1)
    
    check(pwd)