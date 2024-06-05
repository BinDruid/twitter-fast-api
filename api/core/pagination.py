from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm.query import Query
from sqlalchemy_filters import apply_pagination

from api.database import PydanticBase

from .config import settings
from .logging import logger


class Pagination(PydanticBase):
    itemsPerPage: int
    page: int
    total: int


def paginate(*, items: Query, page: int) -> dict:
    try:
        query, pagination = apply_pagination(items, page_number=page, page_size=settings.PAGINATION_PER_PAGE)
    except ProgrammingError as e:
        logger.info(e)
        return {
            'items': [],
            'itemsPerPage': settings.PAGINATION_PER_PAGE,
            'page': page,
            'total': 0,
        }
    return {
        'items': query.all(),
        'itemsPerPage': pagination.page_size,
        'page': pagination.page_number,
        'total': pagination.total_results,
    }
