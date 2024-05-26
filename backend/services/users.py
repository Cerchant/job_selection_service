from schemas.users import User, UserUpdate, Creds
from schemas.CV import CV
from schemas.vacancy import vacancy
import uuid
import json
import re


class UserService:
    def __init__(self) -> None:
        ...
    

    def _valid_mail(self, mail: str) -> bool:
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"

        if re.match(pattern, mail) is not None:
            return True
        else:
            return False


    def get_users(self) -> list[User]:
        with open('data/user_data.json') as user_file:
            self.user_data = json.load(user_file)
        users = []

        for user in self.user_data["users"]:
            users.append(
                User(
                    id=user["id"],
                    mail=user["mail"],
                    password=user["password"],
                    CVes=user["CVes"],
                    vacancies=user["vacancies"]
                )
            )

        return users


    def get_CV(self, creds: Creds) -> list[CV]:
        with open('data/user_data.json') as user_file:
            self.user_data = json.load(user_file)
        with open('data/CV_data.json') as CV_file:
            self.CV_data = json.load(CV_file)
        CVes = []

        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail) and (user["password"] == creds.password):
                for CV in self.CV_data["CVes"]:
                    if (CV["id"] in user["CVes"]):
                        CVes.append(CV)
        return CVes


    def get_vacancy(self, creds: Creds) -> list[vacancy]:
        with open('data/user_data.json') as user_file:
            self.user_data = json.load(user_file)
        with open('data/vacancy_data.json') as vacancy_file:
            self.vacancy_data = json.load(vacancy_file)
        vacancies = []

        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail) and (user["password"] == creds.password):
                for vacancy in self.vacancy_data["vacancies"]:
                    if (vacancy["id"] in user["vacancies"]):
                        vacancies.append(vacancy)
        return vacancies


    def update_user(self, id: str, creds: UserUpdate) -> User:
        if auth_user := self._auth(creds.auth):
            if str(auth_user.id) != str(id):
                raise ValueError()
            
            with open('data/user_data.json') as file:
                self.data = json.load(file)

            for user in self.data["users"]:
                if user["id"] == str(id):
                    user["mail"] = creds.mail
                    with open('data/user_data.json', "w") as file:
                        json.dump(self.data, file, indent=2, ensure_ascii=False)
                    return User(
                        id=user["id"],
                        mail=user["mail"],
                        password=user["password"],
                        CVes=user["CVes"],
                        vacancies=user["vacancies"]
                    )

        raise ValueError()


    def _auth(self, creds: Creds) -> User | None:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        for user in self.user_data["users"]:
            if user["mail"] == creds.mail and user["password"] == creds.password:
                return User(
                    id=user["id"],
                    mail=user["mail"],
                    password=user["password"],
                    CVes=user["CVes"],
                    vacancies=user["vacancies"]
                )
        return None
    

    def register(self, creds: Creds) -> User | str:
        if self._valid_mail(creds.mail) == False:
            return "Uncorrect email form"
        if self._auth(creds):
            return None
        with open('data/user_data.json') as file:
            self.data=json.load(file)
        user = {
            "id": str(uuid.uuid4()),
            "mail": creds.mail,
            "password": creds.password,
            "CVes": [],
            "vacancies": []
        }
        self.data["users"].append(user)
        with open('data/user_data.json', "w") as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)
        return User(
            id=user["id"],
            mail=user["mail"],
            password=user["password"],
            CVes=user["CVes"],
            vacancies=user["vacancies"]
        )
    

    def _CV_exist(self, creds: Creds, CV_id: str) -> CV | None:
        with open('data/user_data.json') as user_file:
            self.data=json.load(user_file)
        with open('data/CV_data.json') as CV_file:
            self.CV_data=json.load(CV_file)
        
        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail) and (user["password"] == creds.password):
                for CV in self.CV_data["CVes"]:
                    if (CV["id"] == CV_id) and (CV["id"] in user["CVes"]):
                        return CV

        return None
    

    def _vacancy_exist(self, creds: Creds, vacancy_id: str) -> CV | None:
        with open('data/user_data.json') as user_file:
            self.data=json.load(user_file)
        with open('data/vacancy_data.json') as vacancy_file:
            self.vacancy_data=json.load(vacancy_file)
        
        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail) and (user["password"] == creds.password):
                for vacancy in self.CV_data["CVes"]:
                    if (vacancy["id"] == vacancy_id) and (vacancy["id"] in user["CVes"]):
                        return vacancy

        return None
    

    def login(self, creds: Creds) -> User:
        auth_user = self._auth(creds)
        if auth_user == None:
            return "User is not found"
        return auth_user
    

    def create_CV(self, creds: Creds, CV_title: str, surname: str,
                  name: str, patronymic: str, date_of_birth: str,
                  gender: str, city: str, salary: str, skills: list[str]) -> CV | None:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/CV_data.json') as CV_file:
            self.CV_data=json.load(CV_file)

        
        CV = {
            "id": str(uuid.uuid4()),
            "title": CV_title,
            "surname": surname,
            "name": name,
            "patronymic": patronymic,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "city": city,
            "salary": salary,
            "skills": skills
        }
        for user in self.user_data["users"]:
            if user["mail"] == creds.mail and user["password"] == creds.password:
                user["CVes"].append(str(CV["id"]))
                self.CV_data["CVes"].append(CV)

                with open('data/user_data.json', "w") as user_file:
                    json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                with open('data/CV_data.json', "w") as CV_file:
                    json.dump(self.CV_data, CV_file, indent=2, ensure_ascii=False)
                return CV
                
        return None
    

    def edit_CV(self, creds: Creds, CV_id: str, CV_title: str, surname: str,
                  name: str, patronymic: str, date_of_birth: str,
                  gender: str, city: str, salary: str, skills: list[str]) -> CV | None:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/CV_data.json') as CV_file:
            self.CV_data=json.load(CV_file)

        
        check_CV = self._CV_exist(creds, CV_id)
        if check_CV:
            for user in self.user_data["users"]:
                if user["mail"] == creds.mail and user["password"] == creds.password:
                    for CV in self.CV_data["CVes"]:

                        if (CV["title"] == CV_title) and (CV["id"] in user["CVes"]):

                            CV["title"] = CV_title
                            CV["surname"] = surname
                            CV["name"] = name
                            CV["patronymic"] = patronymic
                            CV["date_of_birth"] = date_of_birth
                            CV["gender"] = gender
                            CV["city"] = city
                            CV["salary"] = salary
                            CV["skills"] = skills

                            with open('data/user_data.json', "w") as user_file:
                                json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                            with open('data/CV_data.json', "w") as CV_file:
                                json.dump(self.CV_data, CV_file, indent=2, ensure_ascii=False)

                            return CV
                
        return None
    
           
    def delete_CV(self, creds: Creds, CV_title: str) -> CV:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/CV_data.json') as CV_file:
            self.CV_data=json.load(CV_file)

        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail and user["password"] == creds.password):
                for CV in self.CV_data["CVes"]:
                    if (CV["title"] == CV_title) and (CV["id"] in user["CVes"]):
                        user["CVes"].remove(CV["id"])
                        self.CV_data["CVes"].remove(CV)
                        with open('data/user_data.json', "w") as user_file:
                            json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                        with open('data/CV_data.json', "w") as CV_file:
                            json.dump(self.CV_data, CV_file, indent=2, ensure_ascii=False)

                        return CV
    

    def search_CV_by_title(self, title: str) -> list[CV]:
        with open('data/CV_data.json') as CV_file:
            self.CV_data=json.load(CV_file)
        
        CVes = []
        for CV in self.CV_data["CVes"]:
            if (CV["title"] == title):
                CVes.append(CV)
        return CVes
    

    def create_vacancy(self, creds: Creds, vacancy_title: str, 
                       city: str, salary: str, skills: list[str]) -> vacancy | None:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/vacancy_data.json') as vacancy_file:
            self.vacancy_data=json.load(vacancy_file)

        
        vacancy = {
            "id": str(uuid.uuid4()),
            "title": vacancy_title,
            "city": city,
            "salary": salary,
            "skills": skills
        }
        for user in self.user_data["users"]:
            if user["mail"] == creds.mail and user["password"] == creds.password:
                user["vacancies"].append(str(vacancy["id"]))
                self.vacancy_data["vacancies"].append(vacancy)

                with open('data/user_data.json', "w") as user_file:
                    json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                with open('data/vacancy_data.json', "w") as vacancy_file:
                    json.dump(self.vacancy_data, vacancy_file, indent=2, ensure_ascii=False)
                return vacancy
                
        return None
    

    def edit_vacancy(self, creds: Creds, vacancy_id: str, vacancy_title: str, 
                    city: str, salary: str, skills: list[str]) -> vacancy | None:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/vacancy_data.json') as vacancy_file:
            self.vacancy_data=json.load(vacancy_file)

        
        check_vacancy = self._vacancy_exist(creds, vacancy_id)
        if check_vacancy:
            for user in self.user_data["users"]:
                if user["mail"] == creds.mail and user["password"] == creds.password:
                    for vacancy in self.vacancy_data["vacancies"]:

                        if (vacancy["title"] == vacancy_title) and (vacancy["id"] in user["vacancies"]):

                            vacancy["title"] = vacancy_title
                            vacancy["city"] = city
                            vacancy["salary"] = salary
                            vacancy["skills"] = skills

                            with open('data/user_data.json', "w") as user_file:
                                json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                            with open('data/vacancy_data.json', "w") as vacancy_file:
                                json.dump(self.vacancy_data, vacancy_file, indent=2, ensure_ascii=False)

                            return vacancy
                
        return None
    
           
    def delete_vacancy(self, creds: Creds, vacancy_title: str) -> vacancy:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        with open('data/vacancy_data.json') as vacancy_file:
            self.vacancy_data=json.load(vacancy_file)

        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail and user["password"] == creds.password):
                for vacancy in self.vacancy_data["vacancies"]:
                    if (vacancy["title"] == vacancy_title) and (vacancy["id"] in user["vacancies"]):
                        user["vacancies"].remove(vacancy["id"])
                        self.vacancy_data["vacancies"].remove(vacancy)
                        with open('data/user_data.json', "w") as user_file:
                            json.dump(self.user_data, user_file, indent=2, ensure_ascii=False)
                        with open('data/vacancy_data.json', "w") as vacancy_file:
                            json.dump(self.vacancy_data, vacancy_file, indent=2, ensure_ascii=False)

                        return vacancy
    

    def search_vacancy_by_title(self, title: str) -> list[vacancy]:
        with open('data/vacancy_data.json') as vacancy_file:
            self.vacancy_data=json.load(vacancy_file)
        
        vacancies = []
        for vacancy in self.vacancy_data["vacancies"]:
            if (vacancy["title"] == title):
                vacancies.append(vacancy)
        return vacancies


user_service: UserService = UserService()