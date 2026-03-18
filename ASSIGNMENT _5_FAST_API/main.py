from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math

app = FastAPI(title="Product API - Search Sort Pagination")

# -----------------------------
# Products Database
# -----------------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

# -----------------------------
# Orders Storage
# -----------------------------

orders = []
order_counter = 1


class Order(BaseModel):
    customer_name: str
    product_id: int
    quantity: int


# -----------------------------
# Create Order
# -----------------------------

@app.post("/orders")
def create_order(order: Order):
    global order_counter

    product = next((p for p in products if p["id"] == order.product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total = product["price"] * order.quantity

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "product": product["name"],
        "quantity": order.quantity,
        "total_price": total
    }

    orders.append(new_order)
    order_counter += 1

    return {"message": "Order placed", "order": new_order}


# -----------------------------
# Q1 SEARCH PRODUCTS
# -----------------------------

@app.get("/products/search")
def search_products(keyword: str):

    results = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not results:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(results),
        "products": results
    }


# -----------------------------
# Q2 SORT PRODUCTS
# -----------------------------

@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name"]:
        raise HTTPException(
            status_code=400,
            detail="sort_by must be 'price' or 'name'"
        )

    reverse = True if order == "desc" else False

    sorted_products = sorted(
        products,
        key=lambda x: x[sort_by],
        reverse=reverse
    )

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }


# -----------------------------
# Q3 PAGINATION
# -----------------------------

@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    total_products = len(products)

    total_pages = math.ceil(total_products / limit)

    start = (page - 1) * limit
    end = start + limit

    page_products = products[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_products": total_products,
        "total_pages": total_pages,
        "products": page_products
    }


# -----------------------------
# Q4 SEARCH ORDERS
# -----------------------------

@app.get("/orders/search")
def search_orders(customer_name: str):

    results = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not results:
        return {
            "message": f"No orders found for {customer_name}"
        }

    return {
        "customer_name": customer_name,
        "total_found": len(results),
        "orders": results
    }


# -----------------------------
# Q5 SORT BY CATEGORY THEN PRICE
# -----------------------------

@app.get("/products/sort-by-category")
def sort_by_category():

    sorted_products = sorted(
        products,
        key=lambda x: (x["category"], x["price"])
    )

    return {
        "sorted_products": sorted_products
    }


# -----------------------------
# Q6 SEARCH + SORT + PAGINATE
# -----------------------------

@app.get("/products/browse")
def browse_products(
        keyword: str = None,
        sort_by: str = "price",
        order: str = "asc",
        page: int = 1,
        limit: int = 4
):

    filtered = products

    # SEARCH
    if keyword:
        filtered = [
            p for p in filtered
            if keyword.lower() in p["name"].lower()
        ]

    # SORT
    reverse = True if order == "desc" else False

    if sort_by not in ["price", "name"]:
        raise HTTPException(
            status_code=400,
            detail="sort_by must be price or name"
        )

    filtered = sorted(
        filtered,
        key=lambda x: x[sort_by],
        reverse=reverse
    )

    # PAGINATION
    total_found = len(filtered)
    total_pages = math.ceil(total_found / limit)

    start = (page - 1) * limit
    end = start + limit

    page_data = filtered[start:end]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": page_data
    }


# -----------------------------
# BONUS PAGINATE ORDERS
# -----------------------------

@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 3):

    total_orders = len(orders)
    total_pages = math.ceil(total_orders / limit)

    start = (page - 1) * limit
    end = start + limit

    page_orders = orders[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_orders": total_orders,
        "total_pages": total_pages,
        "orders": page_orders
    }


# -----------------------------
# GET PRODUCT BY ID
# (Place below others)
# -----------------------------

@app.get("/products/{product_id}")
def get_product(product_id: int):

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product