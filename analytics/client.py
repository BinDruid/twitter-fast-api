import grpc
import post_views_pb2
import post_views_pb2_grpc


def main():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = post_views_pb2_grpc.PostViewAnalyticsStub(channel)
        response = stub.GetViewCount(post_views_pb2.PostViewRequest(post_id=2))
        print(response)


if __name__ == '__main__':
    main()
