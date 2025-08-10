from datetime import time
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from habits.models import Habit

User = get_user_model()

class PublicHabitsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="pubuser", password="pass")

    def test_list_public_habits(self):
        # публичная запись — должна попасть в /api/public/
        Habit.objects.create(
            user=self.user,
            place="дом",
            time=time(0, 10),
            action="выпить стакан воды",
            is_pleasant=False,
            periodicity=1,
            reward="чай с мёдом",
            execution_time=60,
            is_public=True,
        )
        # приватная — не должна попадать
        Habit.objects.create(
            user=self.user,
            place="офис",
            time=time(0, 11),
            action="растяжка",
            is_pleasant=False,
            periodicity=1,
            reward="кофе",
            execution_time=10,
            is_public=False,
        )

        resp = self.client.get("/api/public/")
        print("DEBUG:", resp.status_code, resp.data)  # чтобы увидеть реальный ответ в логе

        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(resp.data.get("count", 0), 1)
        places = [x["place"] for x in resp.data["results"]]
        self.assertIn("дом", places)
