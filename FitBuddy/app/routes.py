from pathlib import Path
from fastapi import APIRouter,Depends,Form,HTTPException,Request
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import get_db
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .models import User,WorkoutPlan
from .schemas import FeedbackRequest,UserInput
from .updated_plan import update_workout_plan
router=APIRouter()
templates=Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent/'templates'))
@router.get('/',response_class=HTMLResponse)
def home(request:Request): return templates.TemplateResponse(request=request,name='index.html',context={'title':'FitBuddy'})
@router.post('/generate-workout',response_class=HTMLResponse)
def generate_workout(request:Request,name:str=Form(...),user_id:str=Form(...),age:int=Form(...),weight:float=Form(...),goal:str=Form(...),intensity:str=Form(...),db:Session=Depends(get_db)):
    try:u=UserInput(name=name,user_id=user_id,age=age,weight=weight,goal=goal,intensity=intensity)
    except Exception as e:return templates.TemplateResponse(request=request,name='error.html',context={'title':'Invalid input','message':str(e)},status_code=400)
    user=db.scalar(select(User).where(User.user_id==u.user_id))
    if user:
        user.name,user.age,user.weight,user.goal,user.intensity=u.name,u.age,u.weight,u.goal,u.intensity
        for p in list(user.plans):db.delete(p)
    else:user=User(**u.model_dump());db.add(user)
    try:
        workout=generate_workout_gemini(u.name,u.age,u.weight,u.goal,u.intensity);tip=generate_nutrition_tip_with_flash(u.goal,u.age)
    except Exception as e:
        db.rollback();return templates.TemplateResponse(request=request,name='error.html',context={'title':'AI generation error','message':f'{e} Check GOOGLE_API_KEY/model names or set DEMO_MODE=true.'},status_code=502)
    plan=WorkoutPlan(user_id=u.user_id,original_plan=workout,nutrition_tip=tip);db.add(plan);db.commit()
    return templates.TemplateResponse(request=request,name='result.html',context={'title':'Your FitBuddy Plan','user':user,'plan':plan,'active_plan':workout,'message':None})
@router.post('/submit-feedback',response_class=HTMLResponse)
def feedback(request:Request,user_id:str=Form(...),feedback:str=Form(...),db:Session=Depends(get_db)):
    try:r=FeedbackRequest(user_id=user_id,feedback=feedback)
    except Exception as e:return templates.TemplateResponse(request=request,name='error.html',context={'title':'Invalid feedback','message':str(e)},status_code=400)
    user=db.scalar(select(User).where(User.user_id==r.user_id))
    if not user:raise HTTPException(404,'User ID was not found.')
    plan=db.scalar(select(WorkoutPlan).where(WorkoutPlan.user_id==user.user_id).order_by(WorkoutPlan.id.desc()))
    if not plan:raise HTTPException(404,'No workout plan was found.')
    try:
        revised=update_workout_plan(plan.original_plan,r.feedback,user.goal,user.intensity,user.age,user.name);plan.updated_plan=revised;plan.feedback=r.feedback;db.commit()
    except Exception as e:
        db.rollback();return templates.TemplateResponse(request=request,name='error.html',context={'title':'Plan update error','message':str(e)},status_code=502)
    return templates.TemplateResponse(request=request,name='result.html',context={'title':'Updated FitBuddy Plan','user':user,'plan':plan,'active_plan':revised,'message':'Your feedback was processed and the plan was updated.'})
@router.get('/view-all-users',response_class=HTMLResponse)
def all_users(request:Request,db:Session=Depends(get_db)):
    users=db.scalars(select(User).order_by(User.id.desc())).all();return templates.TemplateResponse(request=request,name='all_users.html',context={'title':'All Users','users':users})
@router.get('/api/users')
def api_users(db:Session=Depends(get_db)):
    return [{'id':u.id,'user_id':u.user_id,'name':u.name,'age':u.age,'weight':u.weight,'goal':u.goal,'intensity':u.intensity} for u in db.scalars(select(User).order_by(User.id.desc())).all()]
@router.get('/api/users/{user_id}')
def api_user(user_id:str,db:Session=Depends(get_db)):
    u=db.scalar(select(User).where(User.user_id==user_id))
    if not u:raise HTTPException(404,'User not found.')
    return {'user':{'user_id':u.user_id,'name':u.name,'age':u.age,'weight':u.weight,'goal':u.goal,'intensity':u.intensity},'plans':[{'id':p.id,'original_plan':p.original_plan,'updated_plan':p.updated_plan,'nutrition_tip':p.nutrition_tip,'feedback':p.feedback} for p in u.plans]}
@router.delete('/api/users/{user_id}',response_class=JSONResponse)
def delete_user(user_id:str,db:Session=Depends(get_db)):
    u=db.scalar(select(User).where(User.user_id==user_id))
    if not u:raise HTTPException(404,'User not found.')
    db.delete(u);db.commit();return {'message':f'User {user_id} deleted successfully.'}
