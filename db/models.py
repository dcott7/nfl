from enum import Enum
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, Float, DateTime
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
    contracts: Mapped[list["Contract"]] = relationship("Contract", back_populates="athlete")
    
    
class Team(BaseModel):
    __tablename__ = "teams"
    name = Column(String)
    cap_room = Column(Float)
    
    athletes: Mapped[list["Athlete"]] = relationship(back_populates="team")
    draftpicks: Mapped[list["DraftPick"]] = relationship(back_populates="team")
    events: Mapped[list["Event"]] = relationship("Event", secondary="competitors", back_populates="teams")
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
    is_winner = Column(Boolean, nullable=True)
    score = Column(Integer, nullable=True)

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team: Mapped["Team"] = relationship(viewonly=True)  # 👈 Make view-only
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
    
    
competition_official_association = Table(
    "competition_officials",
    Base.metadata,
    Column("competition_id", ForeignKey("competitions.id"), primary_key=True),
    Column("official_id", ForeignKey("officials.id"), primary_key=True)
)

class Competition(BaseModel):
    __tablename__ = "competitions"

    date = Column(DateTime)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    event: Mapped["Event"] = relationship(back_populates="competition")  
    venue_id: Mapped[int | None] = mapped_column(ForeignKey("venues.id"), nullable=True)
    venue: Mapped["Venue"] = relationship(back_populates="competitions")
    drives: Mapped[list["Drive"]] = relationship(back_populates="competition", cascade="all, delete-orphan")
    competitors: Mapped[list["Competitor"]] = relationship(back_populates="competition", cascade="all, delete-orphan")
    competition_status_id: Mapped[int | None] = mapped_column(ForeignKey("competition_statuses.id"), nullable=True)
    competition_status: Mapped["CompetitionStatus"] = relationship("CompetitionStatus", back_populates="competitions")

    referees: Mapped[list["Official"]] = relationship(
        "Official",
        secondary=competition_official_association,
        back_populates="competitions"
    )


class CompetitionStatus(BaseModel):
    __tablename__ = "competition_statuses"

    clock = Column(Integer)
    display_clock = Column(String)
    period = Column(Integer)

    competition_status_type_id: Mapped[int] = mapped_column(ForeignKey("competition_status_types.id"))
    competition_status_type: Mapped["CompetitionStatusType"] = relationship(
        "CompetitionStatusType", back_populates="competition_statuses"
    )

    competitions: Mapped[list["Competition"]] = relationship("Competition", back_populates="competition_status")


class CompetitionStatusType(BaseModel):
    __tablename__ = "competition_status_types"

    name = Column(String)
    state = Column(String)
    completed = Column(Boolean)
    description = Column(String)
    detail = Column(String)

    competition_statuses: Mapped[list["CompetitionStatus"]] = relationship(
        "CompetitionStatus", back_populates="competition_status_type"
    )
        
        
class DraftPick(BaseModel):
    __tablename__ = "draftpicks"
    
    year = Column(Integer)
    round = Column(Integer)
    pick_number = Column(Integer)
    
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    team: Mapped["Team"] = relationship(back_populates="draftpicks")
        
        
class Weather(BaseModel):
    __tablename__ = "weathers"
    
    wind_speed = Column(Integer)
    temperature = Column(Integer)
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
    
    teams: Mapped[list["Team"]] = relationship("Team", secondary="competitors", back_populates="events")  # Corrected
  
    
class Stat(BaseModel):
    __tablename__ = "stats"
    
    name = Column(String)
    description = Column(String)
    abbreviation = Column(String)
    value = Column(Float)
    
    playparticipant_id: Mapped[int] = mapped_column(ForeignKey("playparticipants.id"))
    playparticipant: Mapped["PlayParticipant"] = relationship(back_populates="stats")
    
    
class Official(BaseModel):
    __tablename__ = "officials"
    
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer)
    
    officialposition_id: Mapped[int] = mapped_column(ForeignKey("officialpositions.id"))
    officialposition: Mapped["OfficialPosition"] = relationship(back_populates="officials")
    
    competitions: Mapped[list["Competition"]] = relationship(
        "Competition",
        secondary=competition_official_association,
        back_populates="referees"
    )
    
    
class OfficialPosition(BaseModel):
    __tablename__ = "officialpositions"
    
    name = Column(String)
    
    officials: Mapped[list[Official]] = relationship(back_populates="officialposition")
    

class Contract(BaseModel):
    __tablename__ = 'contracts'

    athlete_id = Column(Integer, ForeignKey('athletes.id'), nullable=False)
    team_name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    apy_hit_pct = Column(String)
    dead_cap = Column(String)
    base_salary = Column(String)
    signing_bonus = Column(String)
    per_game_bonus = Column(String)
    roster_bonus = Column(String)
    option_bonus = Column(String)
    workout_bonus = Column(String)
    restructure_bonus = Column(String)
    incentives = Column(String)

    athlete = relationship("Athlete", back_populates="contracts")
    
# class Contract(BaseModel):
#     __tablename__ = 'contracts'

#     athlete_id = Column(Integer, ForeignKey('athletes.id'), nullable=False)
#     year = Column(Integer, nullable=False)
#     cap_hit_annual = Column(String)
#     cap_pct_league_cap = Column(String)
#     cash_annual = Column(String)
#     cash_cummulative = Column(String)
#     dead_cap_annual = Column(String)
#      = Column(String)
#     option_bonus = Column(String)
#     workout_bonus = Column(String)
#     restructure_bonus = Column(String)
#     incentives = Column(String)

#     athlete = relationship("Athlete", back_populates="contracts")