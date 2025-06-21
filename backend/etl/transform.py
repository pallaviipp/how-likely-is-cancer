import pandas as pd

def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and map raw dataset fields to match frontend/backend parameters.
    """
    df.replace(9, pd.NA, inplace=True)  # 9 is used as missing data

    # Map categorical values
    age_group_map = {
        1: "20–24", 2: "25–29", 3: "30–34", 4: "35–39",
        5: "40–44", 6: "45–49", 7: "50–54", 8: "55–59",
        9: "60+"
    }
    race_map = {
    1: "White",
    2: "Black",
    3: "Hispanic",
    4: "Asian or Pacific Islander",
    5: "Native American",
    6: "Other",
    9: pd.NA
    }

    df["race_ethnicity"] = df["race_eth"].map(race_map)

    density_map = {1: "Almost entirely fatty", 2: "Scattered fibroglandular", 3: "Heterogeneously dense", 4: "Extremely dense"}
    bmi_map = {1: "<18.5", 2: "18.5–24.9", 3: "25–29.9", 4: "30+", 9: pd.NA}
    hrt_map = {1: "No", 2: "Yes", 9: pd.NA}
    menop_map = {1: "No", 2: "Yes", 3: "Unknown"}

    df["age_group"] = df["age_group_5_years"].map(age_group_map)
    df["bmd_density"] = df["BIRADS_breast_density"].map(density_map)
    df["bmi_group"] = df["bmi_group"].map(bmi_map)
    df["hrt_use"] = df["current_hrt"].map(hrt_map)
    df["menopause"] = df["menopaus"].map(menop_map)
    df["relatives_with_cancer"] = df["first_degree_hx"]

    # Drop unused columns or rename for clarity
    df = df.rename(columns={
        "age_menarche": "age_menarche",
        "age_first_birth": "age_first_birth",
        "count": "cases"
    })

    keep_cols = [
    "age_group", "race_ethnicity", "age_menarche", "age_first_birth",
    "bmd_density", "hrt_use", "menopause", "bmi_group", "relatives_with_cancer", "cases"
    ]

    df = df[keep_cols]

    # Drop rows with missing values in key predictors
    df.dropna(subset=["age_group", "age_menarche", "age_first_birth", "cases"], inplace=True)

    return df


