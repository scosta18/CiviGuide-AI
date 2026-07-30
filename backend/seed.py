from app.pipeline.crawler import crawl_and_index

SEED_URLS = [
    "https://dhs.maryland.gov/supplemental-nutrition-assistance-program/",
    "https://dhs.maryland.gov/supplemental-nutrition-assistance-program/eligibility-rules/",
    "https://dhs.maryland.gov/supplemental-nutrition-assistance-program/applying-for-the-food-supplement-program/",
    "https://dhs.maryland.gov/important-changes-snap-benefits/",
]

if __name__ == "__main__":
    for url in SEED_URLS:
        print(crawl_and_index(url))