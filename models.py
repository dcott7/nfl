from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base 


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key = True)
    

class Athlete(BaseModel):
    __tablename__ = "athletes"
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    salary = Column(Float)
    is_practice_squad = Column(Boolean)
    
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=True)
    team: Mapped["Team"] = relationship(back_populates="athletes")
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))
    position: Mapped["Position"] = relationship(back_populates="athletes")
    ratings: Mapped[list["Rating"]] = relationship(back_populates="athletes")
    playparticipants: Mapped[list["PlayParticipant"]] = relationship(back_populates="athlete")
    teamhistory: Mapped[list["TeamHistory"]] = relationship(back_populates="athlete")
    
    
class Team(BaseModel):
    __tablename__ = "teams"
    name = Column(String)
    cap_room = Column(Float)
    
    athletes: Mapped[list["Athlete"]] = relationship(back_populates="team")
    draftpicks: Mapped[list["DraftPick"]] = relationship(back_populates="team")
    events: Mapped[list["Competitor"]] = relationship(back_populates="team", overlaps="competitors")
    competitors: Mapped[list["Competitor"]] = relationship(back_populates="team", overlaps="events")
    teamhistory: Mapped[list["TeamHistory"]] = relationship(back_populates="team")
    
    
class TeamHistory(BaseModel):
    __tablename__ = "teamhistory"
    
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    season = Column(Integer)

    athlete: Mapped["Athlete"] = relationship("Athlete", back_populates="teamhistory")
    team: Mapped["Team"] = relationship("Team", back_populates="teamhistory")

    
class Position(BaseModel):
    __tablename__ = "positions"
    
    position_name = Column(String)
    
    athletes: Mapped[list["Athlete"]] = relationship(back_populates="position")


class Rating(BaseModel):
    __tablename__ = "ratings"
    
    rating_type = Column(String)
    rating = Column(Integer)
    
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id"))
    athletes: Mapped["Athlete"] = relationship(back_populates="ratings")
        

class Competitor(BaseModel):
    __tablename__ = "competitors"

    is_home = Column(Boolean)
    is_winner = Column(Boolean, nullable=True)  # nullable in case the event isn't concluded
    score = Column(Integer, nullable=True)

    # Foreign key relationships
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team: Mapped["Team"] = relationship(back_populates="competitors")
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped["Event"] = relationship(back_populates="competitors")
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    competition: Mapped["Competition"] = relationship(back_populates="competitors")
        
        
class Venue(BaseModel):
    __tablename__ = "venues"
    
    name = Column(String)
    grass = Column(Boolean)
    indoor = Column(Boolean)
    city = Column(String)
    state = Column(String)
    zip_code = Column(Integer)
    
    competitions: Mapped[list["Competition"]] = relationship(back_populates="venue")


class PlayParticipant(BaseModel):
    __tablename__ = "playparticipants"

    order = Column(Integer)
    type = Column(String)
    
    play_id: Mapped[int] = mapped_column(ForeignKey("plays.id"))
    play: Mapped["Play"] = relationship(back_populates="participants")
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id"))
    athlete: Mapped["Athlete"] = relationship(back_populates="playparticipants")
    stats: Mapped[list["Stat"]] = relationship(back_populates="playparticipant")


class Play(BaseModel):
    __tablename__ = "plays"
    
    sequence_number = Column(Integer)
    play_type = Column(String)
    description = Column(String)
    away_score = Column(Integer)
    home_score = Column(Integer)
    quarter = Column(Integer)
    is_scoring_play = Column(Boolean)
    score_value = Column(Integer)
    start_down = Column(Integer)
    end_down = Column(Integer)
    start_distance = Column(Integer)
    end_distance = Column(Integer)
    start_yardline = Column(Integer)
    end_yardline = Column(Integer)
    start_yards_to_endzone = Column(Integer)
    end_yards_to_endzone = Column(Integer)
    
    drive_id: Mapped[int] = mapped_column(ForeignKey("drives.id"), nullable=True)
    drive: Mapped["Drive"] = relationship(back_populates="plays")
    participants: Mapped[list["PlayParticipant"]] = relationship(back_populates="play")

class Drive(BaseModel):
    __tablename__ = "drives"
    
    description = Column(String)
    yards = Column(Integer)
    is_score = Column(Boolean)
    num_offensive_plays = Column(Integer)
    start_quarter = Column(Integer)
    start_time = Column(Integer)
    start_yardline = Column(Integer)
    end_quarter = Column(Integer)
    end_time = Column(Integer)
    end_yardline = Column(Integer)
    
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.id"))
    competition: Mapped["Competition"] = relationship(back_populates="drives")
    plays: Mapped[list["Play"]] = relationship(back_populates="drive")
    

class Competition(BaseModel):
    __tablename__ = "competitions"
    date = Column(DateTime)
    
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped["Event"] = relationship(back_populates="competition")
    competitors: Mapped[list["Competitor"]] = relationship(back_populates="competition")
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"))
    venue: Mapped["Venue"] = relationship(back_populates="competitions")
    drives: Mapped[list["Drive"]] = relationship(back_populates="competition")
        
        
class DraftPick(BaseModel):
    __tablename__ = "draftpicks"
    
    year = Column(Integer)
    round = Column(Integer)
    pick_number = Column(Integer)
    
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team: Mapped["Team"] = relationship(back_populates="draftpicks")
        
        
class Weather(BaseModel):
    __tablename__ = "weathers"
    
    display = Column(String)
    wind_speed = Column(Integer)
    temperature = Column(Integer)
    gust = Column(Integer)
    precipitation = Column(Integer)
    
    events: Mapped[list["Event"]] = relationship(back_populates="weather")
    
    
class Event(BaseModel):
    __tablename__ = "events"

    season = Column(Integer)
    week = Column(Integer)
    season_type = Column(Integer)
    name = Column(String)

    weather_id: Mapped[int | None] = mapped_column(ForeignKey("weathers.id"), nullable=True)
    weather: Mapped["Weather"] = relationship(back_populates="events")
    competitors: Mapped[list["Competitor"]] = relationship(back_populates="event", cascade="all, delete-orphan")
    competition: Mapped["Competition"] = relationship(back_populates="event")
    
    
class Stat(BaseModel):
    __tablename__ = "stats"
    
    name = Column(String)
    description = Column(String)
    abbreviation = Column(String)
    value = Column(Float)
    
    playparticipant_id: Mapped[int] = mapped_column(ForeignKey("playparticipants.id"))
    playparticipant: Mapped["PlayParticipant"] = relationship(back_populates="stats")