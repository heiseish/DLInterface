import os
import torch
import torch.nn.functional as F
from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPT2Config
from ..utils import get_logger

__all__ = [
    'DialoGPT'
]
class DialoGPT:
    end_token = 50256
    def __init__(self, network_path: str='', device='cpu'):
        ''' Init dialoGPY
        Args:
        - network_path (str) path to the pkl file
        - device (str) one of cpu | cuda
        '''
        self.network_path = network_path
        self.logger = get_logger()
        self.device = device
        self.tokenizer = None
        self.model = None
        self.conditioned_tokens = []
        self.generated_tokens = []

    def Initialize(self):
        self.logger.title('Initializing DialoGPT')
        if not os.path.isfile(self.network_path):
            self.logger.error('Network path doesnt exist')
            return False

        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        try:
            weights = torch.load(self.network_path)
        except Exception as e:
            self.logger.error('Failed to load network')
            return False

        medium_config = GPT2Config(n_embd=1024,n_layer=24,n_head=16)
        self.model = GPT2LMHeadModel(medium_config)

        # fix misused key value
        weights["lm_head.weight"] = weights["lm_head.decoder.weight"]
        weights.pop("lm_head.decoder.weight",None)

        self.model.load_state_dict(weights)
        self.model.eval()
        self.model.to(self.device)
        self.logger.end_section()
        return True

    def reinput(self, text: str):
        self.conditioned_tokens = self.tokenizer.encode(text) + [DialoGPT.end_token]


    def top_p_filtering(self, logits: torch.Tensor, top_p:float = 0.9, filter_value: float =-float('Inf')):
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


    def recalc(self):
        # for segment display purpose, keep 2 sets of tokens
        indexed_tokens = self.conditioned_tokens + self.generated_tokens
        tokens_tensor = torch.tensor([indexed_tokens])
        tokens_tensor = tokens_tensor.to(self.device)
        with torch.no_grad():
            outputs = self.model(tokens_tensor)
            predictions = outputs[0]
        logits = predictions[0, -1, :]
        filtered_logits = self.top_p_filtering(logits)
        probabilities = F.softmax(filtered_logits, dim=-1)
        next_token = torch.multinomial(probabilities, 1)
        self.generated_tokens.append(next_token.item())
        return next_token.item()

    def generate(self):
        ''' generate a response using `self.conditioned_tokens` and `self.generated_token`
        '''
        response = ''
        while True:
            result = self.recalc()
            if result == 50256:
                # end-of-text : 50256
                # use this special token to split segments
                response =  self.tokenizer.decode(self.generated_tokens[:-1])
                self.conditioned_tokens += self.generated_tokens
                self.generated_tokens = []
                break
        return response
    
    def GetNext(self) -> str:
        ''' Keep generating for current `self.conditioned_tokens` and `self.generated_token`
        '''
        self.logger.title('Getting next sentence')
        return self.generate()

    def GenerateFor(self, text:str, times:int = 2):
        ''' Generate a sequence in response to @code `text`
        Args:
        - text (str) text to start generation
        - times (str) number of times to try to generate
        '''
        self.logger.title('Generating sequence')
        self.logger.info('Generate sequence for {}'.format(text))
        self.reinput(text)
        res = ''
        for _ in range(times):
            res += '{}. '.format(self.generate())
        return res