from redis import StrictRedis
from app.cache.base import Cache
from app.model.product import Product


class ProductCache(Cache):
    name = "product"
    refresh_in_seconds = 3600

    def __init__(self, client: StrictRedis):
        self.client = client
        alive = client.get(f"{self.name}__alive")
        if not alive:
            print("RELOAD")
            pipeline = []
            super().__init__(client, Product, self.name, pipeline, self.refresh_in_seconds)

    def get_all(self, name: str):
        return super().get_all(self.name)

    def get_by_id(self, item_id: str):
        return super().get_by_id(item_id)
