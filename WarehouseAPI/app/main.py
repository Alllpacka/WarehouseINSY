from fastapi import FastAPI, HTTPException
from psycopg2 import Error
from pydantic import BaseModel
from app.database import db
from app.routes.suppliers import router as suppliers_router

app = FastAPI(root_path="/warehouse")
app.include_router(suppliers_router)


def get_items():
    try:

        cursor = db.get_cursor()
        # Fetch all data from the "Items" table
        cursor.execute('SELECT * FROM "Items"')
        items = cursor.fetchall()

        return items

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


class Item(BaseModel):
    name: str
    supplier_id: int
    shelf_id: int


def add_item(item: Item):
    try:
        cursor = db.get_cursor()

        # Insert a new item into the "Items" table
        cursor.execute('INSERT INTO "Items" (name, "supplierId", "shelfId") VALUES (%s, %s, %s) RETURNING id;',
                       (item.name, item.supplier_id, item.shelf_id))

        # Commit the transaction
        db.conn.commit()

        # Fetch the ID of the newly inserted item
        item_id = cursor.fetchone()[0]

        return {"item_id": item_id}

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL or inserting item", error)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/items")
async def get_all_items():
    items = get_items()
    return {"items": items}


@app.post("/add_item")
async def add_test_item(item: Item):
    result = add_item(item)
    return result
