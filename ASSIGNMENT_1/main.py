from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 55000, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 500, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Keyboard", "price": 1200, "category": "Electronics", "in_stock": True},
    {"id": 4, "name": "Monitor", "price": 9000, "category": "Electronics", "in_stock": False},

    # New Products
    {"id": 5, "name": "Laptop Stand", "price": 1500, "category": "Accessories", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 3500, "category": "Accessories", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 2200, "category": "Electronics", "in_stock": True}
]

@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}
@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    filtered_products = []

    for product in products:
        if product["category"].lower() == category_name.lower():
            filtered_products.append(product)

    if len(filtered_products) == 0:
        return {"error": "No products found in this category"}

    return {"products": filtered_products}
@app.get("/products/instock")
def get_instock_products():
    instock_products = []

    for product in products:
        if product["in_stock"] == True:
            instock_products.append(product)

    return {
        "in_stock_products": instock_products,
        "count": len(instock_products)
    }
@app.get("/store/summary")
def store_summary():

    total_products = len(products)

    in_stock_count = 0
    out_of_stock_count = 0
    categories = set()

    for product in products:
        if product["in_stock"]:
            in_stock_count += 1
        else:
            out_of_stock_count += 1

        categories.add(product["category"])

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock_count,
        "out_of_stock": out_of_stock_count,
        "categories": list(categories)
    }
@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    matched_products = []

    for product in products:
        if keyword.lower() in product["name"].lower():
            matched_products.append(product)

    if len(matched_products) == 0:
        return {"message": "No products matched your search"}

    return {
        "matched_products": matched_products,
        "count": len(matched_products)
    }
@app.get("/products/deals")
def get_product_deals():

    best_deal = min(products, key=lambda x: x["price"])
    premium_pick = max(products, key=lambda x: x["price"])

    return {
        "best_deal": best_deal,
        "premium_pick": premium_pick
    }