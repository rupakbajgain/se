import google.generativeai as genai
from ...config import getConfig
from langchain_community.chat_models import ChatOllama

config=getConfig()
genai.configure(api_key=config['api']['GEMINI'])

models=["gemini-1.5-flash","gemini-1.5-pro","gemini-1.0-pro"]
limits=[15,2,15]
import time

request_counts = {model: [] for model in models}

def get_available_model():
    current_time = time.time()
    for model, limit in zip(models, limits):
        # Remove timestamps older than 60 seconds
        request_counts[model] = [timestamp for timestamp in request_counts[model] if current_time - timestamp < 60]
        if len(request_counts[model]) < limit:
            request_counts[model].append(current_time)
            return model
    return False

def local_model(msg):
    model_name = "gemma2:2b"
    model = ChatOllama(model=model_name)
    r=model.invoke(msg)
    return r.content

def get_response(msg):
    model=get_available_model()
    if not model:
        return local_model(msg)
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(msg)
        return response.text
    except:
        return local_model(msg)