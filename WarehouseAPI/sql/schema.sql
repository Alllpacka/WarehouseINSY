CREATE TABLE "Items" (
    "id" serial NOT NULL UNIQUE,
    "name" TEXT NOT NULL,
    "supplierId" integer NOT NULL,
    "shelfId" integer NOT NULL,
    CONSTRAINT "Items_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "Shelves" (
    "id" serial NOT NULL,
    "locationCode" varchar(3) NOT NULL,
    "warehouseId" integer NOT NULL,
    CONSTRAINT "Shelves_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "Warehouses" (
    "id" serial NOT NULL,
    "zipCode" integer NOT NULL,
    "address" integer NOT NULL,
    CONSTRAINT "Warehouses_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "Suppliers" (
    "id" serial NOT NULL,
    "name" TEXT NOT NULL,
    "city" TEXT NOT NULL,
    CONSTRAINT "Suppliers_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);

CREATE TABLE "Prices" (
    "itemId" integer NOT NULL,
    "buyingPrice" integer NOT NULL,
    "sellingPrice" integer NOT NULL
) WITH (
  OIDS=FALSE
);

ALTER TABLE "Items" ADD CONSTRAINT "Items_fk0" FOREIGN KEY ("supplierId") REFERENCES "Suppliers"("id");
ALTER TABLE "Items" ADD CONSTRAINT "Items_fk1" FOREIGN KEY ("shelfId") REFERENCES "Shelves"("id");
ALTER TABLE "Shelves" ADD CONSTRAINT "Shelves_fk0" FOREIGN KEY ("warehouseId") REFERENCES "Warehouses"("id");
ALTER TABLE "Prices" ADD CONSTRAINT "Prices_fk0" FOREIGN KEY ("itemId") REFERENCES "Items"("id");