import json
import aiofiles


class PostWriter:

    def __init__(self, file_name, post_queue):

        self.file_name = file_name
        self.post_queue = post_queue

    async def start_file(self):

        async with aiofiles.open(self.file_name, "w") as file:
            await file.write("[\n")

    async def close_file(self):

        async with aiofiles.open(self.file_name, "a") as file:
            await file.write("]\n")

    async def save_posts_to_file(self):

        async with aiofiles.open(self.file_name, "a") as file:
            while True:
                post_data = await self.post_queue.get()
                if post_data is None:
                    break
                await file.write(f"{json.dumps(post_data, indent=4)},\n")
                self.post_queue.task_done()