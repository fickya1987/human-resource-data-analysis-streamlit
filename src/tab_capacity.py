import pandas as pd
import streamlit as st
import updated_data as data  # Pastikan menggunakan updated_data
import utils
import plots


def render(df: pd.DataFrame):
    # Show KPI cards section
    __build_kpi_cards(df)
    # Show plots
    __build_dept_promo_retrench_plots(df)


def __build_kpi_cards(df):
    with st.expander("Overall promotion & retrenchment stats...", expanded=True):
        utils.show_questions(
            [
                "* Do we have a healthy promotion rate (min 10%)?",
                "* Are we above or below performance-based retrenchment rate (max 5%)?",
            ]
        )
        promo_col, retrench_col = st.columns(2)

        # Overall promotion stats
        with promo_col:
            __show_promotion_stats(df)
        # Overall retrenchment stats
        with retrench_col:
            __show_retrench_stats(df)

        with st.expander("View insights...", expanded=True):
            utils.show_insights(
                [
                    "* Rate of promotion is way short of the stipulated minimum promotion rate target.",
                    "* Retrenchment rate is more than double the stipulated maximum retrenchment rate, which is alarming.",
                ]
            )


def __show_promotion_stats(df):
    promo_cnt, not_promo_cnt, promo_pct, no_promo_pct = data.get_promo_count(df)
    utils.render_card(
        key="promo_card",
        title="Promote",
        value=promo_cnt,
        secondary_text=f" ({promo_pct})%",
        icon="fa-sharp fa-solid fa-user-check fa-xs",
        progress_value=int(promo_pct),
        progress_color="green",
    )
    utils.render_card(
        key="no_promo_card",
        title="No Promotion",
        value=not_promo_cnt,
        secondary_text=f" ({no_promo_pct})%",
        icon="fa-sharp fa-solid fa-user-xmark fa-xs",
        progress_value=int(no_promo_pct),
        progress_color="red",
    )


def __show_retrench_stats(df):
    retrench_cnt, not_retrench_cnt, retrench_pct, not_retrench_pct = data.get_retrench_count(df)
    utils.render_card(
        key="no_retrench_card",
        title="No Retrench",
        value=not_retrench_cnt,
        secondary_text=f" ({not_retrench_pct})%",
        icon="fa-sharp fa-solid fa-user-plus fa-xs",
        progress_value=int(not_retrench_pct),
        progress_color="green",
    )
    utils.render_card(
        key="retrench_card",
        title="Retrench",
        value=retrench_cnt,
        secondary_text=f" ({retrench_pct})%",
        icon="fa-sharp fa-solid fa-user-minus fa-xs",
        progress_value=int(retrench_pct),
        progress_color="red",
    )


def __build_dept_promo_retrench_plots(df):
    with st.expander("Analysis: Department wise promotion & retrenchment...", expanded=True):
        utils.show_questions(
            [
                "* How each department is doing in promoting employees?",
                "* Which department has the highest rate of retrenchment?",
            ]
        )

        promo_col, retrench_col = st.columns(2)
        with promo_col:
            df_promo = data.get_dept_promo_pct(df)
            fig = plots.plot_dept_promo_bar(df_promo)
            st.plotly_chart(fig, use_container_width=True)
        with retrench_col:
            df_retrench = data.get_dept_retrench_pct(df)
            fig = plots.plot_dept_retrench_bar(df_retrench)
            st.plotly_chart(fig, use_container_width=True)
        with st.expander("View Insights...", expanded=True):
            utils.show_insights(
                [
                    "* All departments are doing poorly in promoting employees, none even achieved 50% of the promotion target.",
                    "* Retrenchment rates are high in all departments, with R&D and Sales being the most critical.",
                ]
            )
