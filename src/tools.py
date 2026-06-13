import requests
import urllib.parse
import xml.etree.ElementTree as ET

# ─────────────────────────────────────────
# TOOL 1: Wikipedia — Company Background
# ─────────────────────────────────────────
def search_company_info(company_name: str) -> str:
    """Get company overview from Wikipedia"""
    try:
        safe_name = urllib.parse.quote(company_name)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{safe_name}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            extract = data.get("extract", "")
            # Return first 1000 chars to keep it focused
            return extract[:1000] if extract else "No Wikipedia data found."

        # Fallback: Wikipedia search
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": company_name,
            "format": "json",
            "srlimit": 3
        }
        r = requests.get(search_url, params=params, timeout=10)
        results = r.json().get("query", {}).get("search", [])
        snippets = []
        for i in results:
            clean = i.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')
            snippets.append(f"- {i['title']}: {clean}")
        return "\n".join(snippets) if snippets else "No Wikipedia data found."
    except Exception as e:
        return f"Wikipedia error: {str(e)}"


# ─────────────────────────────────────────
# TOOL 2: Google News RSS — Latest Headlines
# ─────────────────────────────────────────
def search_company_news(company_name: str) -> str:
    """Fetch recent news headlines using Google News RSS"""
    try:
        safe_query = urllib.parse.quote(f"{company_name} business news")
        url = f"https://news.google.com/rss/search?q={safe_query}&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Google News unavailable."

        root = ET.fromstring(response.text)
        items = []
        for item in root.findall('./channel/item')[:6]:
            title = item.find('title').text
            pub_date = item.find('pubDate').text
            clean_date = pub_date.replace(" GMT", "") if pub_date else "Recent"
            items.append(f"- [{clean_date}] {title}")
        return "\n".join(items) if items else "No Google News found."
    except Exception as e:
        return f"Google News error: {str(e)}"


def get_ticker(company_name: str) -> str:
    """Dynamically fetch the stock ticker for a company using Yahoo Finance Search"""
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={urllib.parse.quote(company_name)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            quotes = data.get("quotes", [])
            if quotes:
                return quotes[0].get("symbol", "")
    except Exception:
        pass
    return ""

# ─────────────────────────────────────────
# TOOL 3: Yahoo Finance RSS — Stock & Financial News
# ─────────────────────────────────────────
def search_financial_info(company_name: str) -> str:
    """Fetch financial signals from Yahoo Finance RSS using dynamic ticker lookup"""
    try:
        ticker = get_ticker(company_name)
        
        # If we successfully found a ticker, hit Yahoo Finance properly
        if ticker:
            url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                items = []
                for item in root.findall('./channel/item')[:4]:
                    title = item.find('title')
                    if title is not None and title.text:
                        items.append(f"- [Yahoo Finance: {ticker}] {title.text}")
                if items:
                    return "\n".join(items)

        # Fallback: Google News financial search (if ticker fails or Yahoo is empty)
        safe_query2 = urllib.parse.quote(
            f"{company_name} revenue OR earnings OR stock OR valuation OR profit OR loss"
        )
        url2 = f"https://news.google.com/rss/search?q={safe_query2}&hl=en-US&gl=US&ceid=US:en"
        response2 = requests.get(url2, timeout=10)
        root2 = ET.fromstring(response2.text)
        items2 = []
        for item in root2.findall('./channel/item')[:4]:
            title = item.find('title').text
            items2.append(f"- [Google Finance] {title}")
        return "\n".join(items2) if items2 else "No financial data found."
    except Exception as e:
        return f"Financial data error: {str(e)}"

# ─────────────────────────────────────────
# TOOL 4: Bing News RSS — Additional Coverage
# ─────────────────────────────────────────
def search_bing_news(company_name: str) -> str:
    """Fetch additional news from Bing News RSS"""
    try:
        safe_query = urllib.parse.quote(f"{company_name} strategy announcement 2026")
        url = f"https://www.bing.com/news/search?q={safe_query}&format=rss"
        response = requests.get(
            url, timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        if response.status_code != 200:
            return "Bing News unavailable."

        root = ET.fromstring(response.text)
        items = []
        for item in root.findall('./channel/item')[:4]:
            title = item.find('title')
            if title is not None and title.text:
                items.append(f"- {title.text}")
        return "\n".join(items) if items else "No Bing News found."
    except Exception as e:
        return f"Bing News error: {str(e)}"


# ─────────────────────────────────────────
# TOOL 5: Reddit RSS — Public Sentiment
# ─────────────────────────────────────────
def search_reddit_sentiment(company_name: str) -> str:
    """Fetch Reddit public sentiment from relevant subreddits"""
    try:
        safe_query = urllib.parse.quote(company_name)
        url = f"https://www.reddit.com/search.json?q={safe_query}&sort=top&t=month&limit=5"
        response = requests.get(
            url, timeout=10,
            headers={"User-Agent": "BizIntelAgent/2.0"}
        )
        if response.status_code != 200:
            return "Reddit data unavailable."

        posts = response.json().get("data", {}).get("children", [])
        sentiments = []
        for post in posts[:4]:
            data = post.get("data", {})
            title = data.get("title", "")
            score = data.get("score", 0)
            subreddit = data.get("subreddit", "")
            if title:
                sentiments.append(f"- [r/{subreddit} | {score} upvotes] {title}")
        return "\n".join(sentiments) if sentiments else "No Reddit sentiment found."
    except Exception as e:
        return f"Reddit error: {str(e)}"


# ─────────────────────────────────────────
# TOOL 6: DuckDuckGo — Web Summary
# ─────────────────────────────────────────
def search_duckduckgo_summary(company_name: str) -> str:
    """Get instant web summary from DuckDuckGo"""
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": f"{company_name} company",
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        results = []
        if data.get("Abstract"):
            results.append(f"Summary: {data['Abstract']}")
        for topic in data.get("RelatedTopics", [])[:3]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(f"- {topic['Text']}")
        return "\n".join(results) if results else "No DuckDuckGo data found."
    except Exception as e:
        return f"DuckDuckGo error: {str(e)}"