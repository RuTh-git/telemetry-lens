from fastapi import APIRouter 
import fastf1 

router = APIRouter()

# Enable caching so we don't download data every time 
fastf1.Cache.enable_cache("cache")

@router.post("/load")
def load_session(year: int, race: str, session: str):
    """
    Load an F1 session and return the drivers.
    Example:
    year = 2024
    race = "Suzuka"
    session = "R"

    """

    try:
        session_obj = fastf1.get_session(year, race, session)
        session_obj.load()

        driver_numbers = session_obj.drivers
        results = session_obj.results

        drivers = []

        for number in driver_numbers:
            try:
                driver_row = results[results["DriverNumber"] == str(number)].iloc[0]

                drivers.append(
                    {
                        "driver_name": str(number),
                        "code": driver_row.get("Abbreviation"), 
                        "full_name": driver_row.get("FullName"),
                        "team_name": driver_row.get("TeamName"),
                    }
                )
            except Exception:
                drivers.append(
                    {
                        "driver_number": str(number),
                        "code": None,
                        "full_name": None,
                        "team_name": None,

                    }
                )


        return {
            "year": year, 
            "race": race,
            "session": session,
            "drivers": drivers,
        }
    
    except Exception as e:
        return {"error": str(e)}