import asyncio
import time

async def foo():
    time.sleep(3)
    return 5

async def bar():
    r = await asyncio.gather(foo())
    return r[0]

print("a")
print("b")
print(asyncio.run(bar()))
print("c")
print("d")
print("e")