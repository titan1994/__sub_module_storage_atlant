from .models import ExampleModel
from tortoise.contrib.pydantic import pydantic_model_creator
PYD_ExampleModel = pydantic_model_creator(ExampleModel)

