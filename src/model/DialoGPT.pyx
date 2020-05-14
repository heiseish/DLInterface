#cython: language_level=3, c_string_type=unicode, c_string_encoding=utf8, boundscheck=False, cdivision=True, wraparound=False
# distutils: language=c++
import os
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelWithLMHead
from src.utils.logger import get_logger
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp.string cimport string

__all__ = [
    'DialoGPT'
]

cdef class BaseDialoGPT:
    cdef:
        string network_path
        string device
        # int end_token 
        vector[int] conditioned_tokens
        vector[int] generated_tokens
        object logger
        object tokenizer
        object model

    def __cinit__(self, string network_path = b'', string device = b'cpu') :
        ''' Init dialoGPY
        Args:
        - network_path (str) path to the pkl file
        - device (str) one of cpu | cuda
        '''
        self.network_path = network_path
        self.device = device
        # self.end_token = 50256
        self.logger = get_logger()
        self.tokenizer = None
        self.model = None
        

    def __dealloc__(self):
        pass

    cpdef bool Initialize(self) except*:
        ''' Load model and tokenizer for gpt model
        '''
        cdef:
            dict weights
        os.makedirs(self.network_path, exist_ok=True)
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large", cache_dir=self.network_path)
        self.model = AutoModelWithLMHead.from_pretrained("microsoft/DialoGPT-large", cache_dir=self.network_path)
        # Set the model in evaluation mode to deactivate the DropOut modules
        # This is IMPORTANT to have reproducible results during evaluation!
        self.model.eval()
        self.model.to(self.device)
        self.logger.info('Model initialized successfully!')
        return True

    cpdef void reinput(self, string text):
        cdef vector[int] encoded_res

        self.conditioned_tokens.clear()
        encoded_res = self.tokenizer.encode(text)
        self.conditioned_tokens.insert(self.conditioned_tokens.begin(), 
            encoded_res.begin(), encoded_res.end())
        self.conditioned_tokens.push_back(int(self.tokenizer.eos_token_id))


    cdef object top_p_filtering(self, object logits, 
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
        cdef:
            vector[int] indexed_tokens
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

    cdef string generate(self):
        ''' generate a response using `self.conditioned_tokens` and `self.generated_token`
        '''
        cdef:
            string response
            int result
        while True:
            result = self.recalc()
            if result == int(self.tokenizer.eos_token_id):
                # end-of-text : 50256
                # use this special token to split segments
                response = self.tokenizer.decode(self.generated_tokens[:-1])
                self.conditioned_tokens.insert(self.conditioned_tokens.end(), self.generated_tokens.begin(), self.generated_tokens.end())
                self.generated_tokens.clear()
                break
        return response
    
    cpdef string GetNext(self):
        ''' Keep generating for current `self.conditioned_tokens` and `self.generated_token`
        '''
        return self.generate()

    cpdef string GenerateFor(self, string text, int times = 2):
        ''' Generate a sequence in response to @code `text`
        Args:
        - text (str) text to start generation
        - times (str) number of times to try to generate
        '''
        cdef:
            string res = b''
            string nxt

        self.reinput(text)
        for _ in range(times):
            nxt = f'{self.generate()}\n'
            res.append(nxt)
        return res

class DialoGPT(BaseDialoGPT):
    pass

    # Let's chat for 5 lines
# for step in range(5):
    # # encode the new user input, add the eos_token and return a tensor in Pytorch
    # new_user_input_ids = tokenizer.encode(input(">> User:") + tokenizer.eos_token, return_tensors='pt')

    # # append the new user input tokens to the chat history
    # bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # # generated a response while limiting the total chat history to 1000 tokens, 
    # chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # # pretty print last ouput tokens from bot
    # print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))