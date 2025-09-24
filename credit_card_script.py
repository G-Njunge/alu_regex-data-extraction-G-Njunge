import re

# --- Issuer detection (simple prefix rules) ---
def detect_issuer(clean_card):
    # Visa: starts with 4, usually 13 or 16 digits
    if clean_card.startswith('4') and len(clean_card) in (13, 16):
        return 'Visa'
    # American Express: starts with 34 or 37, 15 digits
    if clean_card[:2] in ('34', '37') and len(clean_card) == 15:
        return 'American Express'
    # MasterCard: 51-55 OR 2221-2720, usually 16 digits
    start2 = int(clean_card[:2]) if len(clean_card) >= 2 and clean_card[:2].isdigit() else -1
    start4 = int(clean_card[:4]) if len(clean_card) >= 4 and clean_card[:4].isdigit() else -1
    if (51 <= start2 <= 55 or 2221 <= start4 <= 2720) and len(clean_card) == 16:
        return 'MasterCard'
    # Discover: 6011, 65, 644-649 (typical 16 digits)
    if (clean_card.startswith('6011') or clean_card.startswith('65') or
        (len(clean_card) >= 3 and 644 <= int(clean_card[:3]) <= 649)) and len(clean_card) == 16:
        return 'Discover'
    # Fallback: unknown issuer but plausible length
    return None

def is_repeated_sequence(s):
    return all(ch == s[0] for ch in s)

# Validation function (no Luhn)
def validate_credit_card(card):
    # Remove spaces and dashes
    clean_card = re.sub(r'[\s-]', '', card)

    # Ensure only digits remain
    if not clean_card.isdigit():
        return "Invalid: Contains non-digit characters"

    # Check digit length
    if not (13 <= len(clean_card) <= 16):
        return "Invalid: Must be 13–16 digits long"

    # Reject obvious repeated digit sequences like '0000...'
    if is_repeated_sequence(clean_card):
        return "Invalid: Repeated digit sequence (unlikely to be real card)"

    # Check issuer heuristics
    issuer = detect_issuer(clean_card)
    if issuer:
        return f"Valid credit card number (Issuer: {issuer})"

    # If format is OK but issuer unknown, still plausible
    return "Valid credit card number (Issuer: Unknown but plausible)"

# Read interleaved API response
file_path = r"api_response.txt"
try:
    with open(file_path, 'r') as file:
        text = file.read()
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()

# Regex to capture common card formats (groups of 4 separated by space/dash OR continuous digits)
cc_pattern = r'(?:\d{4}[-\s]?){3}\d{4}|\d{13,16}'

# Extract candidates
cc_candidates = re.findall(cc_pattern, text)

# Clean up 
cc_candidates = list(dict.fromkeys([c.strip() for c in cc_candidates]))  # preserves order

# Validate each candidate
print("Credit Card Validation Results (heuristic, no Luhn):\n")
for card in cc_candidates:
    result = validate_credit_card(card)
    print(f"{card}: {result}")
