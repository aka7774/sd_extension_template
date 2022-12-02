# This file is always executed

import gradio as gr

from modules import script_callbacks, sd_models, shared


def tpl_button_click(tpl_textbox):
    print(f"Hello {tpl_textbox}")

def on_ui_tabs():
    with gr.Blocks() as template_interface:
        with gr.Row(equal_height=True):
            with gr.Column():
                tpl_model_dir = gr.Dropdown(label='ABC', choices=["a","b","c"])
                tpl_checkbox = gr.Checkbox(label="Check", value=False)
                tpl_textbox = gr.Textbox(label="Your Name")
                tpl_button = gr.Button(value='Push me')
                tpl_number = gr.Number(label='Number', value=1000, precision=0)
                tpl_image = gr.Image()

        tpl_button.click(
            fn=tpl_button_click,
            inputs=[tpl_textbox],
            outputs=[]
        )

    return (template_interface, "Template", "template_interface"),


script_callbacks.on_ui_tabs(on_ui_tabs)
