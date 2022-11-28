from fastapi.params import Query

from app.core.config import settings


class PaginationDataParams:
    def __init__(
        self,
        sort: str = Query('', description='Sorting'),
        page_size: int = Query(settings.DEFAULT_PAGE_SIZE, description='Number of filmworks on page',
                               alias='page[size]'),
        page: int = Query(settings.DEFAULT_PAGE_NUMBER, description='Page number', alias='page[number]')
    ):
        self.sort = sort
        self.page_size = page_size
        self.page = page
