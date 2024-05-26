from fastapi import APIRouter
from schemas.users import User, UserUpdate, Creds
from schemas.CV import CV 
from schemas.vacancy import vacancy
from services.users import user_service

router = APIRouter()

@router.get(
    "/users",
    status_code=200,
    response_model=list[User],
)
def get_users():
    return user_service.get_users()

@router.get(
    "/CVes",
    status_code=200,
    response_model=list[CV],
)
def get_CVes(mail: str,
                   password:str):
    creds: Creds = Creds(mail=mail,
                         password=password)
    return user_service.get_CV(creds)

@router.get(
    "/vacancies",
    status_code=200,
    response_model=list[vacancy],
)
def get_vacancies(mail: str,
                   password:str):
    creds: Creds = Creds(mail=mail,
                         password=password)
    return user_service.get_vacancy(creds)

@router.post("/users{mail}",
            status_code=200,
            response_model=User | str,)
def register(mail: str,
             password:str,
             password_check: str):
    if password == password_check:
        creds: Creds = Creds(mail=mail,
                    password=password) 
        user = user_service.register(creds=creds)
        return user
    return "Password mismatch"

@router.put(
    "/users/{id}",
    response_model=User,
)
def update_user(
        id: str,
        creds: UserUpdate
):
    return user_service.update_user(id, creds)

@router.post(
    "/CVes",
    status_code=200,
    response_model=CV | str,
)
def create_CV(mail: str, password: str, title: str, surname: str,
            name: str, patronymic: str, date_of_birth: str,
            gender: str, city: str, salary: str, skills: list[str]):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    CV = user_service.create_CV(creds, title, surname, name, patronymic, date_of_birth, gender, city, salary, skills)
    if CV == None:
        return "This CV is already exist"
    return CV

@router.delete(
    "/users/{CVes}",
    status_code=200,
    response_model=CV,
)
def delete_CV(
        mail: str,
        password:str,
        CV_id: str
):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    return user_service.delete_CV(creds, CV_id)

@router.put(
    "/CVes/{id}",
    status_code=200,
    response_model=CV,
)
def edit_CV(mail: str, password: str, id: str, title: str, surname: str,
            name: str, patronymic: str, date_of_birth: str,
            gender: str, city: str, salary: str, skills: list[str]):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    CV = user_service.edit_CV(creds, id, title, surname,
                                name, patronymic, date_of_birth,
                                gender, city, salary, skills)
    return CV

@router.post(
    "/CVes/{title}",
    status_code=200,
    response_model=list[CV],
)
def search_CV_by_title(title: str):
    return user_service.search_CV_by_title(title)

@router.post(
    "/vacancies",
    status_code=200,
    response_model=vacancy | str,
)
def create_vacancy(mail: str, password: str, title: str, city: str, salary: str, skills: list[str]):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    vacancy = user_service.create_vacancy(creds, title, city, salary, skills)
    if vacancy == None:
        return "This vacancy is already exist"
    return vacancy

@router.delete(
    "/users/{vacancies}",
    status_code=200,
    response_model=vacancy,
)
def delete_vacancy(
        mail: str,
        password:str,
        vacancy_id: str
):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    return user_service.delete_vacancy(creds, vacancy_id)

@router.put(
    "/vacancies/{id}",
    status_code=200,
    response_model=vacancy,
)
def edit_vacancy(mail: str, password: str, id: str, title: str, city: str, salary: str, skills: list[str]):
    creds: Creds = Creds(mail=mail,
                 password=password) 
    vacancy = user_service.edit_vacancy(creds, id, title, city, salary, skills)
    return vacancy

@router.post(
    "/vacancies/{title}",
    status_code=200,
    response_model=list[vacancy],
)
def search_vacancy_by_title(title: str):
    return user_service.search_vacancy_by_title(title)