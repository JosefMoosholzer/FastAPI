from .. import models, schemas, utils, errors
from ..database import get_db
from sqlalchemy.orm import Session

from fastapi import status, HTTPException, Depends, APIRouter

router = APIRouter()

# Create
@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    try:
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    
        return new_user
    except (errors.UniqueViolation, errors.IntegrityError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='E-Mail already in use!')



# Read
@router.get('/users/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} does not exist')
    return user