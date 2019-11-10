import grpc
from .model import DialoGPT
from .protobuf import seq2seq_service_pb2_grpc, ConversationResponse
from .utils import get_logger
from concurrent import futures
__all__ = [
    'ConverseService',
    'StartService'
]
class BaseService:
    pass

class ConverseService(seq2seq_service_pb2_grpc.Seq2SeqServiceServicer, BaseService):
    ''' Provides methods that implement functionality of route guide server.'''
    def __init__(self, model_path: str):
        self.logger = get_logger()
        self.model = DialoGPT(model_path)

    def Initialize(self):
        return self.model.Initialize()

    def RespondToText(self, request, context):
        self.logger.info('Generating text for {}'.format(request.trans_id))
        return ConversationResponse( \
            trans_id=request.trans_id, 
            state=ConversationResponse.State.Value('SUCCESS'), \
            text=self.model.GenerateFor(request.text)
        )

def StartService(service: BaseService, port: int = 8080):
    ''' boot up grpc service
    Args:
    - service: service to boot up
    - port: port to listen to
    '''
    logger = get_logger()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    seq2seq_service_pb2_grpc.add_Seq2SeqServiceServicer_to_server(
        service, server)
    server.add_insecure_port('[::]:{}'.format(port))
    logger.info('Server starting up..')
    server.start()
    server.wait_for_termination()