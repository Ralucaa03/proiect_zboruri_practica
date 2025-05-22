import asyncio
from pymongo import MongoClient
from datetime import datetime, timezone
from random import uniform
from playwright.async_api import async_playwright

async def main():

    client = MongoClient("mongodb://localhost:27017/")
    db = client["proiect_zboruri"]


    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()


        await page.goto("https://m.vola.ro/")
        await asyncio.sleep(1)


        id_zbor = "FR123"
        id_platforma = "vola"
        pret = round(uniform(40, 100), 2)
        durata = 150
        pret_pe_minut = round(pret / durata, 2)
        timestamp = datetime.now(tz=timezone.utc)
        ora_extragere = timestamp.strftime("%H:%M")


        db.preturi_zbor.insert_one({
            "id_zbor": id_zbor,
            "id_platforma": id_platforma,
            "pret": pret,
            "moneda": "EUR",
            "timestamp": timestamp,
            "pret_pe_minut": pret_pe_minut,
            "ora_extragere": ora_extragere
        })

        await browser.close()
        print("✅ Pret salvat în MongoDB:", pret, "EUR")


asyncio.run(main())

