import feedparser
import gspread

gc = gspread.service_account(filename='google_creds.json')

sh = gc.open("Explore_News_Beta_Staging").sheet1

rss_urls = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Education.xml",
    "https://www.the74million.org/feed/",
    "https://www.highereddive.com/feeds/news/",
    "https://www.k12dive.com/feeds/news/"
]

existing_urls = sh.col_values(2)

print("Starting...")

for url in rss_urls:
    feed = feedparser.parse(url)

    for entry in feed.entries:

        if entry.link not in existing_urls:

            sh.append_row([
                entry.title,
                entry.link,
                "",
                "",
                "Draft"
            ])

print("Done")