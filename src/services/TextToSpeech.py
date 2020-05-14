from ..protobuf import add_Text2SpeechServiceServicer_to_server, Text2SpeechServiceServicer, TTSInput, TTSOutput
from ..utils.logger import get_logger
import grpc
from concurrent import futures
from gtts import gTTS
from io import BytesIO

__all__ = ['Text2SpeechService']

class Servicer:
    def __init__(self):
        self.logger = get_logger()

    def TextToSpeech(self, request, context):
        self.logger.info(f'Generating speech for {request.text}')
        mp3_fp = BytesIO()
        tts = gTTS(request.text)
        tts.write_to_fp(mp3_fp)
        return TTSOutput(data=mp3_fp.getvalue())


class Text2SpeechService(Text2SpeechServiceServicer):
    def __init__(self, max_workers: int = 1):
        self.logger = get_logger()
        self.servicer = Servicer()
        self.server = server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers)
        )

    def StartServer(self, port: int = 8080):
        ''' boot up grpc service
        Args:
        - service: service to boot up
        - port: port to listen to
        '''
        add_Text2SpeechServiceServicer_to_server(self.servicer, self.server)
        self.server.add_insecure_port('[::]:{}'.format(port))
        self.logger.info('TTS Server starting up..')
        self.server.start()
        self.server.wait_for_termination()
