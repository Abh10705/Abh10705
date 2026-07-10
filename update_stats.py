import re
import os
import requests

# Get your GitHub statistics via the public API
username = os.environ.get("GITHUB_REPOSITORY").split("/")[0]

# Fetch user data
user_data = requests.get(f"https://api.github.com/users/{username}").json()
repos_count = user_data.get("public_repos", 0)

# Fetch star count
stars_data = requests.get(f"https://api.github.com/users/{username}/starred").json()
stars_count = len(stars_data)

# For commits, using a close approximation from public events or hard API count
# To keep this script lightweight and fast, we'll fetch your public repo events
events_data = requests.get(f"https://api.github.com/users/{username}/events/public").json()
commits_count = sum(1 for event in events_data if event.get("type") == "PushEvent")

# Read the current README
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

# Dynamically replace the blank spaces with real fetched data
readme = re.sub(r"(Repos:\s*)\d*", f"Repos: {repos_count}", readme)
readme = re.sub(r"(Commits:\s*)\d*", f"Commits: {commits_count}", readme)
readme = re.sub(r"(Stars:\s*)\d*", f"Stars: {stars_count}", readme)

# Save the updated README
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
