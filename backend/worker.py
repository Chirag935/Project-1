import asyncio
from pathlib import Path
import json
from analysis import analyze_sun_shadow
from main import broadcast
from ingest import ingest_loop, OUTPUT_DIR

async def analysis_loop():
    processed = set()
    while True:
        for img_path in Path(OUTPUT_DIR).glob("*.jpg"):
            if img_path in processed:
                continue
            try:
                result = analyze_sun_shadow(str(img_path))
                payload = {
                    "filename": img_path.name,
                    **result,
                }
                await broadcast(payload)
                processed.add(img_path)
            except Exception as e:
                print(f"Analysis error {img_path}: {e}")
        await asyncio.sleep(5)

async def main():
    await asyncio.gather(
        ingest_loop(),
        analysis_loop(),
    )

if __name__ == "__main__":
    asyncio.run(main())