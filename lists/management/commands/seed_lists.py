import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_model
from users import models as user_model
from rooms import models as room_model

NAME = "lists"


class Command(BaseCommand):
    help = f"This command creates {NAME}"

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
        all_users = user_model.User.objects.all()
        seeder.add_entity(
            list_model.List,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "user": lambda x: random.choice(all_users),
            },
        )
        created = seeder.execute()
        cleaned = flatten(created.values())
        rooms = room_model.Room.objects.all()
        for pk in cleaned:
            add_list = list_model.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            add_list.rooms.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
