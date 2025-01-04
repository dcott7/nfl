from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base 


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key = True)
    

class Athlete(BaseModel):
    __tablename__ = "athletes"
    
    # id = Column(String) should be espn id
    name = Column(String)
    age = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    salary = Column(Float)
    is_practice_squad = Column(Boolean)
    
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team: Mapped["Team"] = relationship(back_populates="athletes")
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))
    position: Mapped["Position"] = relationship(back_populates="athletes")
    ratings: Mapped[list["Rating"]] = relationship(back_populates="athletes")
    plays: Mapped[list["PlayParticipant"]] = relationship(back_populates="athlete")
    
    
class Team(BaseModel):
    __tablename__ = "teams"
    
    # id = Column(String) should be espn id
    name = Column(String)
    cap_room = Column(Float)
    
    athletes: Mapped[list["Athlete"]] = relationship(back_populates="team")
    draftpicks: Mapped[list["DraftPick"]] = relationship(back_populates="team")
    events: Mapped[list["Competitor"]] = relationship(back_populates="team")
    
    
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
    team: Mapped["Team"] = relationship(back_populates="competitions")
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped["Event"] = relationship(back_populates="competitors")
        
        
class Venue(BaseModel):
    __tablename__ = "venues"
    
    # id = Column(String) should be espn id
    name = Column(String)
    grass = Column(Boolean)
    indoor = Column(Boolean)
    city = Column(String)
    state = Column(String)
    zip_code = Column(Integer)
    
    competitions: Mapped[list["Competition"]] = relationship()


class PlayParticipant(BaseModel):
    __tablename__ = "playparticipants"

    order = Column(Integer)
    type = Column(String)
    
    play_id: Mapped[int] = mapped_column(ForeignKey("plays.id"))
    play: Mapped["Play"] = relationship(back_populates="participants")
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id"))
    athlete: Mapped["Athlete"] = relationship(back_populates="plays")
    stats: Mapped[list["Stat"]] = relationship()


class Play(BaseModel):
    __tablename__ = "plays"
    
    # id = Column(String) should be espn id
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
    
    drive_id: Mapped[int] = mapped_column(ForeignKey("drives.id"))
    drive: Mapped["Drive"] = relationship(back_populates="plays")
    participants: Mapped[list["PlayParticipant"]] = relationship()

class Drive(BaseModel):
    __tablename__ = "drives"
    
    # id = Column(String) should be espn id
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
    plays: Mapped[list["Play"]] = relationship()
    

class Competition(BaseModel):
    __tablename__ = "competitions"
    
    # id = Column(String) should be espn id
    date = Column(DateTime)
    
    event_id = Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped["Event"] = relationship(back_populates="competition")
    competitors: Mapped[list["Competitor"]] = relationship()
    venue_id = Mapped[int] = mapped_column(ForeignKey("venues.id"))
    venue: Mapped["Venue"] = relationship(back_populates="competitions")
    drives: Mapped[list["Drive"]] = relationship()
        
        
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
    
    events: Mapped[list["Event"]] = relationship()
    
    
class Event(BaseModel):
    __tablename__ = "events"

    season = Column(Integer)
    week = Column(Integer)
    season_type = Column(Integer)
    name = Column(String)

    # Relationships
    competitors: Mapped[list["Competitor"]] = relationship(back_populates="event", cascade="all, delete-orphan")
    competition: Mapped["Competition"] = relationship(back_populates="event")
    weather_id: Mapped[int] = mapped_column(ForeignKey("weathers.id"))
    weather: Mapped["Weather"] = relationship(back_populates="events")
    
    
class Stat(BaseModel):
    __tablename__ = "stats"
    
    name = Column(String)
    description = Column(String)
    abbreviation = Column(String)
    value = Column(Float)
    
    play_id: Mapped[int] = mapped_column(ForeignKey("plays.id"))
    play: Mapped["Play"] = relationship()