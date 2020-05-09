# distutils: language=c++
# cython: language_level=3

import os
import torch
import torch.nn.functional as F
from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPT2Config
from ..utils import get_logger

import cython
from libc.stdlib cimport free, malloc
from libc.string cimport strcpy, strlen
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string

__all__ = [
    'DialoGPT'
]

cdef class BaseDialoGPT:
    cdef string network_path
    cdef string device
    cdef int end_token 
    cdef vector[int] conditioned_tokens
    cdef vector[int] generated_tokens

    @cython.wraparound(False)
    @cython.nonecheck(False)
    def __cinit__(self, string network_path = b'', string device = b'cpu') :
        ''' Init dialoGPY
        Args:
        - network_path (str) path to the pkl file
        - device (str) one of cpu | cuda
        '''
        self.network_path = network_path
        self.device = device
        self.end_token = 50256

        self.logger = get_logger()
        self.tokenizer = None
        self.model = None
        

    def __dealloc__(self):
        pass

    def Initialize(self):
        ''' Load model and tokenizer for gpt model
        '''
        if not os.path.isfile(self.network_path):
            self.logger.error('Network path doesnt exist')
            return False
        cdef dict weights

        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        try:
            weights = torch.load(self.network_path.decode())
        except Exception as e:
            self.logger.error('Failed to load network: {}'.format(e))
            return False

        medium_config = GPT2Config(n_embd=1024,n_layer=24,n_head=16)
        self.model = GPT2LMHeadModel(medium_config)

        # fix misused key value
        weights["lm_head.weight"] = weights["lm_head.decoder.weight"]
        weights.pop("lm_head.decoder.weight",None)

        self.model.load_state_dict(weights)
        self.model.eval()
        self.model.to(self.device.decode())
        self.logger.info('Model initialized successfully!')
        return True

    cdef void reinput(self, str text) except *:
        cdef vector[int] encoded_res

        self.conditioned_tokens.clear()
        encoded_res = self.tokenizer.encode(text)
        self.conditioned_tokens.insert(self.conditioned_tokens.begin(),
            encoded_res.begin(), encoded_res.end())
        self.conditioned_tokens.push_back(self.end_token)


    cdef top_p_filtering(self, logits: torch.Tensor, 
        double top_p = 0.9, double filter_value =-float('Inf')):
        """
        Credit: https://gist.github.com/thomwolf/1a5a29f6962089e871b94cbd09daf317
        """
        assert logits.dim() == 1  # batch size 1 for single word generation
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
        # remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        # shift the indices to the right to keep also the first token above the threshold
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0
        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[indices_to_remove] = filter_value
        return logits


    cdef int recalc(self) except *:
        # for segment display purpose, keep 2 sets of tokens
        cdef vector[int] indexed_tokens
        next_token: torch.Tensor

        indexed_tokens.insert(indexed_tokens.end(), self.conditioned_tokens.begin(), self.conditioned_tokens.end())
        indexed_tokens.insert(indexed_tokens.end(), self.generated_tokens.begin(), self.generated_tokens.end())
        tokens_tensor = torch.tensor([indexed_tokens])
        tokens_tensor = tokens_tensor.to(self.device)
        with torch.no_grad():
            outputs = self.model(tokens_tensor)
            predictions = outputs[0]
        logits = predictions[0, -1, :]
        filtered_logits = self.top_p_filtering(logits)
        probabilities = F.softmax(filtered_logits, dim=-1)
        next_token = torch.multinomial(probabilities, 1)
        self.generated_tokens.push_back(next_token.item())
        return next_token.item()

    cdef str generate(self):
        ''' generate a response using `self.conditioned_tokens` and `self.generated_token`
        '''
        cdef str response
        cdef int result
        while True:
            result = self.recalc()
            if result == 50256:
                # end-of-text : 50256
                # use this special token to split segments
                response = self.tokenizer.decode(self.generated_tokens[:-1])
                self.conditioned_tokens.insert(self.conditioned_tokens.end(), self.generated_tokens.begin(), self.generated_tokens.end())
                self.generated_tokens.clear()
                break
        return response
    
    def GetNext(self) -> str:
        ''' Keep generating for current `self.conditioned_tokens` and `self.generated_token`
        '''
        return self.generate()

    def GenerateFor(self, text:str, times:int = 2):
        ''' Generate a sequence in response to @code `text`
        Args:
        - text (str) text to start generation
        - times (str) number of times to try to generate
        '''
        self.reinput(text)
        cdef str res = ''
        for _ in range(times):
            res += '{}. '.format(self.generate())
        return res

class DialoGPT(BaseDialoGPT):
    pass