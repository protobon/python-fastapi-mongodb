from redis import StrictRedis
from app.cache.base import Cache
from app.model.product import Product
from loguru import logger


class ProductCache(Cache):
    client = None
    name = "product"
    refresh_in_seconds = 3600

    def __init__(self, client: StrictRedis):
        self.client = client
        alive = client.get(f"{self.name}__alive")
        if not alive:
            logger.info("ProductCache RELOAD")
            pipeline = []
            super().__init__(client, Product, self.name, pipeline, self.refresh_in_seconds)

    def get_all(self):
        return super().get_all(self.name)

    def get_by_id(self, item_id: str):
        return super().get_by_id(f"{self.name}:{item_id}")

    @classmethod
    async def update_one(cls, client: StrictRedis, document: dict):
        super().update_one(client=client, name=cls.name, doc=document, time=cls.refresh_in_seconds)
