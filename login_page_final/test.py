import google.generativeai as genai

genai.configure(api_key="AIzaSyDuNCt9U-RBn4pNOXS_focEyMH1hmT8q2c")

models = genai.list_models()
for model in models:
    print(model.name)
