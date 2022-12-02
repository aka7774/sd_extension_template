import asyncio
from typing import Optional

import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel

import modules.script_callbacks as script_callbacks


class TemplateParameters(BaseModel):
    example_flag: Optional[bool] = False

def templateAPI(demo: gr.Blocks, app: FastAPI):
    @app.post("/template/run")
    async def templateRun(example_flag):
        print("Starting template run")

script_callbacks.on_app_started(templateAPI)

print("Template API layer loaded")
