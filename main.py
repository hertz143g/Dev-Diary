from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine, Base
from typing import List

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/entries", response_model=schemas.EntryOut)
def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    new = models.Entry(**entry.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@app.get("/entries", response_model=List[schemas.EntryOut])
def get_entries(tag: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Entry)
    if tag:
        query = query.filter(models.Entry.tags.any(tag))
    return query.order_by(models.Entry.created_at.desc()).all()

@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.Entry).get(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(entry)
    db.commit()
    return {"message": "Deleted"}
