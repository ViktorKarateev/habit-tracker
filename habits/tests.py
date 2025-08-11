from datetime import time
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase
from habits.models import Habit

User = get_user_model()
API = "/api/habits/"

# ===== Публичный список (/api/public/) =====
class TestPublicHabitsAPI(TestCase):
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
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(resp.data.get("count", 0), 1)
        places = [x["place"] for x in resp.data["results"]]
        self.assertIn("дом", places)


# ===== Валидации создания привычек (/api/habits/) =====
API = "/api/habits/"

class TestHabitValidations(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="u1", password="p1")
        # Ключ: аутентифицируем клиента без JWT/сессии
        self.client.force_authenticate(user=self.user)

    def _base(self):
        return {
            "place": "дом",
            "time": timezone.localtime().strftime("%H:%M"),
            "action": "делать что-то",
            "periodicity": 1,
            "execution_time": 60,
            "is_public": False,
            "is_pleasant": False,
            "reward": "",
            "linked_habit": None,
        }

    def test_execution_time_limit(self):
        data = self._base()
        data["execution_time"] = 121
        r = self.client.post(API, data, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("execution_time", r.data)

    def test_periodicity_range(self):
        data = self._base()
        data["periodicity"] = 0
        r = self.client.post(API, data, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("periodicity", r.data)

        data = self._base()
        data["periodicity"] = 8
        r = self.client.post(API, data, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("periodicity", r.data)

    def test_pleasant_cannot_have_reward_or_link(self):
        data = self._base()
        data["is_pleasant"] = True
        data["reward"] = "шоколадка"
        r = self.client.post(API, data, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("reward", r.data)

        # Приятная + linked_habit -> тоже 400
        pleasant_other = self.client.post(
            API, {**self._base(), "is_pleasant": True, "action": "приятная"}, format="json"
        )
        self.assertEqual(pleasant_other.status_code, 201)
        data = self._base()
        data["is_pleasant"] = True
        data["linked_habit"] = pleasant_other.data["id"]
        r = self.client.post(API, data, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("linked_habit", r.data)

    def test_nonpleasant_requires_reward_or_link(self):
        # ни награды, ни связанной — 400
        data = self._base()
        r = self.client.post(API, data, format="json")
        self.assertEqual(r.status_code, 400)

        # только награда — 201
        data = self._base()
        data["reward"] = "чай"
        r = self.client.post(API, data, format="json")
        self.assertEqual(r.status_code, 201)

        # только связанная приятная — 201
        pleasant = self.client.post(
            API, {**self._base(), "is_pleasant": True, "action": "приятная"}, format="json"
        )
        self.assertEqual(pleasant.status_code, 201)
        data = self._base()
        data["linked_habit"] = pleasant.data["id"]
        r = self.client.post(API, data, format="json")
        self.assertEqual(r.status_code, 201)

    def test_cannot_have_both_reward_and_link(self):
        pleasant = self.client.post(
            API, {**self._base(), "is_pleasant": True, "action": "приятная"}, format="json"
        )
        self.assertEqual(pleasant.status_code, 201)

        data = self._base()
        data["reward"] = "кофе"
        data["linked_habit"] = pleasant.data["id"]
        r = self.client.post(API, data, format="json")
        self.assertEqual(r.status_code, 400)

    def test_linked_must_be_pleasant(self):
        # создаём НЕприятную (но валидную: с наградой)
        not_pleasant = self.client.post(
            API, {**self._base(), "is_pleasant": False, "reward": "плюшка"}, format="json"
        )
        self.assertEqual(not_pleasant.status_code, 201)

        data = self._base()
        data["linked_habit"] = not_pleasant.data["id"]
        r = self.client.post(API, data, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("linked_habit", r.data)


class TestPermissionsCRUD(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username="alice", password="pass1")
        self.u2 = User.objects.create_user(username="bob", password="pass2")

        now = timezone.localtime().time().replace(second=0, microsecond=0)
        self.h1 = Habit.objects.create(
            user=self.u1, place="дом", time=now, action="вода u1",
            is_pleasant=False, periodicity=1, execution_time=5,
            is_public=False, reward="чай",
        )
        self.h2 = Habit.objects.create(
            user=self.u2, place="офис", time=now, action="вода u2",
            is_pleasant=False, periodicity=1, execution_time=5,
            is_public=False, reward="кофе",
        )

    def test_anonymous_cannot_access(self):
        self.client.force_authenticate(user=None)  # явно без авторизации
        r = self.client.get(API)
        self.assertEqual(r.status_code, 401)

    def test_user_sees_only_own_habits(self):
        self.client.force_authenticate(user=self.u1)
        r = self.client.get(API)
        self.assertEqual(r.status_code, 200)
        ids = [x["id"] for x in r.data["results"]]
        self.assertIn(self.h1.id, ids)
        self.assertNotIn(self.h2.id, ids)

    def test_cannot_retrieve_foreign(self):
        self.client.force_authenticate(user=self.u1)
        r = self.client.get(f"{API}{self.h2.id}/")
        self.assertEqual(r.status_code, 404)

    def test_owner_can_update(self):
        self.client.force_authenticate(user=self.u1)
        r = self.client.patch(f"{API}{self.h1.id}/", {"place": "квартира"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["place"], "квартира")

    def test_cannot_update_foreign(self):
        self.client.force_authenticate(user=self.u1)
        r = self.client.patch(f"{API}{self.h2.id}/", {"place": "в другом месте"}, format="json")
        self.assertEqual(r.status_code, 404)

    def test_owner_can_delete(self):
        self.client.force_authenticate(user=self.u1)
        r = self.client.delete(f"{API}{self.h1.id}/")
        self.assertEqual(r.status_code, 204)

    def test_cannot_delete_foreign(self):
        self.client.force_authenticate(user=self.u1)
        r = self.client.delete(f"{API}{self.h2.id}/")
        self.assertEqual(r.status_code, 404)

    def test_create_forces_current_user(self):
        self.client.force_authenticate(user=self.u1)
        payload = {
            "place": "дом",
            "time": timezone.localtime().strftime("%H:%M"),
            "action": "новая",
            "periodicity": 1,
            "execution_time": 10,
            "is_public": False,
            "is_pleasant": False,
            "reward": "печенька",
            "linked_habit": None,
            "user": self.u2.id,  # попробуем подсунуть bob
        }
        r = self.client.post(API, payload, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["user"], self.u1.id)
