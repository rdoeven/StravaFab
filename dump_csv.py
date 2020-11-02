from sqlalchemy.orm import sessionmaker
from src.models import Person, Weekly, engine
import csv


session = sessionmaker(bind=engine)()

halls = {}
persons = {}

for person, weekly in session.query(Person, Weekly).filter(Person.id ==
                                                           Weekly.runner_id
                                                           ).all():
    hall = person.room_number // 100

    halls[hall] = halls.get(hall, 0) + weekly.distance

    if person.id in persons:
        persons[person.id]["total"] += weekly.distance

    else:
        persons[person.id] = {
            "name": "{} {}".format(person.first_name, person.last_name),
            "total": weekly.distance,
            "hall": hall
        }

session.close()

with open("data/dump.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=';')

    for hall, distance in halls.items():
        writer.writerow([hall, distance])

    writer.writerow([])
    writer.writerow([])

    for data in persons.values():
        writer.writerow([data["name"], data["hall"], data["total"]])
