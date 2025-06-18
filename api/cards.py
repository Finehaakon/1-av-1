
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/cards")
def get_cards():
    player = request.args.get("player", "")
    if not player:
        return jsonify([])

    query = f"{player} 1/1"
    url = "https://www.ebay.com/sch/i.html?_nkw=" + query.replace(" ", "+")
    params = {
        "_nkw": query,
        "_sop": "10",
        "_ipg": "10",
        "_sacat": "0",
        "LH_Sold": "0"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, params=params, headers=headers)
    html = res.text

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
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
