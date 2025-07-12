import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")


async def get_friends(steam_id: str):
    url = "https://api.steampowered.com/ISteamUser/GetFriendList/v1/"
    params = {"key": STEAM_API_KEY, "steamid": steam_id, "relationship": "friend"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            return [f["steamid"] for f in data.get("friendslist", {}).get("friends", [])]

async def get_player_statuses(steam_ids: list[str]):
    ids = ",".join(steam_ids)
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {"key": STEAM_API_KEY, "steamids": ids}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            return data.get("response", {}).get("players", [])

async def get_player_summary(steam_id: str) -> dict | None:
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {"key": STEAM_API_KEY, "steamids": steam_id}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            players = data.get("response", {}).get("players", [])
            return players[0] if players else None
