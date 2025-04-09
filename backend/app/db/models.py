from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TrackingData(Base):
    __tablename__ = "tracking_data"

    id = Column(Integer, primary_key=True, index=True)

    '''
    Based on details provided by Darryl Metcalf
    '''
    
    # Spatial-temporal data
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    game_second = Column(Float, nullable=False)

    # Game context
    game_id = Column(Integer, nullable=False)
    period = Column(Integer, nullable=False)

    # Player metadata
    player_id = Column(Integer, nullable=True)  # Null for puck
    player_position = Column(String, nullable=True)
    player_handedness = Column(String, nullable=True)

    # Team/game state
    team_id = Column(Integer, nullable=True)
    team_current_score = Column(Integer, nullable=True)
    opponent_current_score = Column(Integer, nullable=True)
    number_of_skaters_home = Column(Integer, nullable=True)
    number_of_skaters_away = Column(Integer, nullable=True)
