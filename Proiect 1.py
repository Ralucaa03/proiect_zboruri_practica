import asyncio
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from random import uniform
from playwright.async_api import async_playwright

#aici am ce dest caut
DESTINATII = ["Roma", "Paris", "Londra", "Barcelona", "Milano"]

# buton pt acc cookie
async def accepta_cookie(page):
    try:
        await page.locator("button:has-text('Permite toate')").click()
        await asyncio.sleep(1)
    except:
        print("Cookie-urile nu au apărut sau au fost deja acceptate.")

# caut zbor din Buc pt ziua de maine
async def cauta_zbor(page, oras_destinatie):
    ziua_maine = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")

    try:
        await page.locator("input[placeholder='De unde pleci?']").fill("București")
        element_lista_zboruri = await page.query_selector('div[data-test="flight-select-flight-list"]')
        lista_zboruri = await element_lista_zboruri.query_selector_all('div[data-test="flight-select-flight"]')
        for zbor in lista_zboruri:
            text = await
        await page.wait_for_selector(".autocomplete-suggestion")
        await page.locator(".autocomplete-suggestion").first.click()

        await page.locator("input[placeholder='Orașe sau țări']").fill(oras_destinatie)
        await page.wait_for_selector(".autocomplete-suggestion")
        await page.locator(".autocomplete-suggestion").first.click()

        await page.locator("input[name='departureDate']").fill(ziua_maine)
        await page.locator("button:has-text('Caută')").click()
        await asyncio.sleep(5)

        companie = await page.locator(".flight-company").first.text_content()
        pret_text = await page.locator(".flight-price").first.text_content()
        pret = float(pret_text.replace("€", "").strip())

        ora_plecare = await page.locator(".flight-departure").first.text_content()
        ora_sosire = await page.locator(".flight-arrival").first.text_content()
        durata_minute = 150  #aici nu stiu ce sa pun

    except Exception as e:
        print(f" Nu am putut extrage date pentru {oras_destinatie}. Simulez...")
        print(f"Found {e}")
        companie = "Simulat"
        pret = round(uniform(50, 200), 2)
        ora_plecare = "08:00"
        ora_sosire = "10:30"
        durata_minute = 150

    timestamp = datetime.now(tz=timezone.utc)
    pret_pe_minut = round(pret / durata_minute, 2)

    return {
        "id_zbor": f"Bucuresti-{oras_destinatie}-{ziua_maine}",
        "oras_destinatie": oras_destinatie,
        "companie": companie,
        "pret": pret,
        "durata_minute": durata_minute,
        "pret_pe_minut": pret_pe_minut,
        "timestamp": timestamp,
    }

# mongo
async def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["proiect_zboruri"]
    colectie = db["preturi_zbor"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://m.vola.ro/flight_search?from=AIRPORT:OTP&to=AIRPORT:CLJ&dd=2025-05-23&ad=1&ow=1")
        await accepta_cookie(page)

        toate_zborurile = []

        for destinatie in DESTINATII:
            zbor = await cauta_zbor(page, destinatie)
            colectie.insert_one(zbor)
            toate_zborurile.append(zbor)
            print(f" Zbor salvat către {destinatie}: {zbor['pret']} EUR")

        await browser.close()

        # afis zborul cel mai ieftin
        cel_mai_ieftin = min(toate_zborurile, key=lambda z: z["pret_pe_minut"])
        print("\n  Cel mai ieftin zbor per minut este:")
        print(cel_mai_ieftin)


asyncio.run(main())
