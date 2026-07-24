import json, os, requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GITHUB_USERNAME", "Zaryab-khanzk")

def fetch_contributions():
    url = f"https://github.com/users/{USERNAME}/contributions"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    days = []
    total_count = 0
    for cell in soup.find_all(["td", "rect"], class_="ContributionCalendar-day"):
        date, level = cell.get("data-date"), cell.get("data-level", "0")
        if date:
            days.append({"date": date, "level": int(level)})
            total_count += int(level)
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump({"total": total_count, "days": days}, f, indent=2)
    print("Saved contribution data!")

if __name__ == "__main__":
    fetch_contributions()
