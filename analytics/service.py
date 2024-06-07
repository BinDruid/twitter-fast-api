import grpc
import post_views_pb2
import post_views_pb2_grpc
from logger import logger
from sqlalchemy.orm import Session, sessionmaker

from database.configs import engine
from database.models import PostView


def get_db_session() -> Session:
    session_class = sessionmaker(bind=engine)
    session = session_class()
    return session


class ViewAnalyticsService(post_views_pb2_grpc.PostViewAnalyticsServicer):
    def GetViewCount(self, request, context):
        post_id = request.post_id
        logger.info(f'Counting views for post #{post_id}')
        db_session = get_db_session()
        post_view = db_session.query(PostView).filter(PostView.post_id == post_id).one_or_none()
        if post_view is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f'Post #{post_id} not found')
        return post_views_pb2.PostViewResponse(post_id=post_id, post_view_count=post_view.count)

    def CreateViewCount(self, request, context):
        post_id = request.post_id
        logger.info(f'Creating view entry for post #{post_id}')
        db_session = get_db_session()
        post_view = db_session.query(PostView).filter(PostView.post_id == post_id).one_or_none()
        if post_view is not None:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, f'View record for post #{post_id} already exists')
        new_post_view = PostView(post_id=post_id, count=0)
        db_session.add(new_post_view)
        db_session.commit()
        return post_views_pb2.PostViewResponse(post_id=post_id, post_view_count=0)

    def UpdateViewCount(self, request, context):
        post_id = request.post_id
        logger.info(f'Increasing view count entry for post #{post_id}')
        db_session = get_db_session()
        post_view = db_session.query(PostView).filter(PostView.post_id == post_id).one_or_none()
        if post_view is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f'Post #{post_id} not found')
        post_view.count = post_view.count + 1
        db_session.commit()
        return post_views_pb2.PostViewResponse(post_id=post_id, post_view_count=post_view.count)

    def DeleteViewCount(self, request, context):
        post_id = request.post_id
        logger.info(f'Deleting view entry for post #{post_id}')
        db_session = get_db_session()
        post_view = db_session.query(PostView).filter(PostView.post_id == post_id).one_or_none()
        if post_view is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f'Post #{post_id} not found')
        db_session.delete(post_view)
        db_session.commit()
        return post_views_pb2.PostViewResponse(post_id=post_id, post_view_count=0)
