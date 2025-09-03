from django.apps import AppConfig

import Model.globals as globals
from openai import OpenAI
from transformers import pipeline

import torch

class PromptcontrollerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Controller.promptController'

    def ready(self):
        globals.deepseek = OpenAI(api_key="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",
                                 base_url="https://openrouter.ai/api/v1")