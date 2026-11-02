import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path


STEAM_ID = os.environ.get("STEAM_ID")
API_KEY = os.environ.get("STEAM_API_KEY")
OUTPUT = Path(__file__).with_name("games.csv")


def main():
    if not API_KEY:
        raise SystemExit("Missing STEAM_API_KEY. Add it in repository Actions secrets.")
    if not STEAM_ID:
        raise SystemExit("Missing STEAM_ID. Add it in repository Actions secrets.")

    query = urllib.parse.urlencode({
        "key": API_KEY,
        "steamid": STEAM_ID,
        "include_appinfo": 1,
        "include_played_free_games": 1,
        "format": "json",
    })
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": "steam-games-pages/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)

    games = payload.get("response", {}).get("games", [])
    if not games:
        raise SystemExit("Steam returned no games; leaving the existing CSV unchanged. Check profile privacy and SteamID.")

    games.sort(key=lambda game: (-int(game.get("playtime_forever", 0)), game.get("name", "").casefold()))
    with OUTPUT.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Game", "Hours Played", "App ID", "Icon URL"])
        for game in games:
            appid = int(game["appid"])
            icon_hash = game.get("img_icon_url", "")
            icon_url = (
                f"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{icon_hash}.jpg"
                if icon_hash else ""
            )
            writer.writerow([
                game.get("name") or f"Steam App {appid}",
                f"{int(game.get('playtime_forever', 0)) / 60:.1f}",
                appid,
                icon_url,
            ])

    print(f"Updated {len(games)} games in {OUTPUT.name}.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Steam sync failed: {error}", file=sys.stderr)
        raise
