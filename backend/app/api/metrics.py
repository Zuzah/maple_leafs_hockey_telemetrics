from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import TrackingData

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/zone-time")
def zone_time_per_defenseman(db: Session = Depends(get_db)):
    # Get all LD and RD players
    results = db.query(TrackingData).filter(
        TrackingData.player_position.in_(["LD", "RD"]),
        TrackingData.player_id.isnot(None)
    ).all()

    if not results:
        return {"detail": "No data found."}

    # Group by player_id
    player_map = {}
    for row in results:
        player_id = row.player_id
        if player_id not in player_map:
            player_map[player_id] = {
                "player_id": player_id,
                "team_id": row.team_id,
                "player_position": row.player_position,
                "total_dz_frames": 0,
                "total_frames": 0
            }

        # Defensive zone heuristic (assume Team 1 defends left side, Team 2 right)
        is_in_dz = (
            (row.team_id == 1 and row.x <= -75) or
            (row.team_id == 2 and row.x >= 75)
        )

        if is_in_dz:
            player_map[player_id]["total_dz_frames"] += 1

        player_map[player_id]["total_frames"] += 1

    # Calculate averages
    output = []
    for player in player_map.values():
        total_shifts = max(player["total_frames"] / (30 * 100), 1)  # 30s per shift, 100Hz
        avg_dz_time_per_shift = player["total_dz_frames"] / 100 / total_shifts  # convert to seconds
        output.append({
            "player_id": player["player_id"],
            "position": player["player_position"],
            "team_id": player["team_id"],
            "avg_dz_time_per_shift_secs": round(avg_dz_time_per_shift, 2)
        })

    return output

# TODO
@router.get("/dzs-percentage")
def dzs_percentage_stub():
    """
    Defensive Zone Start % = (DZ starts) / (OZ + NZ + DZ + On-the-Fly starts)
    Requires faceoff location data or shift start context from NHL API.
    """
    return {
        "metric": "Defensive Zone Start %",
        "status": "NOT IMPLEMENTED",
        "todo": [
            "Access faceoff event data with zone location",
            "Join with shift start times per player",
            "Categorize faceoff starts into DZ, OZ, NZ, or OTF",
            "Compute DZS% = DZ / (OZ + NZ + DZ + OTF)",
            "Add SQL joins or event ingestion from NHL API"
        ],
        "example_format": {
            "player_id": 2,
            "position": "LD",
            "team_id": 1,
            "dzs_percentage": "TODO: blocked until data source available"
        }
    }

@router.get("/slot-coverage")
def slot_coverage_effectiveness(db: Session = Depends(get_db)):
    # Get puck frames
    puck_frames = db.query(TrackingData).filter(
        TrackingData.player_id.is_(None)
    ).all()

    # Build a map of puck location by timestamp
    puck_map = {}
    for puck in puck_frames:
        puck_map[puck.timestamp] = {
            "x": puck.x,
            "y": puck.y,
            "team_dz": 1 if puck.x <= -75 else 2 if puck.x >= 75 else None
        }

    # Get all defensemen
    dmen = db.query(TrackingData).filter(
        TrackingData.player_position.in_(["LD", "RD"]),
        TrackingData.player_id.isnot(None)
    ).all()

    slot_stats = {}

    for row in dmen:
        # Match with puck frame
        puck = puck_map.get(row.timestamp)
        if not puck or puck["team_dz"] != row.team_id:
            continue  # only count when puck is in player's DZ

        pid = row.player_id
        if pid not in slot_stats:
            slot_stats[pid] = {
                "player_id": pid,
                "team_id": row.team_id,
                "slot_frames": 0,
                "dz_frames_with_puck": 0
            }

        slot_stats[pid]["dz_frames_with_puck"] += 1

        # Check if player is in the slot area
        if -20 <= row.x <= 20 and -10 <= row.y <= 10:
            slot_stats[pid]["slot_frames"] += 1

    # Calculate %
    output = []
    for s in slot_stats.values():
        if s["dz_frames_with_puck"] == 0:
            pct = 0.0
        else:
            pct = (s["slot_frames"] / s["dz_frames_with_puck"]) * 100
        output.append({
            "player_id": s["player_id"],
            "team_id": s["team_id"],
            "slot_coverage_pct": round(pct, 2)
        })

    return output

