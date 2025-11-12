"""Simple smoke test for the PrayerWall backend.

Usage:
  python test_api.py

It will:
 - request a token for admin credentials (configurable via env vars)
 - submit a public prayer (with prayerRequest as a string)
 - fetch the prayer wall and verify the prayer appears

Configure via environment variables:
 - BASE_URL (default: http://127.0.0.1:8000)
 - USERNAME (default: admin@prayerwall.com)
 - PASSWORD (default: Prayer123!)

This file is intended to be run locally while the backend server is running.
"""

import os
import sys
import time
import requests
import argparse


BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
USERNAME = os.environ.get("USERNAME", "admin@prayerwall.com")
PASSWORD = os.environ.get("PASSWORD", "Prayer123!")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Smoke test for PrayerWall backend")
    parser.add_argument("--base-url", default=BASE_URL,
                        help="Backend base URL")
    parser.add_argument("--username", default=USERNAME, help="Admin username")
    parser.add_argument("--password", default=PASSWORD, help="Admin password")
    return parser.parse_args()


def get_token(base_url: str, username: str, password: str):
    url = f"{base_url}/auth/token"
    data = {"username": username, "password": password}
    print(f"Requesting token for {username}...")
    r = requests.post(url, data=data)
    r.raise_for_status()
    j = r.json()
    print("Token received")
    return j["access_token"]


def submit_prayer(base_url: str, token: str, title: str, body: str):
    url = f"{base_url}/prayers/submit"
    payload = {
        "prayerRequest": body,
        "name": "Auto Tester",
        "phoneNumber": None,
        "keepAnonymous": False,
    }
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}
    print("Submitting prayer...")
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    j = r.json()
    print("Prayer submitted:", j)
    return j


def fetch_wall(base_url: str):
    url = f"{base_url}/prayers/wall"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def main():
    args = parse_args()
    try:
        token = get_token(args.base_url, args.username, args.password)
    except Exception as e:
        print("Failed to get token:", e)
        sys.exit(2)

    title = "Automated test prayer"
    body = f"Automated test prayer from test_api.py at {time.asctime()}"

    try:
        submit_prayer(args.base_url, token, title, body)
    except Exception as e:
        print("Failed to submit prayer:", e)
        sys.exit(3)

    # Wait briefly for DB write (if necessary)
    time.sleep(1)

    try:
        wall = fetch_wall(args.base_url)
        print("Fetched prayer wall, total items:", wall.get("total"))
        # naive check: search for our body in any item
        found = False
        for item in wall.get("items", []):
            if body in (item.get("content") or item.get("title") or ""):
                found = True
                print("Found submitted prayer in wall (id=", item.get("id"), ")")
                break
        if not found:
            print(
                "Submitted prayer not found in wall results. You may need to check moderation filters or DB.")
            sys.exit(4)
    except Exception as e:
        print("Failed to fetch wall:", e)
        sys.exit(5)

    print("Smoke test completed successfully.")


if __name__ == "__main__":
    main()
