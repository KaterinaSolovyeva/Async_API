import asyncio

from etl_service.etl.etl_loader import ESLoader


async def main():
    await ESLoader().load_data()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
