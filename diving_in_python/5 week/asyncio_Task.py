import asyncio


async def sleep_tsk(num):
    for i in range(2):
        print(f'process task: {num} iter: {i}')
        await asyncio.sleep(5)

    return num


loop = asyncio.get_event_loop()

task_list = [loop.create_task(sleep_tsk(i)) for i in range(10)]
loop.run_until_complete(asyncio.wait(task_list))

loop.run_until_complete(loop.create_task(sleep_tsk(3)))

loop.run_until_complete(asyncio.gather(sleep_tsk(10), sleep_tsk(20)))
