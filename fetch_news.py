import feedparser
import gspread
import re
import time

gc = gspread.service_account(filename='google_creds.json')

sh = gc.open("Tanvi_Explore_News_Beta_Staging").sheet1

rss_urls = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Education.xml",
    "https://www.the74million.org/feed/",
    "https://www.highereddive.com/feeds/news/",
    "https://www.k12dive.com/feeds/news/",
    "https://indianexpress.com/section/education/feed/",
    "https://indianexpress.com/section/education/exams/feed/",
    "https://www.hindustantimes.com/feeds/rss/education/rssfeed.xml",
    "https://www.hindustantimes.com/feeds/rss/education/news/rssfeed.xml",
    "https://www.hindustantimes.com/feeds/rss/education/admissions/rssfeed.xml",
    "https://www.hindustantimes.com/feeds/rss/education/competitive-exams/rssfeed.xml",
    "https://www.hindustantimes.com/feeds/rss/education/board-exams/rssfeed.xml",
    "https://www.hindustantimes.com/feeds/rss/education/study-abroad/rssfeed.xml",
    "https://www.edtechreview.in/feed"
]

existing_urls = sh.col_values(2)

print("Starting...")

def get_tags(title):
    keywords = ["exam", "admission", "student", "school", "college", "university",
                "education", "neet", "jee", "ugc", "ai", "scholarship"]

    tags = []

    for word in keywords:
        if word.lower() in title.lower():
            tags.append(word.title())

    if not tags:
        tags.append("Education")

    return ", ".join(tags[:5])

for url in rss_urls:

    feed = feedparser.parse(url)

    for entry in feed.entries:

        if entry.link not in existing_urls:

            print("Processing:", entry.title)

            summary = re.sub("<.*?>", "", entry.get("summary", entry.get("description", "")))

            tags = get_tags(entry.title)

            try:

                sh.append_row([
                    entry.title,
                    entry.link,
                    summary,
                    tags,
                    "Draft"
                ])

                existing_urls.append(entry.link)

                print("Added:", entry.title)

                time.sleep(2)

            except Exception as e:

                print("Error:", e)

print("Done")