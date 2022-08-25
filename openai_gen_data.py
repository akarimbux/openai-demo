from itertools import product 
import random
import pandas as pd
import time
import pickle
import os

from api_utils import *
from keys import *
from seed import *

# check for keys, exit and raise exception
if not gpt_key:
    raise Exception("Tokens cannot be empty, please add to keys.py")

# pick 9 random seed phrases from the combination
random_prompt_seeds = random.sample([p for p in product(objects, scenes)], 9)
result = [{'object':i[0],'prompt': 'describe an image of a ' + i[0] + connecting_term + i[1]} for i in random_prompt_seeds]

ca = CompletionsAPI(gpt_key)
ta = TasksAPI(dalle_key)

for i in result:
    response = ca.getPromptResult(i['prompt'])
    i['gpt3_prompt'] = response.replace('\n', '')
    # prevent overloading the task creation endpoint
    time.sleep(10)
    i['task_id'] = ta.createTask(i['gpt3_prompt'])
    while ta.getStatus(i['task_id']) == 'pending':
        # greedy check for task completion
        time.sleep(10)
    else:
        if ta.getStatus(i['task_id']) == 'failed':
            continue
        else:
            i['img_paths'] = ta.getImagePaths(i['task_id'])
            i['images'] = [ta.downloadImage(k) for k in i['img_paths']]  

fn = 'archive/grid_' + str(time.monotonic_ns()) + '.pkl'

with open(fn, 'wb') as f:
    pickle.dump(result, f)
