#!/usr/bin/env python
'''' Entry script for python server '''
import os
import grpc
from src.utils import init_logger
from src.services import PyRPCService

if __name__ == '__main__':
    logger = init_logger('DawnPy')
    model_path = os.path.join(os.getcwd(), 'models')
    service = PyRPCService(model_path)
    if not service.Initialize():
        logger.error('Failed to load model')
        exit(1)
    
    service.StartServer(int(os.environ.get("PORT", 8080)))

