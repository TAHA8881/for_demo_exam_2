import psycopg2
from psycopg2.extras import RealDictCursor
from models import Product
from contextlib import closing

def get_connection():
    return psycopg2.connect(
        dbname= "shoe_shop",
        user= "postgres",
        password = "postgres",
        host = "localhost",
        port = 5432
    )

def get_products():
    with closing(get_connection()) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
            SELECT
                p.id,
                p.product_name,
                p.category,
                p.manufacturer,
                p.content,
                p.image,
                p.price,
                COALESCE(SUM(s.quantity), 0) AS quantity
            FROM products p
            LEFT JOIN stock_items s
                ON p.id = s.product_id
            GROUP BY p.id
            """)

            return [
                Product(
                    product_id = row["id"],
                    name = row["product_name"],
                    category = row["category"],
                    manufacturer = row["manufacturer"],
                    content = row["content"],
                    image = row["image"],
                    price = row["price"],
                    quantity = row["quantity"],
                )
                for row in cursor.fetchall()
            ]


# products = get_products()
# print(products)