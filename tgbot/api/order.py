import aiohttp


class APIClient:
    def __init__(self):
        self.url = "https://api.khamraev.uz/"

    async def get_order_statistics(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.url}api/orders/statistics/") as response:
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}

    async def get_order_list_by_status(self, order_status, page: int = 1):
        try:
            params = {"page": page} if page > 1 else {}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"{self.url}api/orders/status/{order_status}/", params=params
                ) as response:
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}

    async def get_order_detail(self, order_id):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.url}api/orders/{order_id}/") as response:
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}

    async def get_workers(self, page: int = 1):
        try:
            params = {"page": page} if page > 1 else {}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.url}api/workers/", params=params) as response:
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}
    async def get_workers_by_specialization(self, specialization, page: int = 1):
        try:
            params = {"page": page} if page > 1 else {}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.url}api/workers/by/{specialization}/", params=params) as response:
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}

    async def get_specializations(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.url}api/workers/specializations/") as response:
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}