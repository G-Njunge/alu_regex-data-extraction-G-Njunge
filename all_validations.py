import re
#EMAIL VALIDATION.
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
print("\nEmail Validation Results:")
for email in all_email_candidates:
    result = validate_email(email)
    print(f"{email}: {result}")



#TIME VALIDATION
# Validation function 
def validate_time(candidate):
    """
    candidate: string matched like '14:30', '2:30 PM', '12:59am', '00:00'
    Returns a descriptive validation string.
    """
    # Normalize whitespace and uppercase AM/PM
    s = candidate.strip()
    # Extract optional AM/PM (case-insensitive)
    m = re.fullmatch(r'(\d{1,2}):(\d{2})(?:\s*([AaPp][Mm]))?', s)
    if not m:
        return "Invalid: Doesn't match H:MM or H:MM AM/PM pattern"

    hour_str, minute_str, ampm = m.group(1), m.group(2), m.group(3)

    # Convert to ints, but guard against non-numeric (shouldn't happen from regex)
    try:
        hour = int(hour_str)
        minute = int(minute_str)
    except ValueError:
        return "Invalid: Non-numeric hour or minute"

    # Validate minute range universally
    if not (0 <= minute <= 59):
        return "Invalid: Minute out of range (0-59)"

    # If AM/PM present -> treat as 12-hour format
    if ampm:
        # Accept 1..12 for hours in 12-hour format (0 not allowed)
        if not (1 <= hour <= 12):
            return "Invalid: Hour out of range for 12-hour format (1-12)"
        return f"Valid 12-hour time (normalized: {hour:02d}:{minute:02d} {ampm.upper()})"
    else:
        # No AM/PM -> treat as 24-hour format
        if not (0 <= hour <= 23):
            return "Invalid: Hour out of range for 24-hour format (0-23)"
        return f"Valid 24-hour time (normalized: {hour:02d}:{minute:02d})"

# Read interleaved API response
file_path = r"api_response.txt"
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    raise SystemExit(1)

# Candidate extraction:
# Match patterns like '2:30 PM', '14:30', '00:00', '2:30PM' (optional space), case-insensitive AM/PM
time_candidate_pattern = r'\b\d{1,2}:\d{2}(?:\s*[AaPp][Mm])?\b'

candidates = re.findall(time_candidate_pattern, text)
# Deduplicate while preserving order
seen = set()
candidates_unique = []
for c in candidates:
    cc = c.strip()
    if cc not in seen:
        seen.add(cc)
        candidates_unique.append(cc)

# Validate and print
print("\nTime Validation Results:")
for cand in candidates_unique:
    result = validate_time(cand)
    print(f"{cand}: {result}")



##CREDIT CARD VALIDATION
# Issuer detection function
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
        return "Invalid: Contains nondigit characters"

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
print("\nCredit Card Validation Results):")
for card in cc_candidates:
    result = validate_credit_card(card)
    print(f"{card}: {result}")



##CURRENCY VALIDATION
def validate_currency(candidate):
    """
    Validates currency amounts with mandatory currency markers:
    Examples: $1234.56, £1,234.56, 12.50 RWF, Ksh 1200
    Returns detailed messages for invalid entries.
    """
    s = candidate.strip()

    # Must have a currency marker: symbol or code
    marker_pattern = r'^\s*(?:\$|£|€|RWF|UGX|USD|EUR|GBP|KSH|KES)'
    marker_pattern_end = r'(?:RWF|UGX|USD|EUR|GBP|KSH|KES)\s*$'

    if not re.search(marker_pattern, s, flags=re.IGNORECASE) and not re.search(marker_pattern_end, s, flags=re.IGNORECASE):
        return "Invalid: Missing currency marker"

    # Remove known symbols/codes for numeric validation
    numeric_part = re.sub(r'(?:\$|£|€|RWF|UGX|USD|EUR|GBP|KSH|KES)', '', s, flags=re.IGNORECASE).strip()

    # Split integer and decimal if exists
    if '.' in numeric_part:
        int_part, dec_part = numeric_part.split('.', 1)
        if len(dec_part) != 2 or not dec_part.isdigit():
            return "Invalid: Decimal part must have exactly 2 digits"
    else:
        int_part = numeric_part
        dec_part = None

    # Remove commas for numeric check
    int_clean = int_part.replace(',', '')
    if not int_clean.isdigit():
        return "Invalid: Contains non-digit characters in integer part"

    # Check commas placement (thousands separators)
    groups = int_part.split(',')
    if len(groups) > 1:
        if len(groups[0]) > 3 or any(len(g) != 3 for g in groups[1:]):
            return "Invalid: Incorrect comma placement in thousands"

    return "Valid currency amount"


# Read file
file_path = r"api_response.txt"
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    raise SystemExit(1)

# Regex to capture numbers with mandatory currency markers
currency_pattern = r'(?:\$|£|€|RWF|UGX|USD|EUR|GBP|KSH|KES)\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?|' \
                   r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:RWF|UGX|USD|EUR|GBP|KSH|KES)'

candidates = re.findall(currency_pattern, text, flags=re.IGNORECASE)
# Deduplicate and remove empty matches
candidates_unique = list(dict.fromkeys([c.strip() for c in candidates if c.strip()]))

# Validate each candidate
print("\nCurrency Validation Results:")
for cand in candidates_unique:
    result = validate_currency(cand)
    print(f"{cand}: {result}")


##PHONE NUMBER VALIDATION
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
print("\nPhone Number Validation Results:")
for number in phone_candidates:
    result = validate_phone(number)
    print(f"{number}: {result}")
