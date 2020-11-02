from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from src.models import Person, Weekly, engine
from src.scraper import get_data
import csv


def add_to_db(engine, weekly, year, week):
    session = sessionmaker(bind=engine)()

    result = session.query(Person.id).filter_by(
        first_name=weekly.first_name,
        last_name=weekly.last_name
    ).first()

    if not result:  # this means the user hasn't been added to the system yet
        print("{} {} not found in database. Please contact your local ISP for"
              "more information.".format(
                  weekly.first_name,
                  weekly.last_name
              ), weekly.first_name, weekly.last_name)

        return

    last_weekly = session.query(Weekly).filter_by(
        runner_id=result[0],
        week=week,
        year=year
    ).first()

    if not last_weekly:
        last_weekly = Weekly(
            runner_id=weekly.athlete_id,
            year=year,
            week=week,
            distance=weekly.distance,
            time=weekly.total_time,
            velocity=weekly.velocity,
            activity_count=weekly.activity_count,
            best_distance=weekly.best_distance,
            best_time=weekly.best_moving_time
        )

    else:
        last_weekly.distance = weekly.distance
        last_weekly.time = weekly.total_time
        last_weekly.velocity = weekly.velocity
        last_weekly.activity_count = weekly.activity_count
        last_weekly.best_distance = weekly.best_distance
        last_weekly.best_time = weekly.best_moving_time

    session.add(last_weekly)
    session.commit()
    session.close()


def add_users(engine):
    session = sessionmaker(bind=engine)()

    with open("data/users.csv", "r") as csv_file:
        reader = csv.reader(csv_file)

        for first_name, last_name, room, athlete_id in reader:
            user = session.query(Person.id).filter_by(id=athlete_id).first()

            if not user:
                user = Person(
                    id=athlete_id,
                    first_name=first_name,
                    last_name=last_name,
                    room_number=room
                )

                session.add(user)
                session.commit()

    session.close()


week_count = 5
club_id = 623637


add_users(engine)
for i in range(week_count):
    date = datetime.now() - timedelta(weeks=i)
    year = date.year
    week = date.isocalendar()[1]

    for entry in get_data(club_id, i):
        # if entry.valid:
        add_to_db(engine, entry, year, week)
