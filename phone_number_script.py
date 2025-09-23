import re

# Validation function
def validate_phone(number):
    # Remove spaces, dashes, parentheses, plus signs, and dots to count digits
    digits = re.sub(r'[\s\-\(\)\.+]', '', number)
    
    # Remove leading country code if exists (assume 1-3 digits)
    if len(digits) > 10:
        digits = digits[-10:]
    
    if len(digits) != 10:
        return "Invalid: Must have exactly 10 digits (excluding country code)"

    # Check area code parentheses if present
    if '(' in number or ')' in number:
        if not re.fullmatch(r'.*\(\d{3}\).*', number):
            return "Invalid: Area code parentheses incorrect"

    return "Valid phone number"

# Read interleaved API response
file_path = r"api_response.txt"
try:
    with open(file_path, 'r') as file:
        text = file.read()
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()

# Looser regex to capture all phone-like candidates (including dots)
phone_pattern = r'[\+]?[\d\s\-\(\)\.]{10,20}'

# Extract candidates
phone_candidates = re.findall(phone_pattern, text)

# Remove duplicates and strip leading/trailing spaces
phone_candidates = list(set([p.strip() for p in phone_candidates]))

# Validate each candidate
print("Phone Number Validation Results:\n")
for number in phone_candidates:
    result = validate_phone(number)
    print(f"{number}: {result}")
