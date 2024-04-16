from ..model.DialoGPT import DialoGPT
from ..protobuf import add_PyRPCServiceServicer_to_server, PyRPCServiceServicer, ConversationResponse, TTSOutput
from ..utils.logger import get_logger
import grpc
from concurrent import futures
from gtts import gTTS
from io import BytesIO

__all__ = ['PyRPCService']


class Servicer(PyRPCServiceServicer):
    ''' Provides methods that implement functionality of route guide server.'''
    def __init__(
        self,
        model_path: str,
    ):
        self.logger = get_logger()
        self.model = DialoGPT(model_path, b'cuda')

    def Initialize(self):
        return self.model.Initialize()

    def RespondToText(self, request, context):
        self.logger.info(f'Generating text for {request.text}')
        return ConversationResponse( \
            trans_id=request.trans_id,
            state=ConversationResponse.State.Value('SUCCESS'), \
            text=self.model.GenerateFor(request.text)
        )
    
    def TextToSpeech(self, request, context):
        self.logger.info(f'Generating speech for {request.text}')
        mp3_fp = BytesIO()
        tts = gTTS(request.text, lang=request.lang)
        tts.write_to_fp(mp3_fp)
        return TTSOutput(data=mp3_fp.getvalue())


class PyRPCService:
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
        add_PyRPCServiceServicer_to_server(self.servicer, self.server)
        self.server.add_insecure_port('[::]:{}'.format(port))
        self.logger.info('Server starting up..')
        self.server.start()
        self.server.wait_for_termination()
