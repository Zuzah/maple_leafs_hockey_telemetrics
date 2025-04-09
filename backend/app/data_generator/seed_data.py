
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..db.models import TrackingData, Base
from ..db.database import engine, SessionLocal

POSITIONS = ["LW", "C", "RW", "LD", "RD", "G"]
TEAM_IDS = [1, 2]

# Define consistent roster for a single game
roster = [
    {"player_id": 1, "position": "G",  "team_id": 1, "handedness": "L"},
    {"player_id": 2, "position": "LD", "team_id": 1, "handedness": "L"},
    {"player_id": 3, "position": "RD", "team_id": 1, "handedness": "R"},
    {"player_id": 4, "position": "LW", "team_id": 1, "handedness": "L"},
    {"player_id": 5, "position": "C",  "team_id": 1, "handedness": "L"},
    {"player_id": 6, "position": "RW", "team_id": 1, "handedness": "R"},
    {"player_id": 7, "position": "G",  "team_id": 2, "handedness": "R"},
    {"player_id": 8, "position": "LD", "team_id": 2, "handedness": "L"},
    {"player_id": 9, "position": "RD", "team_id": 2, "handedness": "R"},
    {"player_id": 10, "position": "LW", "team_id": 2, "handedness": "L"},
    {"player_id": 11, "position": "C",  "team_id": 2, "handedness": "R"},
    {"player_id": 12, "position": "RW", "team_id": 2, "handedness": "R"},
]


def generate_position(pos: str, team: int):
    """Simulate (x, y, z) for a position."""
    zone_bias = -1 if team == 1 else 1  # Team 1 defends left, team 2 right

    if pos == "G":
        return zone_bias * 85 + random.uniform(-5, 5), random.uniform(-5, 5), 0.1
    elif pos in ["LD", "RD"]:
        return zone_bias * 60 + random.uniform(-15, 15), random.uniform(-20, 20), 0.1
    elif pos in ["C"]:
        return zone_bias * random.uniform(-30, 30), random.uniform(-15, 15), 0.1
    elif pos in ["LW"]:
        return zone_bias * random.uniform(-30, 30), random.uniform(20, 42.5), 0.1
    elif pos in ["RW"]:
        return zone_bias * random.uniform(-30, 30), random.uniform(-42.5, -20), 0.1
    return 0.0, 0.0, 0.1


def generate_puck_location():
    """Simulate puck location near the middle with bias toward offensive rush."""
    return random.uniform(-50, 50), random.uniform(-25, 25), 0.05


def seed_tracking_data(session: Session, num_games=3, seconds=60, hz=100):
    print(f"Seeding {num_games} games of synthetic tracking data...")

    Base.metadata.create_all(bind=engine)
    base_time = datetime.utcnow()

    for game_index in range(num_games):
        game_id = 1 + game_index  # Example: 1, 2, 3
        game_time_offset = timedelta(hours=game_index)  # Simulate different start times

        for i in range(seconds * hz):  # 100Hz per second
            game_second = i / hz
            timestamp = base_time + game_time_offset + timedelta(seconds=game_second)

            # Puck row (player_id=None)
            x, y, z = generate_puck_location()
            session.add(TrackingData(
                x=x, y=y, z=z,
                timestamp=timestamp,
                game_second=game_second,
                game_id=game_id,
                period=1,
                player_id=None,
                player_position=None,
                player_handedness=None,
                team_id=None,
                team_current_score=random.randint(0, 5),
                opponent_current_score=random.randint(0, 5),
                number_of_skaters_home=5,
                number_of_skaters_away=5
            ))

            # Player data
            for player in roster:
                x, y, z = generate_position(player["position"], player["team_id"])
                session.add(TrackingData(
                    x=x, y=y, z=z,
                    timestamp=timestamp,
                    game_second=game_second,
                    game_id=game_id,
                    period=1,
                    player_id=player["player_id"],
                    player_position=player["position"],
                    player_handedness=player["handedness"],
                    team_id=player["team_id"],
                    team_current_score=random.randint(0, 5),
                    opponent_current_score=random.randint(0, 5),
                    number_of_skaters_home=5,
                    number_of_skaters_away=5
                ))

    session.commit()
    print("Done seeding synthetic games.")


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)  # Drop all tables
    Base.metadata.create_all(bind=engine)  # Recreate tables
    db = SessionLocal()
    seed_tracking_data(db, seconds=60, hz=100)
    db.close()
