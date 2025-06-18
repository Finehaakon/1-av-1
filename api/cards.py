
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route("/api/cards")
def get_cards():
    player = request.args.get("player", "")
    if not player:
        return jsonify([])

    query = f"{player} 1/1"
    query_encoded = query.replace(" ", "+")
    url = f"https://www.ebay.com/sch/i.html?_nkw={query_encoded}&_sop=10&_ipg=10"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(".s-item")
        results = []

        for item in items:
            title_tag = item.select_one(".s-item__title")
            price_tag = item.select_one(".s-item__price")
            img_tag = item.select_one("img")
            link_tag = item.select_one("a.s-item__link")

            if title_tag and price_tag and img_tag and link_tag:
                results.append({
                    "title": title_tag.get_text(),
                    "price": price_tag.get_text(),
                    "image": img_tag.get("src"),
                    "link": link_tag.get("href")
                })

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})
