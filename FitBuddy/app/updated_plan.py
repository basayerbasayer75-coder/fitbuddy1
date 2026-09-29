import os
from dotenv import load_dotenv
from .gemini_generator import _demo_plan,_gemini
load_dotenv()
def update_workout_plan(original_plan,feedback,goal,intensity,age,name):
    demo=os.getenv("DEMO_MODE","true").lower()=="true"
    if demo and not os.getenv("GOOGLE_API_KEY","").strip(): return _demo_plan(name,goal,intensity,age)+"\n\nRequested feedback considered: "+feedback.replace("\n"," ")
    prompt=f"""Revise this general wellness plan safely. Original plan:
{original_plan}

User feedback:
{feedback}

Profile: {name}, age {age}, goal {goal}, intensity {intensity}. Keep it age-appropriate. Do not introduce dangerous exercise, extreme dieting, calorie targets or rapid weight-loss targets. Include recovery. For under 18 avoid weight-loss coaching. Return a complete revised 7-day plan."""
    try:return _gemini(prompt,os.getenv("GEMINI_WORKOUT_MODEL","gemini-2.5-flash"))
    except Exception:
        if demo:return _demo_plan(name,goal,intensity,age)
        raise
