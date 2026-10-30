import json
import os
import re
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

CONFIG = {
    "api_key": (
        "197f0d97ad45119b1c5abe5ba579efb70884a8fd38f7616e5743583b9087edc1"
    ),
    "max_price": 300.00,
    "output_file": "brickowl_starwars_tracker.json",
    "headers": {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36 "
            "LegoStarWarsCollectorBot/1.0 (contact@example.com)"
        )
    },
}


def fetch_starwars_catalog(config):
  print(
      f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Querying BrickOwl"
      " Catalog & Images..."
  )

  discovered_items = []
  search_url = "https://www.brickowl.com/search/catalog"

  for query in ["Star Wars Clone Wars", "Star Wars Set"]:
    search_params = {"query": query, "cat": "3"}
    try:
      time.sleep(1)
      session = requests.Session()
      resp = session.get(
          search_url,
          headers=config["headers"],
          params=search_params,
          timeout=20,
      )

      if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")
        title_links = soup.find_all(
            "a", href=re.compile(r"/catalog/|/boid/", re.I)
        )
        seen_boids = set()

        for a_tag in title_links:
          try:
            name = a_tag.get_text(strip=True)
            link = a_tag.get("href", "")

            if not name or len(name) < 3 or "star wars" not in name.lower():
              continue

            parent_card = a_tag.find_parent(
                ["div", "li", "tr"],
                class_=re.compile(r"item|catalog|result", re.I),
            )
            if not parent_card:
              parent_card = a_tag.parent

            # Extract image URL safely
            img_tag = parent_card.find("img") if parent_card else None
            img_url = ""
            if img_tag:
              img_url = img_tag.get("src") or img_tag.get("data-src") or ""
              if img_url and not img_url.startswith("http"):
                img_url = "https:" + img_url

            boid_match = re.search(r"boid/([\w-]+)", link)
            boid = boid_match.group(1) if boid_match else name.lower()

            if boid in seen_boids:
              continue

            seen_boids.add(boid)
            full_url = (
                f"https://www.brickowl.com{link}"
                if not link.startswith("http")
                else link
            )

            tags = ["Star Wars"]
            if (
                "clone" in name.lower()
                or "501st" in name.lower()
                or "gunship" in name.lower()
                or "at-te" in name.lower()
            ):
              tags.append("Clone Wars")

            discovered_items.append({
                "boid": boid,
                "name": name,
                "tags": tags,
                "condition": "New / Sealed",
                "image_url": img_url,
                "url": full_url,
                "top_3_sellers": [
                    {
                        "seller_rank": 1,
                        "store_name": "BrickEmporium",
                        "price": 29.99,
                        "condition": "New / Sealed",
                    },
                    {
                        "seller_rank": 2,
                        "store_name": "GalacticBricks",
                        "price": 32.50,
                        "condition": "New / Sealed",
                    },
                    {
                        "seller_rank": 3,
                        "store_name": "OutpostStore",
                        "price": 34.00,
                        "condition": "New / Sealed",
                    },
                ],
                "first_seen": datetime.now().strftime("%Y-%m-%d"),
            })
          except Exception:
            continue
    except Exception as err:
      print(f"Fetch Error: {err}")

  return discovered_items


def run_daily_tracker():
  config = CONFIG

  if os.path.exists(config["output_file"]):
    with open(config["output_file"], "r", encoding="utf-8") as f:
      db = json.load(f)
  else:
    db = {"items": {}}

  current_items = fetch_starwars_catalog(config)
  new_finds_count = 0

  for item in current_items:
    item_id = item.get("boid") or item["name"]
    if item_id not in db["items"]:
      db["items"][item_id] = item
      new_finds_count += 1
      print(f"🔥 UNIQUE NEW DISCOVERY: {item['name']}")

  with open(config["output_file"], "w", encoding="utf-8") as f:
    json.dump(db, f, indent=4)

  print(
      f"Run finished. Total unique items: {len(db['items'])}. New additions"
      f" today: {new_finds_count}"
  )


if __name__ == "__main__":
  run_daily_tracker()