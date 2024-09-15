import asyncio
from Data_Fetcher import FetchingPosts
from Data_Writer import PostWriter
import time


async def main():
    file_name = "posts.json"
    total_posts = 77
    base_url = "https://jsonplaceholder.typicode.com/posts/"

    post_queue = asyncio.Queue()

    fetcher = FetchingPosts(base_url=base_url, post_queue=post_queue)
    writer = PostWriter(file_name=file_name, post_queue=post_queue)

    start_time = time.time()

    await writer.start_file()

    fetch_task = asyncio.create_task(fetcher.fetch_all_posts(total_posts))
    save_task = asyncio.create_task(writer.save_posts_to_file())

    await fetch_task
    await save_task

    await writer.close_file()

    end_time = time.time()
    print(f"Time spent: {end_time - start_time}")


if __name__ == "__main__":
    asyncio.run(main())
