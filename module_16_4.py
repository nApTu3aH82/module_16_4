from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List, Annotated

main_app = FastAPI()

users_db = []


class Users(BaseModel):
    id: int = None
    username: str
    age: int


@main_app.get('/users')
def get_users() -> List[Users]:
    return users_db


@main_app.post('/user/{username}/{age}')
def add_user(user: Users,
             username: Annotated[str, Path(min_length=5, max_length=20, description='Enter Username', example='Rinat')],
             age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='42')]) -> Users:
    if len(users_db) == 0:
        user.id = 1
    else:
        user.id = users_db[-1].id + 1
    user.username = username
    user.age = age
    users_db.append(user)
    return user


@main_app.put('/user/{user_id}/{username}/{age}')
def update_user(user_id: Annotated[int, Path(ge=1, description='Enter User ID')],
                username: Annotated[
                    str, Path(min_length=5, max_length=20, description='Enter Username', example='Rinat')],
                age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='42')]) -> Users:
    try:
        users_db[user_id - 1].username = username
        users_db[user_id - 1].age = age
        return users_db[user_id - 1]
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@main_app.delete('/user/{user_id}')
def delete_user(user_id: Annotated[int, Path(ge=1, description='Enter User ID')]) -> Users:
    for user in users_db:
        if user.id == user_id:
            users_db.remove(user)
            return user
    raise HTTPException(status_code=404, detail='User was not found')
