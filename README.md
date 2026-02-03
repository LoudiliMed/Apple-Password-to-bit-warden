# Apple Passwords CSV → Bitwarden CSV

Converts an Apple Passwords / iCloud Passwords / Safari passwords CSV export into a Bitwarden-compatible CSV.

## Security note

This involves plaintext passwords in CSV files.  
Do not commit CSV exports to Git. This repo ignores `*.csv` by default.

## Files

- `apple_to_bitwarden.py` : converter script
- `requirements.txt` : no external deps
- `.gitignore` : prevents committing CSV/password files

## Requirements

- Python 3.9+ recommended (should work on most Python 3 versions)

## Usage

1) Export your passwords from Apple Passwords / iCloud Keychain as a CSV (you should end up with something like `password.csv`).

2) Put `Passwords.csv` in the same folder as the script.

3) Run:

```bash
python3 main.py Passwords.csv -o bitwarden.csv
```
