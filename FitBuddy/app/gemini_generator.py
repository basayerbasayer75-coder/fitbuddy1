import os
from dotenv import load_dotenv
load_dotenv()
SAFETY="""You are a wellness-planning assistant. Give general, age-appropriate fitness guidance. Do not diagnose, prescribe medicine/supplements, give dangerous exercise instructions, extreme dieting, calorie-cutting targets, starvation advice, or rapid weight-loss targets. For users under 18, avoid weight-loss coaching and emphasize safe movement, recovery, enjoyment, and adult/professional support. Always include recovery."""
def _demo_plan(name,goal,intensity,age):
    note="For younger users, prioritize supervision, technique, recovery and enjoyment." if age<18 else "Adjust exercises to ability and stop if you feel pain or dizziness."
    return f"""FITBUDDY 7-DAY WELLNESS PLAN FOR {name.upper()}

Goal: {goal}
Preferred intensity: {intensity}

Day 1 – Full Body Foundation
Warm-up: 5–10 minutes easy walking and mobility.
Main: Bodyweight squats, wall/incline push-ups, glute bridges and gentle plank holds.
Cooldown: 5 minutes gentle stretching.

Day 2 – Light Cardio & Mobility
Comfortable walking/cycling plus gentle mobility.

Day 3 – Upper Body & Core
Incline push-ups, resistance-band rows if available, dead-bugs and bird-dogs.

Day 4 – Recovery Day
Easy walk, light stretching, sleep and hydration focus.

Day 5 – Lower Body & Core
Comfortable squats, step-ups, glute bridges, calf raises and gentle core work.

Day 6 – Fun Cardio
Choose walking, cycling, dancing or a recreational sport at a comfortable effort.

Day 7 – Recovery & Reflection
Easy mobility and a relaxed walk if desired.

Safety note: {note}"""
def _gemini(prompt,model):
    key=os.getenv("GOOGLE_API_KEY","").strip()
    if not key: raise RuntimeError("GOOGLE_API_KEY is not configured.")
    from google import genai
    client=genai.Client(api_key=key)
    r=client.models.generate_content(model=model,contents=prompt)
    text=getattr(r,"text",None)
    if not text: raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
def generate_workout_gemini(name,age,weight,goal,intensity):
    demo=os.getenv("DEMO_MODE","true").lower()=="true"
    if demo and not os.getenv("GOOGLE_API_KEY","").strip(): return _demo_plan(name,goal,intensity,age)
    prompt=f"""{SAFETY}
Generate a structured 7-day general wellness plan for Name={name}, Age={age}, Weight={weight} kg, Goal={goal}, Intensity={intensity}. Include Day 1–7, warm-up/main/cooldown where active, at least one recovery day, practical sets/reps or time, and plain-text headings. Do not provide calorie targets or extreme weight-loss instructions."""
    try: return _gemini(prompt,os.getenv("GEMINI_WORKOUT_MODEL","gemini-2.5-flash"))
    except Exception:
        if demo: return _demo_plan(name,goal,intensity,age)
        raise
