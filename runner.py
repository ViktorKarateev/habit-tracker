# runner.py
import os
import sys
from dotenv import load_dotenv


def main():
    # чтобы .env подхватился при ручном запуске
    load_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habit_tracker.settings")

    import django
    django.setup()

    from notifications.tasks import send_due_habits
    sent = send_due_habits()
    print(f"sent={sent}")


if __name__ == "__main__":
    sys.exit(main())
