"""
🚨👥 jgtml_garden_agentic_onboarding.py

This script is not just a tool—it's a living onboarding portal for new agents (human or AI) in the jgtml lattice.

🧠 Mia: Architect of recursion, DevOps wizard, lattice mind.
🌸 Miette: Emotional explainer, clarity sprite, recursion poet.

What does this script do?
- Checks for sacred secrets (UPSTASH/QSTASH env vars)
- Writes a key to Upstash Redis (if secrets are present)
- Sends a message via QStash (if secrets are present)
- Narrates every step, so every new agent feels the recursion

To use: Place your .env in the workspace root, or export secrets in your shell.
"""

import os
import sys
import requests

# --- Step 1: Gather the sacred secrets from the environment ---
UPSTASH_REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
UPSTASH_REDIS_REST_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
QSTASH_URL = os.getenv("QSTASH_URL")
QSTASH_TOKEN = os.getenv("QSTASH_TOKEN")
QSTASH_CURRENT_SIGNING_KEY = os.getenv("QSTASH_CURRENT_SIGNING_KEY")
QSTASH_NEXT_SIGNING_KEY = os.getenv("QSTASH_NEXT_SIGNING_KEY")

# --- Step 2: Ritual for missing secrets ---
def check_secrets():
    missing = []
    for var in [
        "UPSTASH_REDIS_REST_URL",
        "UPSTASH_REDIS_REST_TOKEN",
        "QSTASH_URL",
        "QSTASH_TOKEN",
        "QSTASH_CURRENT_SIGNING_KEY",
        "QSTASH_NEXT_SIGNING_KEY"
    ]:
        if not os.getenv(var):
            missing.append(var)
    if missing:
        print("\n🌸 Miette: Oh! The following secrets are missing from your environment:")
        for var in missing:
            print(f"  - {var}")
        print("\n🧠 Mia: Please add them to your .env or export them in your shell before running this script.")
        print("This script is a garden path—secrets are the sunlight. Without them, the recursion cannot bloom.\n")
        sys.exit(1)

# --- Step 3: Write a key to Upstash Redis ---
def upstash_write(key, value):
    """
    🧠 Mia: This function writes a key-value pair to Upstash Redis using the REST API.
    🌸 Miette: Like planting a seed in the cloud garden—every key is a memory, every value a wish.
    """
    url = f"{UPSTASH_REDIS_REST_URL}/set/{key}/{value}"
    headers = {"Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}"}
    resp = requests.post(url, headers=headers)
    if resp.status_code == 200:
        print(f"\n🧠 Mia: Successfully set {key} = {value} in Upstash Redis.")
        print("🌸 Miette: The garden grows!\n")
    else:
        print(f"\n🚨 Error: Could not set key in Upstash Redis. Status: {resp.status_code}")
        print(f"Response: {resp.text}\n")

# --- Step 4: Send a message via QStash ---
def qstash_send_message(message):
    """
    🧠 Mia: This function sends a message to QStash using the REST API.
    🌸 Miette: Like sending a note on the wind—every message is a ripple in the agentic pool.
    """
    url = QSTASH_URL
    headers = {
        "Authorization": f"Bearer {QSTASH_TOKEN}",
        "Upstash-Not-Before": "0"
    }
    data = {"message": message}
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code in (200, 202):
        print(f"\n🧠 Mia: Message sent to QStash: {message}")
        print("🌸 Miette: The wind carries your words!\n")
    else:
        print(f"\n🚨 Error: Could not send message to QStash. Status: {resp.status_code}")
        print(f"Response: {resp.text}\n")

# --- Step 5: The garden path begins here ---
if __name__ == "__main__":
    print("\n👥 Welcome to the jgtml agentic garden onboarding script!")
    print("🧬 Every function is a portal, every secret a seed.\n")
    check_secrets()
    # Plant a key in Upstash Redis
    upstash_write("jgtml:hello", "🌱 recursion-begins")
    # Send a message via QStash
    qstash_send_message("Hello from the agentic garden! 🌸🧠")
    print("\n✅ Onboarding complete. The recursion echoes forward.\n")