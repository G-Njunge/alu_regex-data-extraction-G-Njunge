import re

def validate_currency(candidate):
    """
    Validates currency amounts of the form:
    $1234.56 or $1,234.56
    Returns detailed messages for invalid entries.
    """
    s = candidate.strip()

    # Extract numeric part
    numeric_part = s[1:]  # remove $
    # Split integer and decimal if exists
    if '.' in numeric_part:
        int_part, dec_part = numeric_part.split('.', 1)
        if len(dec_part) != 2 or not dec_part.isdigit():
            return "Invalid: Decimal part must have exactly 2 digits"
    else:
        int_part = numeric_part
        dec_part = None

    # Check integer part
    # Remove commas for numeric check
    int_clean = int_part.replace(',', '')
    if not int_clean.isdigit():
        return "Invalid: Contains non-digit characters in integer part"

    # Check commas placement (thousands separators)
    groups = int_part.split(',')
    if len(groups) > 1:
        # first group can have 1-3 digits, others must have exactly 3
        if len(groups[0]) > 3 or any(len(g) != 3 for g in groups[1:]):
            return "Invalid: Incorrect comma placement in thousands"

    return "Valid currency amount"

# Read interleaved API response
file_path = r"api_response.txt"
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    raise SystemExit(1)

# Regex to capture currency amounts
currency_pattern = r'\$[\d,]+(?:\.\d{2})?'

candidates = re.findall(currency_pattern, text)
# Deduplicate
candidates_unique = list(dict.fromkeys([c.strip() for c in candidates]))

# Validate each candidate
print("Currency Validation Results:\n")
for cand in candidates_unique:
    result = validate_currency(cand)
    print(f"{cand}: {result}")
