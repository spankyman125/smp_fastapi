from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import dependencies, filldata

router = APIRouter()

@router.get("/")
async def root():
	return {"test":"test"}

@router.get("/filldata/")
def fill_with_test_data(db: Session = Depends(dependencies.get_db)):
    filldata.fill_testdata(db)
    return True