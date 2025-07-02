import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

# Setup sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def fetch_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={API_KEY}&currencies=BTC"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("Failed to fetch news:", response.text)
        return []

def analyze_sentiment(news_items):
    pump = []
    dump = []

    for item in news_items:
        title = item.get("title", "")
        summary = item.get("domain", "")
        content = title + " " + summary
        score = analyzer.polarity_scores(content)

        print(f"\n📰 Title: {title}")
        print(f"Sentiment Score: {score}")

        if score["compound"] >= 0.4:
            pump.append(title)
        elif score["compound"] <= -0.4:
            dump.append(title)

    return pump, dump

def main():
    print("🔍 Scanning news for BTC market-moving sentiment...\n")

    news = fetch_news()
    if not news:
        print("No news found.")
        return

    pump, dump = analyze_sentiment(news)

    print("\n📈 Possible PUMP News:")
    for title in pump:
        print(" +", title)

    print("\n📉 Possible DUMP News:")
    for title in dump:
        print(" -", title)

# Run every 5 minutes
if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)  # 5 minutes
