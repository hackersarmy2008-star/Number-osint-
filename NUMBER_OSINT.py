#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phone Number OSINT (Ethical, Passive)
-------------------------------------
Features:
- Validates number and extracts metadata locally (country, type, carrier, timezones).
- Optional enrichment with NumVerify API (if NUMVERIFY_API_KEY is set).
- Optional Aadhar info lookup with third-party API (if AADHAR_API_KEY is set).
- Generates link pack (Google dorks & major platforms) for manual review.
"""

import sys, os, time
import phonenumbers
import argparse
import datetime
import requests
from phonenumbers import carrier, geocoder, timezone

# ---------------- API KEYS ----------------
# Load from environment variables
NUMVERIFY_API_KEY = "84a23c87af2e09a3e1bb3a2fc05a10ab"
AADHAR_API_KEY = os.getenv("AADHAR_API_KEY")

# ------------- Flash Print -------------
def flash_print(text, delay=0.002):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ------------- Banner -------------
def print_banner():
    banner = r"""
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::



                        .............. ..
                   .  ...'',.'..,.''.......'',....
                   .  ... .,''..'.'....... ..,',....
                   .........'.',........,....,.....
                  .. ..:,.':'...;........'',;'..':''.
              '......,.,'.';'...,.,',..';,.',....:' .
            ..     . ....'';....,.'';...     ....;''.
                 .       '',....'...     ............
              ....'..     .,.'..,.    ......',.''....
              .....,....   '''..,.......'....,.'''...
              .......'...  ...'',......... .....','..
                        .   . ..'''..           ...,.
             ....',....      .,;;,..,............:,,.
             ... ,;;.,.     ..,;...........',;,..:'..
          ..;..'.,;....     ..,;,.,,...';,.',..;,:,,.
           .,....''...      ..','',',....'...'',',...
            ..'....         '..''...'...'''..,''''...
              .             ............,'...'......
              .              ... ...,'..,... .'.....
             .                    ........   ,'.....
              .  .           ...    .      .;......
                   . .... .............';,;,'....;
                ..     .. .,,;..,.,,.'.......;','
                  ..            ..'.....,......
                   ..     ..   ...'''''.,.....
                       . ...    ..'''...'...
                        ....    ..''.......
                          ..    . ''.....
                           .     ......
                           .    .....
                                                    ......
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
            Phone Number OSINT Tool
            Author: cyber-23priyanshu
    """
    flash_print(banner, delay=0.005)

# ------------- Footer -------------
def print_footer():
    flash_print("\n[+] Scan complete. Stay ethical! ⚡\n", delay=0.002)

# ------------- Local Metadata Lookup -------------
def local_metadata(num_obj):
    return {
        "valid": phonenumbers.is_valid_number(num_obj),
        "possible": phonenumbers.is_possible_number(num_obj),
        "type": phonenumbers.number_type(num_obj),
        "region_code": phonenumbers.region_code_for_number(num_obj),
        "country": geocoder.description_for_number(num_obj, "en"),
        "carrier": carrier.name_for_number(num_obj, "en"),
        "timezones": timezone.time_zones_for_number(num_obj),
        "formats": {
            "E164": phonenumbers.format_number(num_obj, phonenumbers.PhoneNumberFormat.E164),
            "International": phonenumbers.format_number(num_obj, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "National": phonenumbers.format_number(num_obj, phonenumbers.PhoneNumberFormat.NATIONAL)
        }
    }

# ------------- NumVerify Lookup -------------
def numverify_lookup(number):
    if not NUMVERIFY_API_KEY:
        return None
    try:
        url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={number}"
        resp = requests.get(url, timeout=10).json()
        if "error" in resp:
            return {"error": resp["error"].get("info", "API Error")}
        return {
            "valid": resp.get("valid"),
            "number": resp.get("number"),
            "local_format": resp.get("local_format"),
            "international_format": resp.get("international_format"),
            "country_code": resp.get("country_code"),
            "country_name": resp.get("country_name"),
            "location": resp.get("location"),
            "carrier": resp.get("carrier"),
            "line_type": resp.get("line_type")
        }
    except Exception as e:
        return {"error": str(e)}

# ------------- Aadhar Lookup (Mock) -------------
def aadhar_lookup(number):
    if not AADHAR_API_KEY:
        return None
    return {"aadhar_linked": False, "notes": "Demo only"}

# ------------- Link Pack -------------
def build_link_pack(e164, national):
    q = national
    return {
        "Google Search": f"https://www.google.com/search?q={q}",
        "Truecaller": f"https://www.truecaller.com/search/in/{q}",
        "Facebook": f"https://www.facebook.com/search/top?q={q}",
        "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={q}",
        "Instagram": f"https://www.instagram.com/{q}",
    }

# ------------- Report Builder -------------
def build_report_md(number, local, numv, aadhar, links):
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    report = f"""
# Phone OSINT Report
- **Input:** `{number}`
- **Generated:** {now}

## Validation & Metadata (Local)
- **Valid:** {local['valid']}
- **Possible:** {local['possible']}
- **Type:** {local['type']}
- **Region Code:** {local['region_code']}
- **Country/Area:** {local['country']}
- **Carrier (DB):** {local['carrier']}
- **Time Zone(s):** {", ".join(local['timezones'])}
- **Format E.164:** {local['formats']['E164']}
- **Format Intl.:** {local['formats']['International']}
- **Format Nat.:** {local['formats']['National']}

## NumVerify API
"""
    if numv:
        if "error" in numv:
            report += f"- Error: {numv['error']}\n"
        else:
            report += f"""
- **Valid:** {numv.get('valid')}
- **Number:** {numv.get('number')}
- **Local Format:** {numv.get('local_format')}
- **International Format:** {numv.get('international_format')}
- **Country Code:** {numv.get('country_code')}
- **Country Name:** {numv.get('country_name')}
- **Location:** {numv.get('location')}
- **Carrier (API):** {numv.get('carrier')}
- **Line Type:** {numv.get('line_type')}
"""
    else:
        report += "Skipped (no API key)\n"

    report += "\n## Aadhaar Lookup\n"
    if aadhar:
        report += f"- {aadhar}\n"
    else:
        report += "Skipped (no API key)\n"

    report += "\n## Useful Links\n"
    for k, v in links.items():
        report += f"- [{k}]({v})\n"

    return report

# ------------- Main -------------
def main():
    print_banner()

    # Interactive input
    country_code = input("Enter country code (e.g. +91 or 91): ").strip().lstrip("+")
    number = input("Enter phone number (without country code): ").strip()

    full_number = f"+{country_code}{number}"

    try:
        num_obj = phonenumbers.parse(full_number, None)
    except Exception as e:
        sys.exit(f"[!] Error parsing phone number: {e}")

    local = local_metadata(num_obj)
    e164 = local.get("formats", {}).get("E164", full_number)
    national = local.get("formats", {}).get("National", number)

    numv = numverify_lookup(e164)
    aadhar = aadhar_lookup(e164)
    links = build_link_pack(e164, national)

    report = build_report_md(full_number, local, numv, aadhar, links)
    flash_print(report, delay=0.0015)

    print_footer()

if __name__ == "__main__":
    main()