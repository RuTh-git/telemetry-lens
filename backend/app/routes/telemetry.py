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
    
@router.get("/compare")
def compare_drivers(year: int, race: str, session: str, driver1: str, driver2: str):
    """
    Compare fastest laps of two drivers
    """

    try:
        session_obj = fastf1.get_session(year, race, session)
        session_obj.load()

        # Driver 1 
        lap1 = session_obj.laps.pick_driver(driver1).pick_fastest()
        tel1 = lap1.get_car_data().add_distance()

        # Driver 2 
        lap2 = session_obj.laps.pick_driver(driver2).pick_fastest()
        tel2 = lap2.get_car_data().add_distance()

        return {
            "driver1": driver1,
            "driver2": driver2,
            "lap1_time": str(lap1["LapTime"]),
            "lap2_time": str(lap2["LapTime"]),
            "telemetry": {
                "driver1": {
                    "distance": tel1["Distance"].fillna(0).tolist(),
                    "speed": tel1["Speed"].fillna(0).tolist(),
                },
                "driver2": {
                    "distance": tel2["Distance"].fillna(0).tolist(),
                    "speed": tel2["Speed"].fillna(0).tolist(),
                },
            },
        }
    except Exception as e:
        return {"error": str(e)}
    