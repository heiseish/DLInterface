from ..model.DialoGPT import DialoGPT
from ..protobuf import add_Seq2SeqServiceServicer_to_server, Seq2SeqServiceServicer, ConversationResponse
from ..utils.logger import get_logger
import grpc
from concurrent import futures

__all__ = ['ConverseService']


class Servicer:
    ''' Provides methods that implement functionality of route guide server.'''
    def __init__(
        self,
        model_path: str,
    ):
        self.logger = get_logger()
        self.model = DialoGPT(model_path)

    def Initialize(self):
        return self.model.Initialize()

    def RespondToText(self, request, context):
        self.logger.info(f'Generating text for {request.text}')
        return ConversationResponse( \
            trans_id=request.trans_id,
            state=ConversationResponse.State.Value('SUCCESS'), \
            text=self.model.GenerateFor(request.text)
        )


class ConverseService(Seq2SeqServiceServicer):
    def __init__(self, model_path: str, max_workers: int = 1):
        self.logger = get_logger()
        self.servicer = Servicer(model_path)
        self.server = server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers)
        )

    def Initialize(self):
        return self.servicer.Initialize()

    def StartServer(self, port: int = 8080):
        ''' boot up grpc service
        Args:
        - service: service to boot up
        - port: port to listen to
        '''
        add_Seq2SeqServiceServicer_to_server(self.servicer, self.server)
        self.server.add_insecure_port('[::]:{}'.format(port))
        self.logger.info('Server starting up..')
        self.server.start()
        self.server.wait_for_termination()
