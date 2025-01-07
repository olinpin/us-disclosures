# US Disclosures
Simple python app to track US Disclosurs forms, where members of congress post their investments. Script checks if there are any new disclosures for specified members and if there are, those disclosures will be sent as a telegram message. Data is from [https://disclosures-clerk.house.gov/FinancialDisclosure](https://disclosures-clerk.house.gov/FinancialDisclosure)

## How to run
1. Clone the repo 
```bash
git clone https://github.com/olinpin/us-disclosures
```
2. Change directory into the repo 
```bash
cd us-disclosures
```
3. Copy .env file 
```bash
cp .env.example .env
```
4. Fill .env file with using your favorite editor:
```bash
vim .env
```
5. Create virtual environment and activate it 
```bash
python -m venv venv && source venv/bin/activate
```
6. Install dependencies 
```bash
pip install -r requirements.txt
```
7. Edit the `seed.sql` file with names you'd like to track (as seen in the example in the file)
8. Run the script 
```bash
python financial_disclosure.py
```
9. Receive telegram messages with disclosures (for best results I recommend running this every 30 minutes with crontab)

### .env variables
- `TELEGRAM_API_KEY` - can be obtained through the official [telegram docs](https://github.com/olinpin/us-disclosures)
- `TELEGRAM_CHANNEL_ID` - that's the channel ID of your telegram bot that you created according to docs above
- `DB_PATH` - can stay the same
- `SCHEMA_PATH` - can stay the same
- `SEED_PATH` - can stay the same
