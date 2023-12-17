from fastapi import APIRouter, HTTPException
from psycopg2 import Error
from pydantic import BaseModel
from app.database import db

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


class Supplier(BaseModel):
    name: str
    city: str


def get_suppliers():
    try:
        cursor = db.get_cursor()

        # Fetch all data from the "Items" table
        cursor.execute('SELECT * FROM "Suppliers"')
        items = cursor.fetchall()

        return items

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


def add_supplier(supplier: Supplier):
    try:
        cursor = db.get_cursor()

        cursor.execute('INSERT INTO "Suppliers" (name, city) VALUES (%s, %s) RETURNING id;',
                       (supplier.name, supplier.city))

        db.conn.commit()

        supplier_id = cursor.fetchone()[0]

        return {"supplier_id": supplier_id}

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL or inserting item", error)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/")
async def get_all_suppliers():
    suppliers = get_suppliers()
    return {"suppliers": suppliers}


@router.post("/")
async def add_test_supplier(supplier: Supplier):
    result = add_supplier(supplier)
    return result
