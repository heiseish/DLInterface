import sys
sys.path.append(
    "./src/protobuf"
)  # this should be the directory of the generated files relative to where you're running it from
from .py_rpc_pb2 import *
from .py_rpc_pb2_grpc import *
