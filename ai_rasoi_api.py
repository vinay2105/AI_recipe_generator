from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

# ✅ Configure Gemini API Key
genai.configure(api_key="AIzaSyCq-9E_exJEB7d6hx1822dXmrxnVG2Foyg")

# ✅ Get Available Models
models = genai.list_models()
available_models = [model.name for model in models]
model_name = 'models/gemini-1.5-pro' if 'models/gemini-1.5-pro' in available_models else available_models[0]

# ✅ FastAPI App
app = FastAPI(
    title="AI Rasoi Recipe API 🍛",
    description="An API that generates desi recipes based on ingredients using Gemini AI",
    version="1.0.0"
)

# ✅ Request Schema
class RecipeRequest(BaseModel):
    ingredients: str
    preferences: str = "Less spicy, Punjabi style"

# ✅ Response Schema
class RecipeResponse(BaseModel):
    recipe: str

# ✅ Recipe Generation Function
def generate_recipe(ingredients, preferences):
    prompt = f"""
You are a desi home-cook AI. A user has these ingredients: {ingredients}.
Preferences: {preferences}.

Suggest a traditional Indian recipe that:
- Uses mostly these ingredients
- Is healthy and low-oil
- Includes: Dish name, Steps, Calories (estimate), Spice level (1–5), Regional style (e.g. South Indian, Punjabi)
- Add a friendly mom-style cooking tip
- Also tell approximate amount of protein, carbohydrates, fats and fibre.

Be casual and friendly like an Indian mom talking to her kid.
"""
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    return response.text  # plain text response

# ✅ API Route
@app.post("/generate_recipe", response_model=RecipeResponse)
async def get_recipe(request: RecipeRequest):
    recipe_text = generate_recipe(request.ingredients, request.preferences)
    return {"recipe": recipe_text}






