import os
from concurrent import futures

import grpc
from service import ViewAnalyticsService, post_views_pb2_grpc
from service.logger import logger


def runserver():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    post_views_pb2_grpc.add_PostViewAnalyticsServicer_to_server(ViewAnalyticsService(), server)
    server_port = os.getenv('ANALYTICS_PORT', default=50051)
    server.add_insecure_port(f'[::]:{server_port}')
    logger.info(f'GRPC server running on 0.0.0.0:{server_port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    runserver()
