from ..protobuf import add_ImageClassificationServiceServicer_to_server, ImageClassificationServiceServicer,\
    ImageResponse
from .BaseService import *


class ImageRecognitionService(ImageClassificationServiceServicer, BaseService):
    ''' Provides methods that implement functionality of route guide server.'''
    def __init__(self, model_path: str, max_workers: int = 1):
        super(ImageRecognitionService, self).__init__(max_workers)

    def Initialize(self):
        pass

    def RecognizeImage(self, request, context):
        pass

    def StartServer(self, port: int = 8080):
        ''' boot up grpc service
        Args:
        - service: service to boot up
        - port: port to listen to
        '''
        add_ImageClassificationServiceServicer_to_server(self, self.server)
        super(ImageRecognitionService, self).StartServer(port)
