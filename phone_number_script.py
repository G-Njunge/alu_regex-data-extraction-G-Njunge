import re

def validate_phone(number):
    # Remove non-digit characters
    digits = re.sub(r'\D', '', number)

    # Strip country code if more than 10 digits
    if len(digits) > 10:
        digits = digits[-10:]

    if len(digits) != 10:
        return "Invalid: Must have exactly 10 digits (excluding country code)"

    # Area code parentheses check
    if '(' in number or ')' in number:
        if not re.fullmatch(r'\(\d{3}\)[\s.-]?\d{3}[\s.-]?\d{4}', number):
            return "Invalid: Area code parentheses incorrect"

    return "Valid phone number"


# Read file
file_path = r"api_response.txt"
try:
    with open(file_path, 'r') as file:
        text = file.read()
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()

# Stricter regex: only match full 10-digit numbers with optional separators and optional country code
phone_pattern = r'\b(?:\+?\d{1,3}[\s.-]?)?(?:\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}\b'

# Extract candidates
phone_candidates = [m.group(0) for m in re.finditer(phone_pattern, text)]

# Remove duplicates
phone_candidates = list(dict.fromkeys(phone_candidates))

# Filter out credit card-like numbers (16 digits)
def is_credit_card_like(number):
    digits_only = re.sub(r'\D', '', number)
    return len(digits_only) == 16

phone_candidates = [p for p in phone_candidates if not is_credit_card_like(p)]

# Validate each candidate
print("Phone Number Validation Results:\n")
for number in phone_candidates:
    result = validate_phone(number)
    print(f"{number}: {result}")
