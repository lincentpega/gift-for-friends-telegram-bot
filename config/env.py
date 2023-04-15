import os

from dotenv import load_dotenv

load_dotenv()

pg_username = os.getenv('PG_USERNAME')
pg_password = os.getenv('PG_PASSWORD')
db_uri = os.getenv('DB_URI')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

bot_token = os.getenv('BOT_TOKEN')
provider_token = os.getenv('PROVIDER_TOKEN')
