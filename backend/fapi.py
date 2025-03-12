from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is working!"}
    
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

game_state = {
    "numbers": [random.randint(1, 10) for _ in range(5)],
    "selected_numbers": [],
    "sum": 0,
    "target": random.randint(10, 20),
    "status": "Select numbers to match the target!",
    "scale_tilt": "balanced",
}


class NumberSelection(BaseModel):
    num: int

@app.get("/game-state")
async def get_game_state():
    """Fetch the current game state."""
    return game_state

@app.post("/select-number")
async def select_number(selection: NumberSelection):
    """Handle number selection logic."""
    num = selection.num
    if num in game_state["selected_numbers"]:
        return {"message": "Number already selected!"}
    
    game_state["selected_numbers"].append(num)
    game_state["sum"] += num

    
    if game_state["sum"] < game_state["target"]:
        game_state["scale_tilt"] = "left"
        game_state["status"] = "Too low! Add more."
    elif game_state["sum"] > game_state["target"]:
        game_state["scale_tilt"] = "right"
        game_state["status"] = "Too high! Remove numbers."
    else:
        game_state["scale_tilt"] = "balanced"
        game_state["status"] = "Correct! You matched the target."

    return game_state

@app.post("/reset-game")
async def reset_game():
    """Reset the game with new random numbers and a target."""
    game_state["numbers"] = [random.randint(1, 20) for _ in range(5)]
    game_state["selected_numbers"] = []
    game_state["sum"] = 0
    game_state["target"] = random.randint(10, 50)
    game_state["status"] = "Select numbers to match the target!"
    game_state["scale_tilt"] = "balanced"

    return game_state
