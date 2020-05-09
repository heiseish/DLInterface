#!/usr/bin/env python3

import pstats, cProfile
import os

from src.model import DialoGPT

model_path = os.path.join(os.getcwd(), 'models', 'medium_ft.pkl')
model = DialoGPT(model_path.encode())
assert(model.Initialize())

input_text = 'hey who are you'
cProfile.runctx("model.GenerateFor(input_text)", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()
