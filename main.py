from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from db.models import Team

engine = create_engine('sqlite:///sports.db')
Session = sessionmaker(bind=engine)
session = Session()

teams = session.query(Team).all()
for team in teams:
    print(team.id, team.name)