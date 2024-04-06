from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from redis import StrictRedis

from app.db.redis import get_redis_client
from app.model.product import Product
from app.cache.product import ProductCache
from app.schema.product import (ProductSchema, FetchProductSchema, FetchProductBody,
                                FetchProductResponse, NewProductSchema, NewProductBody, NewProductResponse)


product = APIRouter(
    prefix="/product",
    tags=["product"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@product.post(path="/new",
              description="Create a new product",
              response_model=ProductSchema)
async def create_product(p: NewProductSchema = Body(...)):
    new_product = Product(
        title=getattr(p, "title", ""),
        quantity=getattr(p, "quantity", 0),
        createdAt=datetime.now()
    ).save()
    body = NewProductBody(
        success=True,
        timestamp=datetime.now().isoformat(),
        data=ProductSchema(
            id=str(new_product.id),
            title=getattr(p, "title"),
            quantity=getattr(p, "quantity"),
            createdAt=getattr(p, "createdAt"))
    )
    response = NewProductResponse(body=body).dict()
    return JSONResponse(content=response, status_code=200)


@product.get(path="/all",
             description="Fetch all products",
             response_model=FetchProductResponse)
async def fetch_products():
    try:
        all_products = Product.objects().all()
        product_schemas = []
        for p in all_products:
            product_schemas.append(ProductSchema(
                id=str(p.id),
                title=getattr(p, "title", ""),
                quantity=getattr(p, "quantity", 0),
                createdAt=getattr(p, "createdAt", None)
            ))

        fetch_schema = FetchProductSchema(
            products=product_schemas,
            total=len(product_schemas)
        )
        body = FetchProductBody(
            success=True,
            data=fetch_schema,
            timestamp=datetime.now().isoformat()
        )
        response = FetchProductResponse(body=body).dict()
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@product.get(path="/all/cache",
             description="Fetch all products from cache",
             response_model=FetchProductResponse)
async def fetch_products_cache(redis_client: StrictRedis = Depends(get_redis_client)):
    try:
        all_products = ProductCache(client=redis_client).get_all(ProductCache.name)
        product_schemas = []
        for p in all_products:
            product_schemas.append(ProductSchema(
                id=p.get("_id"),
                title=p.get("title"),
                quantity=p.get("quantity"),
                createdAt=p.get("createdAt")
            ))

        fetch_schema = FetchProductSchema(
            products=product_schemas,
            total=len(product_schemas)
        )
        body = FetchProductBody(
            success=True,
            data=fetch_schema,
            timestamp=datetime.now().isoformat()
        )
        response = FetchProductResponse(body=body).dict()
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@product.get("/{product_id}")
async def read_product(product_id: str):
    #  raise HTTPException(status_code=404, detail="Product not found")
    return dict()


@product.put("/{product_id}")
async def update_product(product_id: str):
    return dict()
