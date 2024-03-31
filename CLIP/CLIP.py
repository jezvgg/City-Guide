from concurrent import futures
from clip_pb2 import ResultHello
import clip_pb2_grpc
import grpc

class HelloService(
    clip_pb2_grpc.HelloServicer
):
    def HelloPython(self, request, context):
        return ResultHello(result=f"Hello {request.name}!")

def service():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    clip_pb2_grpc.add_HelloServicer_to_server(
        HelloService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    service()