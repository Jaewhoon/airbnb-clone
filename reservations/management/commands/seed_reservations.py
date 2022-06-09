import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservation_model
from users import models as user_model
from rooms import models as room_model

NAME = "reservations"


class Command(BaseCommand):
    help = "This command creates reservations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help=f"How many {NAME} do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_guests = user_model.User.objects.all()
        all_rooms = room_model.Room.objects.all()
        seeder.add_entity(
            reservation_model.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(all_guests),
                "room": lambda x: random.choice(all_rooms),
                "check_in": lambda x: datetime.now()
                + timedelta(days=random.randint(-20, 3)),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
