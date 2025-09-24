import re

# Validation function
def validate_email(email):
    # Check for exactly one @ symbol
    if email.count('@') != 1:
        return "Invalid: Missing or multiple @ symbols"

    username, domain_part = email.split('@')

    # Username: letters, digits, dot, dash, underscore
    if not re.fullmatch(r'[\w\.-]+', username):
        return "Invalid: Username contains illegal characters or spaces"

    # Domain must contain at least one dot
    if '.' not in domain_part:
        return "Invalid: Domain missing '.'"

    # Split domain into parts
    domain_parts = domain_part.split('.')
    for part in domain_parts[:-1]:
        if not re.fullmatch(r'[\w-]+', part):
            return f"Invalid: Domain name part '{part}' contains illegal characters"

    # Top-level domain check
    if not re.fullmatch(r'[a-zA-Z]{2,}', domain_parts[-1]):
        return f"Invalid: Top-level domain '{domain_parts[-1]}' is invalid"

    return "Valid email"

# Read interleaved API response
file_path = r"api_response.txt"
try:
    with open(file_path, 'r') as file:
        text = file.read()
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()

# Step 1: Extract standard emails (with @)
emails_with_at = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)

# Step 2: Extract "email-like" strings without @ but containing a dot
emails_without_at = re.findall(r'\b[\w\.-]+\.[\w\.-]+\b', text)

# Step 2a: Remove purely numeric strings (e.g., 123.456)
emails_without_at = [
    e for e in emails_without_at 
    # Remove purely numeric strings
    if not re.fullmatch(r'[\d\.]+', e)
    # Keep only if there's at least one letter before the first dot
    and re.search(r'[a-zA-Z]', e.split('.')[0])
]

# Step 3: Combine both lists, remove duplicates
all_email_candidates = list(set(emails_with_at + emails_without_at))

# Step 4: Validate each candidate
print("Email Validation Results:\n")
for email in all_email_candidates:
    result = validate_email(email)
    print(f"{email}: {result}")
