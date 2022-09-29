
from scraper import EpicWarScraper
from store import EpicWarStore
import psycopg2

db_connection = psycopg2.connect(dbname="pet2", user="postgres", password="123456789")
my_store = EpicWarStore(db_connection)
my_scraper = EpicWarScraper(my_store)
my_scraper.start()
db_connection.close()