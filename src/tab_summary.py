import pandas as pd
import streamlit as st
import updated_data as data  # Gunakan updated_data
import utils
from config import app_config


def render(df: pd.DataFrame):
    # Show sample data in a dataframe
    __show_sample_data(df)
    # Show KPI cards section
    __build_kpi_cards(df)
    # Show plots
    __build_age_plots(df)
    __build_dept_plots(df)
    __build_exp_plots(df)


def __show_sample_data(df: pd.DataFrame):
    """Display sample data as pandas DataFrame"""
    with st.expander("View sample data | Download dataset..."):
        st.markdown("#### Top 5 rows")
        st.dataframe(df.head(5))
        st.markdown("#### Bottom 5 rows")
        st.dataframe(df.tail(5))
        # Read the file again and then download
        csv = data.df_to_csv(app_config.data_file)  # Revisi untuk menggunakan updated_data
        utils.download_file(
            btn_label="Download As CSV",
            data=csv,
            file_name="hr_data_downloaded.csv",
            mime_type="text/csv",
        )


def __build_kpi_cards(df: pd.DataFrame):
    """display total, male, female employees cards"""
    with st.expander("View Gender Stats...", expanded=True):
        utils.show_questions(
            [
                "* Do we have a balanced workforce in terms of gender?",
            ]
        )

        tot_emp_cnt, male_emp_cnt, female_emp_cnt, male_pct, female_pct = data.get_gender_count(df)

        with st.container():
            g_col1, g_col2, g_col3 = st.columns(3)
            with g_col1:
                utils.render_card(
                    key="tot_card",
                    title="Total<br>Employees",
                    value=tot_emp_cnt,
                    icon="fa-sharp fa-solid fa-venus-mars fa-xs",
                )
            with g_col2:
                utils.render_card(
                    key="male_card",
                    title="Males",
                    value=male_emp_cnt,
                    secondary_text=f" ({male_pct})%",
                    icon="fa-sharp fa-solid fa-mars fa-xs",
                    progress_value=int(male_pct),
                    progress_color="#186ee8",
                )
            with g_col3:
                utils.render_card(
                    key="female_card",
                    title="Females",
                    value=female_emp_cnt,
                    secondary_text=f" ({female_pct})%",
                    icon="fa-sharp fa-light fa-venus fa-xs",
                    progress_value=int(female_pct),
                    progress_color="#ff6d6d",
                )


def __build_age_plots(df: pd.DataFrame):
    pass  # Tambahkan logika sesuai kebutuhan


def __build_dept_plots(df: pd.DataFrame):
    pass  # Tambahkan logika sesuai kebutuhan


def __build_exp_plots(df: pd.DataFrame):
    pass  # Tambahkan logika sesuai kebutuhan
