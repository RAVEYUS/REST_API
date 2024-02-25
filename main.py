from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import JSONResponse
from database import Base, engine, SessionLocal
import models
from sqlalchemy.orm import Session
from pydantic import BaseModel


Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserSchema(BaseModel):
  
    Header:str
    Body:str
    class Config:
        orm_mode=True

@app.get("/users", response_model=list[UserSchema], summary="fetch the list of all tasks")
def get(db:Session=Depends(get_db)):
    return db.query(models.users).all()

@app.get("/users/{user_id}", response_model=list[UserSchema], summary="fetch a particular task by their id")
def get(user_id: int, db:Session=Depends(get_db)):

    try:
        u = db.query(models.users).filter(models.users.id == user_id).first()
        return u
    except:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/users", response_model=UserSchema,summary= "Add a new task")
def post(user:UserSchema,db:Session=Depends(get_db)):
    u=models.users(Header=user.Header,Body=user.Body)
    db.add(u)
    db.commit()
    return u

@app.put("/users/{user_id}", response_model=UserSchema,summary= "Update an existing task")
def update_user(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    try:
        u = db.query(models.users).filter(models.users.id == user_id).first()
        u.Header = user.Header
        u.Body = user.Body
        db.add(u)
        db.commit()
        return u
    except:
        raise HTTPException(status_code=404, detail="User not found")
    
class DeleteResponse(BaseModel):
    message: str

@app.delete("/users/{user_id}", response_model=DeleteResponse, summary="Delete a user by id")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    try:
        user_to_delete = db.query(models.users).filter(models.users.id == user_id).first()
        db.delete(user_to_delete)
        db.commit()
        return DeleteResponse(message=f"User with id {user_id} deleted successfully")
    except:
        raise HTTPException(status_code=404, detail="User not found")