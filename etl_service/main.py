import asyncio
import logging

from etl.etl_loader import ESLoader
from etl.helpers import redis

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


async def main():
    await ESLoader().load_data()


if __name__ == '__main__':
    logger.info("Запуск процесса переноса данных из es в postgre")
    loop = asyncio.get_event_loop()
    while True:
        try:
            loop.run_until_complete(main())
            logger.info("Перенос выполнен")
            loop.run_until_complete(asyncio.sleep(3600))
        except Exception as e:
            logger.exception("Во время работы сервиса возникла ошибка")
            loop.close()
            redis.close()
