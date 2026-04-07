import json
from difflib import get_close_matches

class ProductRetriever:
    def __init__(self):
        with open("data/catalog.json", "r") as f:
            self.data = json.load(f)

    def get_context(self, query):
        query = query.lower()
        names = [p["name"] for p in self.data["products"]]
        match = get_close_matches(query, names, n=1, cutoff=0.7)  # updated for accuracy
        if match:
            p = next(p for p in self.data["products"] if p["name"] == match[0])
            return f"{p['name']} costs {p['price']}. Specs: {p['description']}. Status: {p['status']}"
        return "No specific product found. Try asking about Earbud Pro or Smart Watch."
