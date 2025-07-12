import re

import aiohttp
from bs4 import BeautifulSoup


async def get_free_steam_games() -> list[dict]:
    url = "https://store.steampowered.com/search/?filter=free&ndl=1"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "html.parser")
    games = []

    for result in soup.select(".search_result_row"):
        title = result.select_one(".title").text.strip()
        game_url = result["href"]

        # Витягнути appid із URL
        match = re.search(r"/app/(\d+)", game_url)
        appid = match.group(1) if match else None

        if appid:
            image = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg"
        else:
            image = result.select_one("img")["src"]

        games.append({
            "name": title,
            "url": game_url,
            "image": image
        })

    return games

import aiohttp

async def get_discounted_to_free_games():
    url = "https://store.steampowered.com/api/featuredcategories/?cc=us&l=en"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    discounted_games = []

    for game in data.get("specials", {}).get("items", []):
        original_price = game.get("original_price", 0)
        final_price = game.get("final_price", 0)
        if original_price > 0 and final_price == 0:
            discounted_games.append({
                "name": game["name"],
                "url": f"https://store.steampowered.com/app/{game['id']}",
                "image": game["header_image"]
            })

    return discounted_games
