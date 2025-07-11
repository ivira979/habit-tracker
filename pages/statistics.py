import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
import altair as alt

page_title = "Statistics"
page_list = ["Home",  "Submission Form", "Last Completed", "Analytics", "Statistics", "Habit Manager"]
curr_index = page_list.index(page_title)

st.title(page_title)
selected = option_menu(None, page_list, 
    icons=['house', "list-task", "calendar-check", "bar-chart", "graph-up-arrow", "database-fill-gear"], 
    menu_icon="cast", default_index=curr_index, orientation="vertical")

# Add page description
st.caption("📈 Statistics: View summary statistics for your daily habit completions.")

if selected == page_title:
    pass
elif selected == "Home":
    st.switch_page("home.py")
elif selected == "Submission Form":
    st.switch_page("pages/submission_form.py")
elif selected == "Last Completed":
    st.switch_page("pages/last_completed.py")
elif selected == "Analytics":
    st.switch_page("pages/analytics_test.py")
elif selected == "Statistics":
    st.switch_page("pages/statistics.py")
elif selected == "Habit Manager":
    st.switch_page("pages/habit_manager.py")
else:
    pass

st.header("Daily Habit Completion Statistics")

conn = st.connection("postgresql", type="sql")

with st.form("statistics_form"):
    st.subheader("Report Parameters")
    granularity = st.selectbox("Select granularity", ["Weekly", "Monthly", "Yearly"])
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", value=datetime.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End date", value=datetime.today())
    use_current_period = st.checkbox(
        "Use current period to date", value=False,
        help="If selected, the report will use the current week/month/year up to today, based on the selected granularity. Overrides the 'Use full period(s)' option."
    )
    if use_current_period:
        st.caption("🔹 The report will use the current period (week/month/year) up to today, regardless of the selected date range.")
    use_full_period = st.checkbox(
        "Use full period(s) for selected granularity", value=False,
        help="If selected, the report will include all full periods (weeks/months/years) that overlap your selected date range."
    )
    if use_full_period and not use_current_period:
        st.caption("🔹 The report will include all full periods (weeks/months/years) that overlap your selected date range. For example, if your dates span two months, both months will be included in full.")
    submitted = st.form_submit_button("Generate Report")

if submitted:
    if start_date > end_date:
        st.error("Start date must be before end date.")
    else:
        today = datetime.today().date()
        adj_start = start_date
        adj_end = end_date
        if use_current_period:
            if granularity == "Yearly":
                adj_start = datetime(today.year, 1, 1).date()
                adj_end = today
            elif granularity == "Monthly":
                adj_start = datetime(today.year, today.month, 1).date()
                adj_end = today
            elif granularity == "Weekly":
                adj_start = today - timedelta(days=today.weekday())
                adj_end = today
        elif use_full_period:
            if granularity == "Yearly":
                years = range(start_date.year, end_date.year + 1)
                adj_start = datetime(years[0], 1, 1).date()
                adj_end = datetime(years[-1], 12, 31).date()
            elif granularity == "Monthly":
                months = []
                y, m = start_date.year, start_date.month
                while (y < end_date.year) or (y == end_date.year and m <= end_date.month):
                    months.append((y, m))
                    if m == 12:
                        y += 1
                        m = 1
                    else:
                        m += 1
                adj_start = datetime(months[0][0], months[0][1], 1).date()
                last_y, last_m = months[-1]
                last_day = calendar.monthrange(last_y, last_m)[1]
                adj_end = datetime(last_y, last_m, last_day).date()
            elif granularity == "Weekly":
                adj_start = (start_date - timedelta(days=start_date.weekday()))
                adj_end = (end_date + timedelta(days=(6 - end_date.weekday())))
        # Only daily habits
        habit_type_code = 'D'
        date_filter = f"submission_date BETWEEN '{adj_start}' AND '{adj_end}'"
        group_by = ""
        select_fields = "h.habit_name"

        if granularity == "Weekly":
            group_by = "GROUP BY h.habit_name, EXTRACT(YEAR FROM submission_date), EXTRACT(WEEK FROM submission_date)"
            select_fields += ", EXTRACT(YEAR FROM submission_date) AS year, EXTRACT(WEEK FROM submission_date) AS week"
        elif granularity == "Monthly":
            group_by = "GROUP BY h.habit_name, EXTRACT(YEAR FROM submission_date), EXTRACT(MONTH FROM submission_date)"
            select_fields += ", EXTRACT(YEAR FROM submission_date) AS year, EXTRACT(MONTH FROM submission_date) AS month"
        elif granularity == "Yearly":
            group_by = "GROUP BY h.habit_name, EXTRACT(YEAR FROM submission_date)"
            select_fields += ", EXTRACT(YEAR FROM submission_date) AS year"

        agg = "SUM(hs.submission_value) AS completions"

        query = f"""
            SELECT {select_fields}, {agg}
            FROM habit_submission hs
            JOIN habits h ON hs.sub_habit_id = h.habit_id
            WHERE {date_filter} AND h.habit_type = '{habit_type_code}'
            {group_by}
            ORDER BY h.habit_name
        """

        df = conn.query(query)
        st.info(
            f"Report for: **Daily** habits | Granularity: **{granularity}** | "
            f"Date range: **{adj_start}** to **{adj_end}**"
        )
        if df.empty:
            st.warning("No data found for the selected parameters.")
        else:
            days_in_period = (adj_end - adj_start).days + 1
            # Calculate total possible completions
            # Get all active daily habits in the period
            habits_df = conn.query("SELECT habit_id, habit_name FROM habits WHERE habit_type = 'D' AND active_flag = TRUE")
            num_habits = len(habits_df)
            total_possible = num_habits * days_in_period if num_habits > 0 else 1
            total_completed = df["completions"].sum()
            overall_pct = (total_completed / total_possible * 100) if total_possible > 0 else 0
            st.success("Report generated successfully! You have completed " 
                       f"{overall_pct:.2f}% of daily habits in the selected period. Wah Wah!")
            st.metric(
                label="Aggregate Completion Percentage",
                value=f"{overall_pct:.2f}%",
                help="This is the percentage of all daily habit completions out of all possible completions for the selected period."
            )
            summary = (
                df.groupby("habit_name")["completions"]
                .sum()
                .reset_index()
                .assign(**{
                    "Percent Completions": lambda x: (x["completions"] / days_in_period * 100).map(lambda v: f"{v:.2f}%")
                })
                .drop(columns=["completions"])
            )
            
            st.dataframe(summary.rename(columns={"habit_name": "Habit Name"}), use_container_width=True)
            # Visualization: Line chart for percent completions over time per habit
            st.subheader("Percent Completions Over Time by Habit")
            # Query for completions by habit and date for the selected period
            chart_query = f"""
                SELECT h.habit_name AS "Habit Name", hs.submission_date AS "Date", SUM(hs.submission_value) AS "Completions"
                FROM habit_submission hs
                JOIN habits h ON hs.sub_habit_id = h.habit_id
                WHERE {date_filter} AND h.habit_type = 'D'
                GROUP BY h.habit_name, hs.submission_date
                ORDER BY h.habit_name, hs.submission_date
            """
            chart_df = conn.query(chart_query)
            if not chart_df.empty:
                # Calculate percent completions per habit per day
                # Use the number of active daily habits for normalization
                chart_df["Percent Completion"] = chart_df["Completions"] / num_habits * 100 if num_habits > 0 else 0

                # Aggregate by date for overall percent completion
                agg_df = chart_df.groupby("Date", as_index=False).agg(
                    {"Percent Completion": "mean"}
                )
                agg_df["Type"] = "Average"
                # Find min/max for highlighting
                min_idx = agg_df["Percent Completion"].idxmin()
                max_idx = agg_df["Percent Completion"].idxmax()

                # Plot per-habit lines and overall average
                base = alt.Chart(chart_df).mark_line(point=True).encode(
                    x=alt.X("Date:T", title="Date"),
                    y=alt.Y("Percent Completion:Q", title="Percent Completion (%)"),
                    color=alt.Color("Habit Name:N", scale=alt.Scale(scheme="category20b")),
                    tooltip=[
                        alt.Tooltip("Habit Name:N"),
                        alt.Tooltip("Date:T"),
                        alt.Tooltip("Percent Completion:Q", format=".2f")
                    ]
                )

                avg_line = alt.Chart(agg_df).mark_line(point=True, color="black", strokeDash=[5,5]).encode(
                    x="Date:T",
                    y="Percent Completion:Q",
                    tooltip=[
                        alt.Tooltip("Date:T"),
                        alt.Tooltip("Percent Completion:Q", format=".2f")
                    ]
                )

                # Highlight min/max points on the average line
                highlight_points = alt.Chart(agg_df.loc[[min_idx, max_idx]]).mark_point(
                    color="red", size=120, filled=True, shape="diamond"
                ).encode(
                    x="Date:T",
                    y="Percent Completion:Q",
                    tooltip=[
                        alt.Tooltip("Date:T"),
                        alt.Tooltip("Percent Completion:Q", format=".2f")
                    ]
                )

                chart = (base + avg_line + highlight_points).properties(
                    width="container",
                    height=350
                ).interactive()

                st.altair_chart(chart, use_container_width=True)
                st.caption("Dashed black line shows the average percent completion across all daily habits. Red diamonds highlight min/max average days.")
            else:
                st.caption("No date breakdown available for this granularity.")
