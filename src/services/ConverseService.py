from ..model import DialoGPT
from ..protobuf import add_Seq2SeqServiceServicer_to_server, Seq2SeqServiceServicer, ConversationResponse
from .BaseService import *

class ConverseService(Seq2SeqServiceServicer, BaseService):
    ''' Provides methods that implement functionality of route guide server.'''
    def __init__(self, model_path: str, max_workers: int = 1):
        super(ConverseService, self).__init__(max_workers)
        self.model = DialoGPT(model_path)

    def Initialize(self):
        return self.model.Initialize()

    def RecognizeImage(self, request, context):
        self.logger.info('Generating text for {}'.format(request.trans_id))
        return ConversationResponse( \
            trans_id=request.trans_id, 
            state=ConversationResponse.State.Value('SUCCESS'), \
            text=self.model.GenerateFor(request.text)
        )

    def StartServer(self, port: int = 8080):
        ''' boot up grpc service
        Args:
        - service: service to boot up
        - port: port to listen to
        '''
        add_Seq2SeqServiceServicer_to_server(self, self.server)
        super(ConverseService, self).StartServer(port)