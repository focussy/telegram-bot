import functools
from typing import Callable

import anyio.to_thread


async def run_async(func: Callable, *args, **kwargs):
    return await anyio.to_thread.run_sync(functools.partial(func, *args, **kwargs))
