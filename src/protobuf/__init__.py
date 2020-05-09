import sys
sys.path.append(
    "./src/protobuf"
)  # this should be the directory of the generated files relative to where you're running it from
from .seq2seq_service_pb2 import *
from .seq2seq_service_pb2_grpc import *
from .image_classification_service_pb2 import *
from .image_classification_service_pb2_grpc import *
