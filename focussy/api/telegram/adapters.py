from typing import Callable

import anyio.to_thread


async def run_async(func: Callable, *args, **kwargs):
    def run_func():
        return func(*args, **kwargs)

    return await anyio.to_thread.run_sync(run_func)
