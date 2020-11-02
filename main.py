from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import csv

from src.models import Person, Weekly, engine
from src.scraper import get_data


def add_to_db(session, weekly, year, week):
    """
    Adds the given weekly item to the database, if its runner is already in the
    system.
    """

    # Query the db for the user
    result = session.query(Person.id).filter_by(
        first_name=weekly.first_name,
        last_name=weekly.last_name
    ).first()

    if not result:  # this means the user hasn't been added to the system yet
        print("{} {} not found in database, add them to data/users.csv if you "
              "want them to be stored.".format(
                  weekly.first_name,
                  weekly.last_name
              ))

        return

    last_weekly = session.query(Weekly).filter_by(
        runner_id=result[0],
        week=week,
        year=year
    ).first()

    if not last_weekly:  # This means this week's data hasn't been added before
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

    else:  # The row's already in the table, so just update its data
        last_weekly.distance = weekly.distance
        last_weekly.time = weekly.total_time
        last_weekly.velocity = weekly.velocity
        last_weekly.activity_count = weekly.activity_count
        last_weekly.best_distance = weekly.best_distance
        last_weekly.best_time = weekly.best_moving_time

    session.add(last_weekly)
    session.commit()  # Very important, otherwise the add gets rollbacked


def add_users(session):
    """
    Add new users from data/users.csv to the database
    """

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


# =====CONFIG=====
# Amount of weeks to check (including the current week)
week_count = 5
# The club to scrape
club_id = 623637

# This starts a connection to the database
session = sessionmaker(bind=engine)()

add_users(session)

for i in range(week_count):
    date = datetime.now() - timedelta(weeks=i)
    year = date.year
    week = date.isocalendar()[1]  # This returns the week number

    for entry in get_data(club_id, i):
        # if entry.valid:
        add_to_db(session, entry, year, week)

session.close()
