import unittest
import uuid
from services.users import UserService
from schemas.users import User, Creds
import random

#Test cases to test Calulator methods
#You always create  a child class derived from unittest.TestCase
class TestUserService(unittest.TestCase):
    #setUp method is overridden from the parent class TestCase
    def setUp(self):
        self.user_service: UserService = UserService()
    #Each test method starts with the keyword test_
    def test_register(self):
        creds: Creds = Creds(mail="test" + str(random.randint(999, 9999)) + "@mail.ru", password="123")

        user: User = User(
            id=str(uuid.uuid4()),
            mail=creds.mail,
            password=creds.password,
            CVes=[],
            vacancies=[]
        )

        self.assertEqual(self.user_service.register(creds).mail, user.mail)

    def test_create_CV(self):
        creds: Creds = Creds(mail="test@mail.ru", password="123")
        title = "Petrov"
        surname = "Programmer"
        name = "Ivan"
        patronymic = "Ivanovich"
        date_of_birth = "12.02.2004"
        gender = "М"
        city = "Томск"
        salary = "70000"
        skills = ["SQL"]
        
        CV = self.user_service.create_CV(creds, title, surname,
                                name, patronymic, date_of_birth,
                                gender, city, salary, skills)
        # print(CV)
        self.assertEqual(CV["title"], title)

    def test_search_CV_by_title(self):
        CVes = [
            {
                "id": "f1151ee0-9c8a-437a-b27b-98b5fdb69c37",
                "title": "Programmer",
                "surname": "Petrov",
                "name": "Ivan",
                "patronymic": "Ivanovich",
                "date_of_birth": "12.02.2004",
                "gender": "M",
                "city": "Tomsk",
                "salary": "70000",
                "skills": [
                "SQL"
                ]
            }
        ]
        self.assertEqual(self.user_service.search_CV_by_title("Programmer")[0]["title"], CVes[0]["title"])

# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()