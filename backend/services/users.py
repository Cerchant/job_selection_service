from schemas.users import User, UserUpdate, Creds
from schemas.CV import CV
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
                    CVes=user["CVes"]
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

    def update_user(self, id: uuid.UUID, creds: UserUpdate) -> User:
        if auth_user := self._auth(creds.auth):
            if auth_user.id != id:
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
                        CVes=user["CVes"]
                    )

        raise ValueError()


    def _auth(self, creds: Creds) -> User | None:
        with open('data/user_data.json') as user_file:
            self.user_data=json.load(user_file)
        for user in self.user_data["users"]:
            print(user, "AAAAAA")
            if user["mail"] == creds.mail and user["password"] == creds.password:
                return User(
                    id=user["id"],
                    mail=user["mail"],
                    password=user["password"],
                    CVes=user["CVes"]
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
            "CVes": []
        }
        self.data["users"].append(user)
        with open('data/user_data.json', "w") as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)
        return User(
            id=user["id"],
            mail=user["mail"],
            password=user["password"],
            CVes=user["CVes"]
        )
    
    def _CV_exist(self, creds: Creds, CV_title: str) -> CV | None:
        with open('data/user_data.json') as user_file:
            self.data=json.load(user_file)
        with open('data/CV_data.json') as CV_file:
            self.CV_data=json.load(CV_file)
        
        for user in self.user_data["users"]:
            if (user["mail"] == creds.mail) and (user["password"] == creds.password):
                for CV in self.CV_data["CVes"]:
                    if (CV["title"] == CV_title) and (CV["id"] in user["CVes"]):
                        return CV

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

        
        check_CV = self._CV_exist(creds, CV_title)
        if check_CV == None:
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
      
user_service: UserService = UserService()