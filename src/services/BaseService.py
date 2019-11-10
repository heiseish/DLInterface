import grpc
from ..utils import get_logger
from concurrent import futures
__all__ = [
    'BaseService',
]
class BaseService:
    def __init__(self, max_workers: int = 1):
        self.logger = get_logger()
        self.server = server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    
    def Initialize(self):
        raise NotImplementedError('Method not implemented')

    def StartServer(self, port: int = 8080):
        self.server.add_insecure_port('[::]:{}'.format(port))
        self.logger.info('Server starting up..')
        self.server.start()
        self.server.wait_for_termination()