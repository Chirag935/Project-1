import asyncio
import aiohttp
from typing import List
from datetime import datetime
from pathlib import Path

WEBCAM_LIST: List[str] = [
    # replace with actual webcam image URLs
    "https://example.com/webcam1.jpg",
    "https://example.com/webcam2.jpg",
]

OUTPUT_DIR = Path("/workspace/data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FETCH_INTERVAL = 60  # seconds

async def fetch_image(session: aiohttp.ClientSession, url: str):
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                img_bytes = await resp.read()
                timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
                filename = OUTPUT_DIR / f"{url.split('/')[-1].split('.')[0]}_{timestamp}.jpg"
                filename.write_bytes(img_bytes)
                return str(filename)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

async def ingest_loop():
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [fetch_image(session, url) for url in WEBCAM_LIST]
            await asyncio.gather(*tasks)
            await asyncio.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    asyncio.run(ingest_loop())