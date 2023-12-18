from fastapi import APIRouter, HTTPException
from psycopg2 import Error
from pydantic import BaseModel
from app.database import db

router = APIRouter(prefix="/shelves", tags=["Shelves"])


class Shelf(BaseModel):
    locationCode: str
    warehouseId: int


def get_shelves():
    try:
        cursor = db.get_cursor()
        cursor.execute('SELECT * FROM "Shelves"')
        shelves = cursor.fetchall()
        return shelves
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


def add_shelf(shelf: Shelf):
    try:
        cursor = db.get_cursor()
        cursor.execute('INSERT INTO "Shelves" ("locationCode", "warehouseId") VALUES (%s, %s) RETURNING id;',
                       (shelf.locationCode, shelf.warehouseId))
        db.conn.commit()
        shelf_id = cursor.fetchone()[0]
        return {"shelf_id": shelf_id}
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL or inserting shelf", error)
        raise HTTPException(status_code=500, detail="Internal Server Error")


def update_shelf(shelf_id: int, updated_shelf: Shelf):
    try:
        cursor = db.get_cursor()
        cursor.execute('UPDATE "Shelves" SET "locationCode" = %s, "warehouseId" = %s WHERE id=%s RETURNING id;',
                       (updated_shelf.locationCode, updated_shelf.warehouseId, shelf_id))
        db.conn.commit()
        updated_shelf_id = cursor.fetchone()[0]
        return {"updated_shelf_id": updated_shelf_id}
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL or updating shelf", error)
        raise HTTPException(status_code=500, detail="Internal Server Error")


def delete_shelf(shelf_id: int):
    try:
        cursor = db.get_cursor()
        cursor.execute('DELETE FROM "Shelves" WHERE id=%s RETURNING id;', (shelf_id,))
        db.conn.commit()
        deleted_shelf_id = cursor.fetchone()[0]
        return {"deleted_shelf_id": deleted_shelf_id}
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL or deleting shelf", error)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/")
async def get_all_shelves():
    shelves = get_shelves()
    return {"shelves": shelves}


@router.post("/")
async def add_shelf_endpoint(shelf: Shelf):
    result = add_shelf(shelf)
    return result


@router.patch("/{shelf_id}")
async def update_shelf_endpoint(shelf_id: int, updated_shelf: Shelf):
    result = update_shelf(shelf_id, updated_shelf)
    return result


@router.delete("/{shelf_id}")
async def delete_shelf_endpoint(shelf_id: int):
    result = delete_shelf(shelf_id)
    return result
