# ALU Regex Data Extraction - {YourUsername}

## Project Overview
This project is a **Regex-based Data Extraction Tool** developed as part of the Formative One - Regex Onboarding Hackathon.  
The goal is to simulate processing large API responses containing mixed content (valid,invalid data and noise) and accurately **extract and validate** the following data types:

1. **Email Addresses**  
2. **Phone Numbers**  
3. **Credit Card Numbers**  
4. **Time (12-hour and 24-hour formats)**  
5. **Currency Amounts**

The tool demonstrates:
- Effective use of **regular expressions** for pattern matching.  
- **Validation logic** to handle edge cases.  
- Clear, user-friendly output for both **valid and invalid entries**.  
- Modular, readable, and maintainable Python code.

---

## Features

### 1. Emails
- Extracts emails from text and validates:
  - Must have a username (letters, numbers, underscores, hyphens)
  - Must have `@` and a domain
  - Supports subdomains and `.co.uk` style domains
- Flags invalid formats (missing `@`, invalid characters, numeric-only usernames)

### 2. Phone Numbers
- Supports multiple formats:
  - `(123) 456-7890`
  - `123-456-7890`
  - `123 456 7890`
  - `123.456.7890`
  - Optional country code prefixes
- Flags invalid numbers:
  - Wrong digit count
  - Malformed parentheses
  - Incorrect separators

### 3. Credit Card Numbers
- Extracts numbers in these formats:
  - `1234 5678 9012 3456`
  - `1234-5678-9012-3456`
  - `1234567890123456`
- Validates using:
  - 13–16 digits
  - Digits-only check
  - Rejects obvious repeated sequences (`0000...`)
  - Heuristic issuer detection (Visa, MasterCard, AmEx, Discover)
- Flags invalid lengths or malformed entries

### 4. Time
- Supports:
  - 24-hour format: `00:00`–`23:59`
  - 12-hour format: `1:00 AM`–`12:59 PM`
- Validates hour and minute ranges
- Flags invalid times like `25:00`, `2:60 PM`, `14.30`

### 5. Currency
- Recognizes:
  - `$19.99`
  - `$1,234.56`
- Validates:
  - Correct thousand separators
  - Exactly 2 decimal digits
  - Only digits in the integer part
- Flags malformed amounts like `$12.3` or `$1,23,456.78`

---

## Repository Structure

alu_regex-data-extraction-G-Njunge/
│
├── api_response.txt # Sample API response with mixed valid/invalid data
├── email_validation.py # Email extraction and validation
├── phone_validation.py # Phone number extraction and validation
├── creditcard_validation.py # Credit card extraction and validation
├── time_validation.py # Time extraction and validation
├── currency_validation.py # Currency extraction and validation
├── all_validations.py # Combined script for all data types 
└── README.md # This file

- Each module is **self-contained** for testing individual types.  
- `all_validations.py` runs all extraction/validation at once for convenience.

---

## Setup Instructions

1. **Clone the repository**:
```bash
git clone https://github.com/{YourUsername}/alu_regex-data-extraction-{YourUsername}.git
cd alu_regex-data-extraction-{YourUsername}
```
2. Ensure Python 3.x is installed:
```
python --version
```
3. Run individual validation scripts:
```
python email_validation.py
python phone_validation.py
python creditcard_validation.py
python time_validation.py
python currency_validation.py
```
Or run combined script:
```
python all_validations.py
```
The output will list all candidates from api_response.txt along with validation status.

Edge Case Handling
Emails: missing @, numeric-only usernames, invalid domains
Phones: dots, dashes, spaces, parentheses, country codes, invalid digits
Credit Cards: wrong length, repeated digits, invalid characters, issuer heuristics
Time: invalid hours/minutes, missing AM/PM, malformed separators
Currency: missing $, malformed decimals, incorrect comma placement

All errors provide descriptive messages, aiding debugging and validation.

GitHub Best Practices
Commits: Meaningful messages, frequent commits for each module.
Code Structure: Modular scripts per data type, reusable validation functions.
Documentation: Clear README, inline comments, edge-case explanations.

Notes
This project is implemented in Python 3.
Designed for educational and testing purposes; not production-grade for financial or personal data.
Encouraged to extend regex patterns or validations for more complex real-world data.

Author
Grace Njunge
African Leadership University
GitHub: https://github.com/G-Njunge
```
This `README.md` covers:

- **Project overview** and goals  
- **Detailed explanation of each validation module** (emails, phones, credit cards, times, currency)  
- **Repository structure** with clarity  
- **Setup instructions** for reproducibility  
- **Edge-case handling** (important for rubric points)  
- **GitHub best practices**  
- **Author info**
```



