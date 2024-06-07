import grpc

from twitter_api.core.config import settings
from twitter_api.core.logging import logger

from .grpc import post_views_pb2, post_views_pb2_grpc


def create_post_view_count_entry(post_id: int):
    logger.info('Task to increase post #{} views has been called'.format(post_id))
    with grpc.insecure_channel(settings.ANALYTICS_URL) as channel:
        stub = post_views_pb2_grpc.PostViewAnalyticsStub(channel)
        stub.CreateViewCount(post_views_pb2.PostViewRequest(post_id=post_id))


def increase_post_view_count(post_id: int):
    logger.info('Task to increase post #{} views has been called'.format(post_id))
    with grpc.insecure_channel(settings.ANALYTICS_URL) as channel:
        stub = post_views_pb2_grpc.PostViewAnalyticsStub(channel)
        stub.UpdateViewCount(post_views_pb2.PostViewRequest(post_id=post_id))


def delete_post_view_count_entry(post_id: int):
    logger.info('Task to increase post #{} views has been called'.format(post_id))
    with grpc.insecure_channel(settings.ANALYTICS_URL) as channel:
        stub = post_views_pb2_grpc.PostViewAnalyticsStub(channel)
        stub.DeleteViewCount(post_views_pb2.PostViewRequest(post_id=post_id))
