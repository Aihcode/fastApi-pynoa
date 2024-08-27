from config.app import Config
from config.auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_active_user, get_current_active_user_role, Annotated, OAuth2PasswordRequestForm, Depends, Token, get_user, HTTPException, status, User, UserRole, CustomProfile, timedelta
from orm_db import crud, schemas
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from helpers.getdb import get_db
from random import random, choice
from helpers.encryptgen import get_hashed_name
import os
auth = Config().auth

@auth.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session=Depends(get_db)
) -> Token:
    """
    Authenticates a user and generates an access token for API authorization.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends()]): The form data containing the username and password.
        db (Session, optional): The database session. Defaults to the result of the `get_db` function.

    Returns:
        Token: The access token and its type.

    Raises:
        HTTPException: If the username or password is incorrect.

    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(db,
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(token=access_token, token_type="bearer")


@auth.post("/users/")
def post_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    """
    Posts a new user to the database if the email is not already registered.

    Args:
        user (schemas.UserCreate): The user data to be created.
        db (Session): The database session.

    Returns:
        The created user data.

    Raises:
        HTTPException: If the email is already registered.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db,user=user)


@auth.put("/users/{id}", response_model=schemas.Profile)
def update_user(user:schemas.UserUpdate, id:int, db:Session=Depends(get_db), current_user=Depends(get_current_active_user)):
    """
    Update a user's profile information.

    Parameters:
        user (schemas.UserUpdate): The updated user information.
        id (int): The ID of the user to be updated.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (Depends(get_current_active_user), optional): The current active user. Defaults to Depends(get_current_active_user).

    Returns:
        schemas.Profile: The updated user profile.

    Raises:
        HTTPException: If the current user does not have enough permissions or if the user is not found.
    """
    if current_user.id != id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    db_user = crud.get_user(db, user_id=id)
    print(db_user, id, user)
    db_id = db_user.id
    r_user = user
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return crud.update_user(db=db, db_user=db_id, user=r_user)


@auth.patch("/users/{convert}", response_model=schemas.Profile)
def update_user(file: Annotated[UploadFile, File()], convert: str, db:Session=Depends(get_db), current_user=Depends(get_current_active_user)):
    """
    Updates the profile picture of a user.

    Parameters:
        file (Annotated[UploadFile, File()]): The uploaded file containing the new profile picture.
        convert (str): The file type to convert the uploaded file to. If empty, the original file type will be used.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        current_user (Depends(get_current_active_user), optional): The current active user. Defaults to Depends(get_current_active_user).

    Returns:
        schemas.Profile: The updated user profile.

    Raises:
        HTTPException: If the current user does not have enough permissions or if the user is not found.
    """
    if not current_user:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    basePatch = './static/uploads/profiles/media/'
    if not os.path.exists(basePatch):
        os.mkdir(basePatch)
        pass

    fileType = '.webp'

    if len(convert) > 0:
        fileType = '.' + convert
    

    randomId = random()
    randomChoice = choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    hashedName = get_hashed_name(str(randomId) + randomChoice + file.filename) + fileType
    fileUpload = os.path.join(basePatch, hashedName.replace('', ''))
    with open(fileUpload, "wb") as buffer:
        while contents := file.file.read(1024 * 1024):
            buffer.write(contents)

    db_user = crud.get_user(db, user_id=id)
    if db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return crud.update_user_pic(db=db, db_user=current_user.id, pic=fileUpload)

@auth.get("/users/", response_model=list[schemas.User])
def get_users(skip:int=0, limit:int=0, db:Session=Depends(get_db), current_user=Depends(get_current_active_user)):
    """
    Get a list of users from the database.

    Parameters:
        skip (int): The number of users to skip. Defaults to 0.
        limit (int): The maximum number of users to return. Defaults to 0.
        db (Session): The database session. Defaults to Depends(get_db).
        current_user (Depends(get_current_active_user)): The current active user. Defaults to Depends(get_current_active_user).

    Returns:
        list[schemas.User]: A list of User objects from the database.

    Raises:
        HTTPException: If the current user does not have enough permissions.
    """
    if current_user.id != id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    users = crud.get_users(db,skip=skip,limit=limit)
    return users


@auth.get("/users/me/", response_model=CustomProfile)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Get the profile of the current user.

    Parameters:
        current_user (Annotated[User, Depends(get_current_active_user)]): The current active user.

    Returns:
        Profile: The profile of the current user.
    """
    return current_user


@auth.get("/users/role", response_model=UserRole)
async def read_users_me(
    current_user: Annotated[UserRole, Depends(get_current_active_user_role)],
):
    """
    Get the role of the current user.

    Parameters:
        current_user (Annotated[UserRole, Depends(get_current_active_user_role)]): The current active user's role.

    Returns:
        UserRole: The role of the current user.
    """
    return current_user