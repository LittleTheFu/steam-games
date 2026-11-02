import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path


STEAM_ID = os.environ.get("STEAM_ID")
API_KEY = os.environ.get("STEAM_API_KEY")
ROOT = Path(__file__).parent
OUTPUT = ROOT / "games.csv"
COVERS = ROOT / "covers"


def download_cover(game):
    appid = int(game["appid"])
    destination = COVERS / f"{appid}.jpg"
    if destination.exists() and destination.stat().st_size > 0:
        return f"covers/{appid}.jpg"

    icon_hash = game.get("img_icon_url", "")
    urls = [
        f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/library_600x900.jpg",
        f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg",
    ]
    if icon_hash:
        urls.append(f"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{icon_hash}.jpg")

    for url in urls:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "steam-games-pages/1.0"})
            with urllib.request.urlopen(request, timeout=20) as response:
                data = response.read()
            if len(data) > 1000:
                destination.write_bytes(data)
                return f"covers/{appid}.jpg"
        except Exception:
            continue
    return ""


def main():
    if not API_KEY:
        raise SystemExit("Missing STEAM_API_KEY. Add it in repository Actions secrets.")
    if not STEAM_ID:
        raise SystemExit("Missing STEAM_ID. Add it in repository Actions secrets.")

    COVERS.mkdir(exist_ok=True)
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
        writer.writerow(["Game", "Hours Played", "App ID", "Icon URL", "Cover"])
        for game in games:
            appid = int(game["appid"])
            icon_hash = game.get("img_icon_url", "")
            icon_url = (
                f"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{icon_hash}.jpg"
                if icon_hash else ""
            )
            cover = download_cover(game)
            writer.writerow([
                game.get("name") or f"Steam App {appid}",
                f"{int(game.get('playtime_forever', 0)) / 60:.1f}",
                appid,
                icon_url,
                cover,
            ])

    print(f"Updated {len(games)} games and downloaded missing covers.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Steam sync failed: {error}", file=sys.stderr)
        raise
