import gradio as gr
import pickle
import random
import numpy as np
import sys

fn = sys.argv[1]
with open(fn, 'rb') as f:
    grid = pickle.load(f)

# randomize grid so things load in different places
shuffled = random.sample(grid, len(grid))

# set target for an object prompt, match a set of indices
objects = [(key, value) for i in shuffled for key, value in i.items() if key=='object']
pick = random.choice(objects)[1]
target_array = [idx for idx, obj in enumerate(objects) if obj[1] == pick] 

# check array function
def check_array(image_nums):
    my_list = list(map(int,image_nums))
    return "Yes, you got it!" if sorted(my_list) == sorted(target_array) else "No, try again!"

# display result
def display_result(image_nums):
    return sorted(target_array)

with gr.Blocks() as demo:
    gr.Markdown("Which of the images below contain a:")
    gr.Textbox(pick, show_label=False)
    with gr.Column():
        with gr.Row():
            for i in range(0,3):
                # a random image is picked from the batch result
                gr.Image(shuffled[i]['images'][np.random.randint(0,4)], label=str(i), show_label=True)
        with gr.Row():
            for i in range(3,6):
                gr.Image(shuffled[i]['images'][np.random.randint(0,4)], label=str(i), show_label=True)
        with gr.Row():
            for i in range(6,9):
                gr.Image(shuffled[i]['images'][np.random.randint(0,4)], label=str(i), show_label=True)
    input_image = gr.CheckboxGroup(label="Enter image labels", choices=['0','1','2','3','4','5','6','7','8'])
    click_result = gr.Textbox(label="Did you get it?")
    btn = gr.Button("Submit")   
    btn.click(fn=check_array, inputs=input_image, outputs=click_result)
    show_result = gr.Textbox(label="Expected images are")
    result = gr.Button("Show Result")   
    result.click(fn=display_result, inputs=input_image, outputs=show_result)
demo.launch()