import os
from dotenv import load_dotenv
from .gemini_generator import _gemini
load_dotenv()
def _demo_tip(goal):
    return {"weight loss":"Choose regular balanced meals with vegetables, fruit, whole grains and a protein source; avoid extreme dieting.","muscle gain":"Include a protein-rich food in regular meals and prioritize sleep and recovery.","general wellness":"Stay hydrated, eat a varied diet, move regularly and keep a consistent sleep routine.","flexibility":"Hydrate and include gentle mobility work regularly; never force a stretch into pain."}.get(goal,"Stay hydrated and prioritize balanced meals and recovery.")
def generate_nutrition_tip_with_flash(goal,age):
    demo=os.getenv("DEMO_MODE","true").lower()=="true"
    if demo and not os.getenv("GOOGLE_API_KEY","").strip(): return _demo_tip(goal)
    prompt=f"Give one concise practical nutrition/recovery tip for goal={goal}, age={age}. No calorie targets, restrictive dieting, supplement dosing or medical advice. For under 18, avoid weight-loss advice and emphasize balanced meals, hydration, sleep and adult/professional support. Return 2–4 sentences."
    try: return _gemini(prompt,os.getenv("GEMINI_TIP_MODEL","gemini-2.5-flash"))
    except Exception:
        if demo:return _demo_tip(goal)
        raise
