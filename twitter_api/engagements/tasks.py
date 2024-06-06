from twitter_api.core.logging import logger
from twitter_api.database.depends import get_db_session
from twitter_api.posts.models import Post

from .models import View


def increase_post_view_count(post_id: int):
    logger.info('Task to increase post #{} views has been called'.format(post_id))
    db_session = get_db_session()
    post = db_session.query(Post).filter(Post.id == post_id).one_or_none()
    if post is None:
        return
    post_view = db_session.query(View).filter(View.post_id == post_id).one_or_none()
    if post_view is None:
        new_post_view = View(post_id=post_id, count=1)
        db_session.add(new_post_view)
    else:
        post_view.count = post_view.count + 1
    db_session.commit()
    return
