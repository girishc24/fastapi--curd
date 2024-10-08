from typing import Union, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class Book(BaseModel):
     id : UUID
     title : str = Field(min_length=1)
     author : str = Field(min_lenght=1, max_length=100)
     description : str = Field(min_length=1, max_length=100)
     rating: int = Field(gt=-1, lt=101)

BOOKS = []

class Task(BaseModel):
     id : Optional[UUID] = None 
     title : str = Field(min_length=1)
     description : Optional[str] = Field(min_length=1)
     compeleted : bool = False

TASKS = []

class ChoiceBase(BaseModel):
     choice_text : str
     is_correct : bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase] 

def get_db():
     db =SessionLocal()
     try:
          yield db
     finally:
          db.close()

db_dependency = Depends(get_db)


@app.get("/questions/{question_id}")
async def read_questions(question_id: int, db: Session = db_dependency):
     result =db.query(models.Questions).filter(models.Questions.id == question_id).first()
     if not result:
          raise HTTPException(status_code=404, detail='Question is not found')
     return result

@app.get("/choices/{question_id}")
async def read_questions(question_id: int, db: Session = db_dependency):
     result =db.query(models.Questions).filter(models.Choices.id == question_id)
     if not result:
          raise HTTPException(status_code=404, detail='Question is not found')
     return result

@app.post("/questions")
async def create_questions(questions: QuestionBase, db: Session = db_dependency):
    db_question = models.Questions(question_text=questions.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in questions.choices:
        db_choice = models.Choices(
            choices_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id
        )
        db.add(db_choice)

    db.commit()
    return {"question_id": db_question.id, "question_text": db_question.question_text}





@app.get("/")
def read_root():
    return {"Greeting": "Welcome Girish"}


#TASK Session
@app.post("/task/", response_model=Task)
def create_task(task : Task):
     task.id = uuid4()
     TASKS.append(task)
     return task


@app.get("/task/", response_model=List[Task])
def get_tasks():
    return TASKS


@app.get("/task/{task_id}/", response_model=Task)
def get_task(task_id : UUID):
    for task in TASKS:
         if task.id == task_id:
              return task
    return HTTPException(
         status_code= 404,
         detail=f"ID {task_id} : is not found in List"
    )


@app.put("/task/{task_id}/", response_model=Task)
def updated_task(task_id: UUID, task_update: Task):
    for idx, task in enumerate(TASKS):
        if task.id == task_id:
            # Use Pydantic's .copy() to merge updates with existing task data
            updated_task = task.copy(update=task_update.dict(exclude_unset=True))
            TASKS[idx] = updated_task
            return updated_task
    
    # If no task with the given ID is found, raise 404
    raise HTTPException(
        status_code=404,
        detail=f"ID {task_id} does not exist"
    )

@app.delete('/task/{task_id}/', response_model=Task)
def delete_task(task_id: UUID):
    for idx, task in enumerate(TASKS):
        if task.id == task_id:
            deleted_task = TASKS.pop(idx)  # Remove the task from the list
            return deleted_task  # Return the deleted task
    
    # If no task with the given ID is found, raise 404
    raise HTTPException(
        status_code=404,
        detail=f"ID {task_id} does not exist"
    )

# Book Session
@app.post("/book/")
def createbook(book: Book):
     BOOKS.append(book)
     return book


@app.get("/book/")
def getbook():
     return BOOKS

@app.put("/book/{book_id}")
def update_book(book_id: UUID, book : Book):
     counter = 0
     for x in BOOKS:
          counter += 1
          if x.id == book.id:
               BOOKS[counter - 1] = book
               return BOOKS[counter - 1]
     raise HTTPException(
          status_code=404,
          detail=f"ID {book_id} : Does not Exist"
     )

@app.delete("/book/{book_id}")
def delete_book(book_id: UUID):
     counter = 0 
     for x in BOOKS:
          counter += 1
          if x.id == book_id:
               del BOOKS[counter - 1]
               return f"ID : {book_id} deleted"
     raise HTTPException(
          status_code=404,
          detail=f"ID {book_id} : Does not Exist"
     )
     
     
# Query Parmeter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    if q:
            return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# Parmeter
@app.get("/itemview/{item_name}")
def get_item(item_name :str):
    return {"item_name": item_name}

# if __name__ == "__main__":
#      import uvicorn

#      uvicorn.run(app, host="0.0.0.0", port=800)