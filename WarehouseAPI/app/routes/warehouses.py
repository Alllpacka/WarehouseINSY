from fastapi import APIRouter, HTTPException
from psycopg2 import Error
from pydantic import BaseModel
from app.database import db

router = APIRouter(prefix="/warehouses", tags=["Warehouses"])


class Warehouse(BaseModel):
    zipCode: int
    address: str


def get_warehouses():
    try:
        cursor = db.get_cursor()
        cursor.execute('SELECT * FROM "Warehouses"')
        warehouses = cursor.fetchall()
        return warehouses
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


def add_warehouse(warehouse: Warehouse):
    try:
        cursor = db.get_cursor()
        cursor.execute('INSERT INTO "Warehouses" ("zipCode", address) VALUES (%s, %s) RETURNING id;',
                       (warehouse.zipCode, warehouse.address))
        db.conn.commit()
        warehouse_id = cursor.fetchone()[0]
        return {"warehouse_id": warehouse_id}
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL or inserting warehouse", error)
        raise HTTPException(status_code=500, detail="Internal Server Error")


def update_warehouse(warehouse_id: int, updated_warehouse: Warehouse):
    try:
        cursor = db.get_cursor()
        cursor.execute('UPDATE "Warehouses" SET "zipCode" = %s, address = %s WHERE id=%s RETURNING id;',
                       (updated_warehouse.zipCode, updated_warehouse.address, warehouse_id))
        db.conn.commit()
        updated_warehouse_id = cursor.fetchone()[0]
        return {"updated_warehouse_id": updated_warehouse_id}
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL or updating warehouse", error)
        raise HTTPException(status_code=500, detail="Internal Server Error")


def delete_warehouse(warehouse_id: int):
    try:
        cursor = db.get_cursor()
        cursor.execute('DELETE FROM "Warehouses" WHERE id=%s RETURNING id;', (warehouse_id,))
        db.conn.commit()
        deleted_warehouse_id = cursor.fetchone()[0]
        return {"deleted_warehouse_id": deleted_warehouse_id}
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL or deleting warehouse", error)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/")
async def get_all_warehouses():
    warehouses = get_warehouses()
    return {"warehouses": warehouses}


@router.post("/")
async def add_warehouse_endpoint(warehouse: Warehouse):
    result = add_warehouse(warehouse)
    return result


@router.patch("/{warehouse_id}")
async def update_warehouse_endpoint(warehouse_id: int, updated_warehouse: Warehouse):
    result = update_warehouse(warehouse_id, updated_warehouse)
    return result


@router.delete("/{warehouse_id}")
async def delete_warehouse_endpoint(warehouse_id: int):
    result = delete_warehouse(warehouse_id)
    return result
