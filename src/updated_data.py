import pandas as pd
from pandas import DataFrame


def load_transform(file) -> DataFrame:
    """Load the raw data and prepare/transform it"""
    df = pd.read_csv(file)

    # Handle missing data
    df.fillna(0, inplace=True)

    # Feature Engineering for Promotion Analysis
    df['ToBePromoted'] = ((df['YearsSinceLastPromotion'] >= 5) & 
                          (df['PerformanceRating'] > 2)).astype(int)

    return df


def get_filter_options(df, empty_filters=False):
    """Returns filter fields options to fill filter or clear filter fields"""
    if empty_filters:
        filter_opt = {
            "Gender": [],
            "Department": [],
            "EducationField": [],
            "JobRole": [],
            "Age": [df["Age"].min(), df["Age"].max()],
            "YearsAtCompany": [df["YearsAtCompany"].min(), df["YearsAtCompany"].max()],
        }
    else:
        filter_opt = {
            "Gender": df["Gender"].unique().tolist(),
            "Department": df["Department"].unique().tolist(),
            "EducationField": df["EducationField"].unique().tolist(),
            "JobRole": df["JobRole"].unique().tolist(),
            "Age": [df["Age"].min(), df["Age"].max()],
            "YearsAtCompany": [df["YearsAtCompany"].min(), df["YearsAtCompany"].max()],
        }
    return filter_opt


def get_dept_stats_df(df: DataFrame):
    """Calculate various stats for each department and returns results in a DataFrame"""
    df_dept = (
        df.groupby("Department")[
            [
                "MonthlyIncome",
                "PercentSalaryHike",
                "TotalWorkingYears",
                "YearsAtCompany",
                "TrainingTimesLastYear",
            ]
        ]
        .mean()
        .round(2)
    )
    df_ot = (
        df.query("OverTime == 'Yes'")
        .groupby("Department")["OverTime"]
        .count()
        .to_frame()
    )
    df_dept_stat = df_dept.join(df_ot, how="inner").reset_index()
    return df_dept_stat


def get_gender_count(df: DataFrame):
    """Calculates employee total count and for each gender,
    returns count and percentage as result"""
    df_gender = df.groupby("Gender").size()
    male_emp_cnt = df_gender.get("Male", 0)
    female_emp_cnt = df_gender.get("Female", 0)
    tot_emp_cnt = male_emp_cnt + female_emp_cnt
    male_pct = round((male_emp_cnt / tot_emp_cnt) * 100, 2)
    female_pct = round((female_emp_cnt / tot_emp_cnt) * 100, 2)
    return tot_emp_cnt, male_emp_cnt, female_emp_cnt, male_pct, female_pct


def get_promo_count(df: DataFrame):
    """Calculates number of employees due for promotion,
    returns count and percentage as result"""
    df_promo = df.groupby("ToBePromoted").size()
    promo_cnt = df_promo.get(1, 0)  # 1 represents "Yes" in binary
    not_promo_cnt = df_promo.get(0, 0)
    tot_emp_cnt, _, _, _, _ = get_gender_count(df)
    promo_pct = round((promo_cnt / tot_emp_cnt) * 100, 2)
    not_promo_pct = round((not_promo_cnt / tot_emp_cnt) * 100, 2)
    return promo_cnt, not_promo_cnt, promo_pct, not_promo_pct


def df_to_csv(file: str) -> bytes:
    """Read file again and return as as a csv"""
    df = pd.read_csv(file)
    return df.to_csv(index=False).encode("utf-8")
