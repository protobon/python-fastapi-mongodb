import asyncio
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from redis import StrictRedis
from loguru import logger

from app.util.redis import get_redis_client
from app.model.product import Product, get_products_by_filter, get_product_by_id
from app.cache.product import ProductCache
from app.schema.product import (ProductSchema, FetchProductSchema, FetchProductBody,
                                FetchProductResponse, NewProductSchema, ProductBody, ProductResponse)


router = APIRouter(
    prefix="/product",
    tags=["product"]
)


@router.post(path="/new",
             description="Create a new product",
             response_model=ProductResponse)
async def create_product(product: NewProductSchema = Body(...),
                         redis_client: StrictRedis = Depends(get_redis_client)):
    try:
        product_dict = product.dict()
        new_product = Product(**product_dict).save()
        product_dict["_id"] = str(new_product.id)
        asyncio.ensure_future(ProductCache.update_one(redis_client, product_dict))
        body = ProductBody(
            success=True,
            timestamp=datetime.now().isoformat(),
            data=ProductSchema(
                id=str(new_product.id),
                title=getattr(product, "title"),
                quantity=getattr(product, "quantity"),
                createdAt=getattr(product, "createdAt"))
        )
        response = ProductResponse(body=body).dict()
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.exception("create_product")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(path="/all",
            description="Fetch all products",
            response_model=FetchProductResponse)
async def fetch_products():
    try:
        all_products = Product.objects().all()
        product_schemas = []
        for product in all_products:
            product_schemas.append(ProductSchema(
                id=str(product.id),
                title=getattr(product, "title", ""),
                quantity=getattr(product, "quantity", 0),
                createdAt=getattr(product, "createdAt", None)
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
        logger.exception("fetch_products")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(path="/all/cache",
            description="Fetch all products from cache",
            response_model=FetchProductResponse)
async def fetch_products_cache(redis_client: StrictRedis = Depends(get_redis_client)):
    try:
        all_products = ProductCache(client=redis_client).get_all()
        product_schemas = []
        for product in all_products:
            product_schemas.append(ProductSchema(
                id=product.get("_id"),
                title=product.get("title"),
                quantity=product.get("quantity"),
                createdAt=product.get("createdAt")
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
        logger.exception("fetch_products_cache")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(path="/{product_id}",
            description="Get a product by id",
            response_model=ProductResponse)
async def get_product(product_id: str):
    try:
        product = get_product_by_id(product_id)
        body = ProductBody(
            success=True,
            timestamp=datetime.now().isoformat(),
            data=ProductSchema(
                id=str(product.id),
                title=getattr(product, "title"),
                quantity=getattr(product, "quantity"),
                createdAt=getattr(product, "createdAt"))
        )
        response = ProductResponse(body=body).dict()
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.exception("get_product")
        raise HTTPException(status_code=500, detail=str(e))


@router.put(path="/update",
            description="Update a product, replaces whole document",
            response_model=ProductResponse)
async def update_product(product: ProductSchema = Body(...), redis_client: StrictRedis = Depends(get_redis_client)):
    try:
        product_dict = product.dict()
        Product(**product_dict).save()
        asyncio.ensure_future(ProductCache.update_one(redis_client, product_dict))
        body = ProductBody(
            success=True,
            timestamp=datetime.now().isoformat(),
            data=product
        )
        response = ProductResponse(body=body).dict()
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.exception("get_product")
        raise HTTPException(status_code=500, detail=str(e))
