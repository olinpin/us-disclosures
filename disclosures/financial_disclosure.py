import requests
from bs4 import BeautifulSoup
import os
from util.telegram_bot import Telegram
from util.db import DB
from dotenv import load_dotenv
import asyncio
import datetime

load_dotenv()


class Disclosures:
    def __init__(
        self, telegram_api_key, telegram_channel, db_name, schema_path, seed_path
    ):
        self.telegram = Telegram(telegram_api_key, telegram_channel)
        self.db = DB(db_name, schema_path, seed_path)

    async def send_message(self, message, return_value=True):
        try:
            await self.telegram.send_message(message)
            return return_value
        except Exception as e:
            self.log(f"Error sending message: {e}, message: {message}, return_value: {return_value}")
            return False

    def getDocuments(self, name="pelosi"):
        disclosures_url = "https://disclosures-clerk.house.gov"
        data = {"LastName": name}
        response = requests.post(
            f"{disclosures_url}/FinancialDisclosure/ViewMemberSearchResult", data=data
        )

        parsed_html = BeautifulSoup(response.text, "html.parser")
        fillings = parsed_html.find_all("tr", attrs={"role": "row"})
        fillings.pop(0)

        # sort fillings by year
        fillings.sort(
            key=lambda x: int(
                x.find_all("td", attrs={"data-label": "Filing Year"})[0].text
            )
        )
        documents = []
        for filling in fillings:
            year = self.formatString(
                filling.find_all("td", attrs={"data-label": "Filing Year"})[0].text
            )
            name = self.formatString(
                filling.find_all("td", attrs={"data-label": "Name"})[0].text
            )
            filing = self.formatString(
                filling.find_all("td", attrs={"data-label": "Filing"})[0].text
            )
            url = f'{disclosures_url}/{filling.a.get("href")}'
            documents.append({"name": name, "year": year, "filing": filing, "url": url})

        return documents

    def formatString(self, text):
        # remove \n and \t
        text = text.replace("\n", " ").replace("\t", " ")
        # remove extra spaces
        text = " ".join(text.split())
        return text

    def prepareValues(self, documents):
        already_inserted = self.db.query("SELECT link FROM disclosures;")
        already_inserted = [x[0] for x in already_inserted]
        values = []
        for member_id, d in documents.items():
            for document in d:
                if document["url"] not in already_inserted:
                    values.append(
                        (
                            member_id,
                            int(document["year"]),
                            document["filing"],
                            document["url"],
                        )
                    )

        return values

    def insertDisclosures(self, values):
        self.db.insertDisclosures(values)

    async def run(self):
        members = self.db.query("SELECT * FROM members;")
        documents = {}
        for id, name in members:
            documents[id] = self.getDocuments(name)
        values = self.prepareValues(documents)
        tasks = []
        sent = []
        for v in values:
            message = f"New disclosure from {[name for id, name in members if id == v[0]][0]} for the year {v[1]}. {v[2]} {v[3]}"
            tasks.append(asyncio.create_task(self.send_message(message, v)))
            await asyncio.sleep(0.2)

        results = await asyncio.gather(*tasks)
        sent = [r for r in results if r]

        self.insertDisclosures(sent)

        self.log(
            f"Sent {len(sent)} disclosures. Inserted {len(sent)} disclosures. Total disclosures {len(values)}"
        )

    def log(self, message):
        print(f"{datetime.datetime.now()} - {message}")


d = Disclosures(
    os.getenv("TELEGRAM_API_KEY"),
    os.getenv("TELEGRAM_CHANNEL_ID"),
    os.getenv("DB_PATH"),
    os.getenv("SCHEMA_PATH"),
    os.getenv("SEED_PATH"),
)
try:
    asyncio.run(d.run())
except Exception as e:
    d.log(f"Error while running: {e}")
