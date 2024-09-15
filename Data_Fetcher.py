import aiohttp
import asyncio


class FetchingPosts:

    def __init__(self, base_url, post_queue):

        self.base_url = base_url
        self.post_queue = post_queue

    async def fetch_post(self, post_id):

        post_url = f"{self.base_url}{post_id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(post_url, ssl=False) as response:
                    response.raise_for_status()
                    post_data = await response.json()
                    await self.post_queue.put(post_data)
            except aiohttp.ClientError as e:
                print(f"Failed to fetch post {post_id}: {e}")

    async def fetch_all_posts(self, total_posts):

        tasks = [
            asyncio.create_task(self.fetch_post(post_id))
            for post_id in range(1, total_posts + 1)
        ]
        await asyncio.gather(*tasks)
        await self.post_queue.put(None)
