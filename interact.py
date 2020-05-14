#!/usr/bin/env python
import os
from src.model.DialoGPT import DialoGPT
from src.utils import init_logger

if __name__ == '__main__':  
    logger = init_logger('DawnPy')
    model_path = os.path.join(os.getcwd(), 'models')
    model = DialoGPT(model_path, 'cuda')
    if not model.Initialize():
        logger.error('Failed to load model')
        exit(1)
    
    while True:
        res = input(f'User: ')
        if res:
            model.reinput(res)
        print(f'Bot: {model.GetNext()}')