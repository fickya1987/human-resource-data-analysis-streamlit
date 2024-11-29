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

    # Feature Engineering for Retrenchment Analysis
    df["ToBeRetrenched"] = ((df["YearsInCurrentRole"] >= 10) & (df["PerformanceRating"] < 3)) | \
                           ((3 <= df["YearsInCurrentRole"]) & (df["YearsInCurrentRole"] < 10) & (df["PerformanceRating"] == 1))
    df["ToBeRetrenched"] = df["ToBeRetrenched"].map({True: "Yes", False: "No"})

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


def get_retrench_count(df: DataFrame):
    """Calculates number of employees due for retrenchment,
    returns count and percentage as result"""
    df_retrench = df.groupby("ToBeRetrenched").size()
    retrench_cnt = df_retrench.get("Yes", 0)
    not_retrench_cnt = df_retrench.get("No", 0)
    tot_emp_cnt = len(df)
    retrench_pct = round((retrench_cnt / tot_emp_cnt) * 100, 2)
    not_retrench_pct = round((not_retrench_cnt / tot_emp_cnt) * 100, 2)
    return retrench_cnt, not_retrench_cnt, retrench_pct, not_retrench_pct
