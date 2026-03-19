from fastapi import APIRouter 
import fastf1 

router = APIRouter()

fastf1.Cache.enable_cache("cache")

@router.get("/fastest-lap")
def get_fastest_lap_telemetry(year: int, race: str, session: str, driver: str):
    """
    Example:
    /api/telemetry/fastest-lap?year=2023&race=monza&session=Q&driver=VER
    
    """

    try:
        session_obj = fastf1.get_session(year, race, session)
        session_obj.load()

        lap = session_obj.laps.pick_driver(driver).pick_fastest()
        telemetry = lap.get_car_data().add_distance()

        return{
            "driver": driver,
            "lap_number": int(lap["LapNumber"]),
            "lap_time": str(lap["LapTime"]),
            "telemetry": {
                "distance": telemetry["Distance"].fillna(0).round(2).tolist(),
                "speed": telemetry["Speed"].fillna(0).tolist(),
                "throttle": telemetry["Throttle"].fillna(0).tolist(),
                "brake": telemetry["Brake"].fillna(0).astype(int).tolist(),
            },
        }
    
    except Exception as e:
        return {"error": str(e)}
    