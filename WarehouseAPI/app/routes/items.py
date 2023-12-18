from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import db

router = APIRouter(prefix="/items", tags=["Items"])


class Item(BaseModel):
    name: str
    supplierId: int
    shelfId: int
    buyingPrice: int
    sellingPrice: int


def get_items():
    try:
        cursor = db.get_cursor()
        cursor.execute('SELECT * FROM "Items"')
        items = cursor.fetchall()
        return items
    except Exception as error:
        print("Error while connecting to PostgreSQL", error)


def add_item(item: Item):
    try:
        cursor = db.get_cursor()
        cursor.execute(
            'INSERT INTO "Items" (name, "supplierId", "shelfId", "buyingPrice", "sellingPrice") VALUES (%s, %s, %s, %s, %s) RETURNING id;',
            (item.name, item.supplierId, item.shelfId, item.buyingPrice, item.sellingPrice))
        db.conn.commit()
        item_id = cursor.fetchone()[0]
        return {"item_id": item_id}
    except Exception as error:
        print("Error while connecting to PostgreSQL or inserting item", error)
        raise HTTPException(status_code=500, detail="Internal Server Error")


def update_item(item_id: int, updated_item: Item):
    try:
        cursor = db.get_cursor()
        cursor.execute(
            'UPDATE "Items" SET name = %s, "supplierId" = %s, "shelfId" = %s, "buyingPrice" = %s, "sellingPrice" = %s WHERE id=%s RETURNING id;',
            (updated_item.name, updated_item.supplierId, updated_item.shelfId, updated_item.buyingPrice,
             updated_item.sellingPrice, item_id))
        db.conn.commit()
        updated_item_id = cursor.fetchone()[0]
        return {"updated_item_id": updated_item_id}
    except Exception as error:
        print("Error while connecting to PostgreSQL or updating item", error)
        raise HTTPException(status_code=500, detail="Internal Server Error")


def delete_item(item_id: int):
    try:
        cursor = db.get_cursor()
        cursor.execute('DELETE FROM "Items" WHERE id=%s RETURNING id;', (item_id,))
        db.conn.commit()
        deleted_item_id = cursor.fetchone()[0]
        return {"deleted_item_id": deleted_item_id}
    except Exception as error:
        print("Error while connecting to PostgreSQL or deleting item", error)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/")
async def get_all_items():
    items = get_items()
    return {"items": items}


@router.post("/")
async def add_item_endpoint(item: Item):
    result = add_item(item)
    return result


@router.patch("/{item_id}")
async def update_item_endpoint(item_id: int, updated_item: Item):
    result = update_item(item_id, updated_item)
    return result


@router.delete("/{item_id}")
async def delete_item_endpoint(item_id: int):
    result = delete_item(item_id)
    return result
