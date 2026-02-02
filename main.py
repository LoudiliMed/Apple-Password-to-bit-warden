f v is not None and str(v).strip() != "":
                return str(v).strip()
                return ""


            def guess_name(title: str, url: str) -> str:
                    t = (title or "").strip()
                        if t:
                                    return t
                                    u = (url or "").strip()
                                        if not u:
                                                    return ""
                                                    try:
                                                                p = urlparse(u if "://" in u else "https://" + u)
                                                                        host = (p.hostname or "").strip()
                                                                                return host or u
                                                                                except Exception:
                                                                                            return u


                                                                                        def build_field_map(headers: list[str]) -> dict[str, str]:
                                                                                                """
                                                                                                    Returns mapping from internal keys -> actual header name in the input CSV.
                                                                                                        internal keys: title,url,username,password,notes,totp,favorite,folder
                                                                                                            """
                                                                                                                # Common Apple / iCloud / Safari export variants (best-effort)
                                                                                                                    candidates = {
                                                                                                                                    "title": [
                                                                                                                                              #!/usr/bin/env python3
"""
Convert Apple Passwords / iCloud Passwords CSV export to Bitwarden CSV import.

Bitwarden CSV columns (required order):
folder,favorite,type,name,notes,fields,login_uri,login_username,login_password,login_totp

This script tries to auto-detect Apple/Safari/iCloud column names.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
from urllib.parse import urlparse

BW_HEADER = [
    "folder",
    "favorite",
    "type",
    "name",
    "notes",
    "fields",
    "login_uri",
    "login_username",
    "login_password",
    "login_totp",
]


def norm(s: str) -> str:
    return re.sub(r"[\s_\-]+", "", (s or "").strip().lower())


def first_nonempty(*vals: str) -> str:
    for v in vals:
        i      "title",
            "name",
            "website name",
            "site",
            "service",
        ],
        "url": [
            "url",
            "website",
            "website url",
            "websiteurl",
            "uri",
            "link",
        ],
        "username": [
            "username",
            "user name",
            "login",
            "account",
            "email",
        ],
        "password": [
            "password",
            "pass",
            "passwd",
        ],
        "notes": [
            "notes",
            "note",
            "comments",
            "comment",
        ],
        "totp": [
            "otp",
            "totp",
            "one-time password",
            "onetimepassword",
            "verification code",
            "verificationcode",
            "2fa",
            "two-factor",
            "twofactor",
            "authenticator",
        ],
        "folder": [
            "folder",
            "group",
            "category",
            "collection",
        ],
        "favorite": [
            "favorite",
            "favourite",
            "star",
            "starred",
        ],
    }

    by_norm = {norm(h): h for h in headers}

    mapping: dict[str, str] = {}
    for key, names in candidates.items():
        for n in names:
            nn = norm(n)
            if nn in by_norm:
                mapping[key] = by_norm[nn]
                break

    # Extra heuristic: sometimes URL column is empty and the "Title" is the domain
    # (no action needed here; handled later by guess_name)

    return mapping


def to_bool_favorite(val: str) -> str:
    v = norm(val)
    if v in {"1", "true", "yes", "y", "on"}:
        return "1"
    return ""


def convert(in_path: str, out_path: str) -> None:
    # Apple exports are often UTF-8 with BOM
    with open(in_path, "r", encoding="utf-8-sig", newline="") as f_in:
        reader = csv.DictReader(f_in)
        if not reader.fieldnames:
            raise ValueError("Input CSV has no header row.")

        field_map = build_field_map(reader.fieldnames)

        with open(out_path, "w", encoding="utf-8", newline="") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=BW_HEADER, extrasaction="ignore")
            writer.writeheader()

            for row in reader:
                title = row.get(field_map.get("title", ""), "")
                url = row.get(field_map.get("url", ""), "")
                username = row.get(field_map.get("username", ""), "")
                password = row.get(field_map.get("password", ""), "")
                notes = row.get(field_map.get("notes", ""), "")
                totp = row.get(field_map.get("totp", ""), "")
                folder = row.get(field_map.get("folder", ""), "")

                favorite_raw = row.get(field_map.get("favorite", ""), "")
                favorite = to_bool_favorite(favorite_raw)

                # Some Apple exports put domain in Title and leave URL empty
                # Try to treat Title as URL if it looks like a domain/URL and URL is empty.
                if not url and title:
                    looks_like_url = bool(
                        re.match(r"^(https?://)", title.strip(), re.I)
                        or re.match(r"^[a-z0-9.-]+\.[a-z]{2,}(/.*)?$", title.strip(), re.I)
                    )
                    if looks_like_url:
                        url = title.strip()

                bw_row = {
                    "folder": (folder or "").strip(),
                    "favorite": favorite,
                    "type": "login",
                    "name": guess_name(title, url),
                    "notes": (notes or "").strip(),
                    "fields": "",  # custom fields not supported here
                    "login_uri": (url or "").strip(),
                    "login_username": (username or "").strip(),
                    "login_password": (password or "").strip(),
                    "login_totp": (totp or "").strip(),
                }
                # Skip completely empty rows
                if any(bw_row[k] for k in ["name", "login_uri", "login_username", "login_password", "notes"]):
                    writer.writerow(bw_row)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Convert Apple Passwords CSV export to Bitwarden CSV import format."
    )
    ap.add_argument("input_csv", help="Path to Apple/iCloud exported CSV (e.g., password.csv)")
    ap.add_argument(
        "-o",
        "--output",
        default="bitwarden.csv",
        help="Output CSV path (default: bitwarden.csv)",
    )
    args = ap.parse_args()

    in_path = args.input_csv
    out_path = args.output

    if not os.path.exists(in_path):
        raise SystemExit(f"Input file not found: {in_path}")

    convert(in_path, out_path)
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()

