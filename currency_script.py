import re

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
print("Currency Validation Results:\n")
for cand in candidates_unique:
    result = validate_currency(cand)
    print(f"{cand}: {result}")
