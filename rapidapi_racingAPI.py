import requests
import pandas as pd
from datetime import datetime
import re
from database.DBConnection import DbConnection
from DataFrame.ResultsDataframe import add_median_or_excluding_runner


def get_turf_handicap_racecards(day="tomorrow"):
    obj = DbConnection('mssql')
    obj.createConnection("AUTOCOMMIT")
    con = obj.connection

    url = "https://the-racing-api1.p.rapidapi.com/v1/racecards/free"

    querystring = {
        "day": day,
        "region_codes": ["ire", "gb"]
    }

    headers = {
        "x-rapidapi-key": "4f9e9e1672msh840c89f56a726e1p15c39fjsnf96f795b0305",
        "x-rapidapi-host": "the-racing-api1.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    # print(data)
    rows = []

    for race in data.get("racecards", []):

        race_type = race.get("type")
        race_name = race.get("race_name", "")
        surface = race.get("surface", "")
        race_date = race.get("date")

        month = int(datetime.strptime(race_date, "%Y-%m-%d").month)

        # ---------------------------------
        # raceType division
        # Turf / AW / Chase / Hurdle
        # ---------------------------------
        if race_type == "Flat":
            raceType = "AW" if surface == "AW" else "Turf"

        elif race_type == "Chase":
            if "Hurdle" in race_name:
                raceType = "Hurdle"
            else:
                raceType = "Chase"
        else:
            raceType = race_type

        if race_type == "Flat":
            raceType1 = "Flat"

        elif race_type == "Chase":
            if "Hurdle" in race_name:
                raceType1 = "Hurdle"
            else:
                raceType1 = "Chase"
        else:
            raceType1 = race_type

        handicap = ("Hcap" if "handicap" in race_name.lower() else "NonHcap" )

        # ---------------------------------
        # FILTER ONLY TURF HANDICAPS
        # ---------------------------------
        if raceType != "Turf" or handicap != "Hcap":
            continue

        # ---------------------------------
        # Prize money
        # ---------------------------------
        prize_raw = str(race.get("prize", ""))

        prize_match = re.search(r"([\d,]+)", prize_raw)

        prizeMoney = (
            int(prize_match.group(1).replace(",", ""))
            if prize_match
            else None
        )

        # ---------------------------------
        # Race class numeric
        # ---------------------------------
        race_class = str(race.get("race_class", ""))
        class_match = re.search(r"(\d+)", race_class)
        raceClassNumeric = (int(class_match.group(1)) if class_match else None )
        try:
            raceClassNumeric = int(raceClassNumeric)
        except (ValueError, TypeError):
            raceClassNumeric = None

        track = str(race.get("course", "")).replace("'", "")
        region = race.get("region")
        if region and region != "GB":
            track = f"{track} ({region})"
        # ---------------------------------
        # Race-level fields
        # ---------------------------------
        race_info = {
            "track": track,
            "raceTime": race.get("off_time"),
            "raceName": race.get("race_name"),
            "raceType": raceType,
            "raceType1": raceType1,
            "raceDate": race.get("date"),
            "month": month,
            "handicap": handicap,
            "distance": race.get("distance_f"),
            "yards": int(float(race.get("distance_f")) * 220 if race.get("distance_f") else None),
            "ageLimit": race.get("age_band"),
            "ORLimitNumerical": (str(race.get("rating_band")).split('-')[-1] if race.get("rating_band") else ""),
            "raceClass": race.get("race_class"),
            "raceClassNumeric": raceClassNumeric,
            "numberOfFences": "",
            "prizeMoney": prizeMoney,
        }

        # ---------------------------------
        # Runner-level fields
        # ---------------------------------
        for runner in race.get("runners", []):
            # Horse name + region
            horse_name = str(runner.get("horse", "")).replace("'", "")
            region = runner.get("region")
            if region and region != "GB":
                horse_name = f"{horse_name} ({region})"
            # Jockey
            jockey_raw = str(runner.get("jockey", "")).replace("'", "")
            match = re.match(r"^(.*?)(?:\((\d+)\))?$", jockey_raw)
            jockey_name = (match.group(1).strip() if match else jockey_raw)
            jockey_claim = (int(match.group(2)) if match and match.group(2) else "")
            # ---------------------------------
            # OR cleanup
            # ---------------------------------
            try:
                OR = int(runner.get("ofr"))
                # print(OR)
            except (ValueError, TypeError):
                OR = ""

            row = {
                **race_info,
                "horseName": horse_name,
                "horseNameRaw": str(runner.get("horse", "")).replace("'", ""),
                "horseID": "",
                "draw": runner.get("draw"),
                "htype": str(runner.get("sex_code", "")).lower(),
                "hcolor": runner.get("colour"),
                "hg": runner.get("headgear"),
                "age": int(runner.get("age")),
                "weight": int(runner.get("lbs")),
                "OR": OR,
                "jockey": jockey_name,
                "jockeyID": "",
                "jockeyClaim": jockey_claim,
                "trainer": str(runner.get("trainer", "")).replace("'", ""),
                "trainerID": "",
                "owner": "",
                "ownerID": "",
                "Race_Card_Median_OR": 0,
            }

            rows.append(row)

    df = pd.DataFrame(rows)
    df = df.replace('', None)
    df = add_median_or_excluding_runner(df)
    df["noOfRunners"] = (df.groupby(["raceDate", "raceTime"])["horseName"].transform("nunique"))
    # df.to_csv('d:/test.csv')
    DbConnection.importToTable('Race_Card_turf_handicap', con, df)


# get_turf_handicap_racecards('today')
