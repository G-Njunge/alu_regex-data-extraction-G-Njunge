import re

# Validation function for times
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
print("Time Validation Results:\n")
for cand in candidates_unique:
    result = validate_time(cand)
    print(f"{cand}: {result}")
