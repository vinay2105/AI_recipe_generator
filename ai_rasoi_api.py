from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# ✅ Configure Gemini API Key
genai.configure(api_key=os.getenv("api_key"))

model_name = "gemini-1.5-flash"

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

Your job:
- Suggest a traditional Indian recipe using mostly these ingredients.
- Be healthy and low-oil.
- Include: Dish name, Steps, Calories (estimate), Spice level (1–5), Regional style (e.g. South Indian, Punjabi)
- Add a friendly mom-style cooking tip
- Provide approximate amount of protein, carbohydrates, fats, and fibre.

Important Rules:
- If the request is irrelevant or not related to food or cooking (like jokes, poems, tech queries, etc), politely reply: "❌ Sorry, I only help with desi food recipes. Please provide ingredients."
- If ingredients are clearly invalid or empty, politely say: "❌ No valid ingredients found. Please list some food ingredients to get a recipe."

Be casual and friendly.

Now, generate the response accordingly.
"""
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    return response.text  # plain text response

# ✅ API Route
@app.post("/generate_recipe", response_model=RecipeResponse)
async def get_recipe(request: RecipeRequest):
    recipe_text = generate_recipe(request.ingredients, request.preferences)
    return {"recipe": recipe_text}






