import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
import altair as alt

page_title = "Analytics"
page_list = ["Home",  "Submission Form", "Last Completed", "Analytics", "Statistics", "Habit Manager"]
curr_index = page_list.index(page_title)

st.title(page_title)
selected = option_menu(
    None, page_list,
    icons=['house', "list-task", "calendar-check", "bar-chart", "graph-up-arrow", "database-fill-gear"],
    menu_icon="cast", default_index=curr_index, orientation="vertical"
)

# Add page description
st.caption("📊 Analytics: Visualize and analyze your habit completion trends.")

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

st.header("Habit Analytics Report")

conn = st.connection("postgresql", type="sql")

with st.form("analytics_form"):
    st.subheader("Report Parameters")
    granularity = st.selectbox("Select granularity", ["Weekly", "Monthly", "Yearly"])
    habit_type = st.selectbox("Select habit type", ["Daily", "Other"])
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
    # Validate date range
    if start_date > end_date:
        st.error("Start date must be before end date.")
    else:
        # Determine date range based on checkboxes
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
                # Find all months between start and end
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
                # ISO week: Monday is the first day of the week
                # Find all weeks between start and end
                # Set adj_start to the Monday of the first week, adj_end to Sunday of the last week
                adj_start = (start_date - timedelta(days=start_date.weekday()))
                adj_end = (end_date + timedelta(days=(6 - end_date.weekday())))
        habit_type_code = 'D' if habit_type == "Daily" else 'O'
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
            f"Report for: **{habit_type}** habits | Granularity: **{granularity}** | "
            f"Date range: **{adj_start}** to **{adj_end}**"
        )
        if df.empty:
            st.warning("No data found for the selected parameters.")
        else:
            if habit_type_code == 'D':
                days_in_period = (adj_end - adj_start).days + 1
                summary = (
                    df.groupby("habit_name")["completions"]
                    .sum()
                    .reset_index()
                    .assign(**{
                        "Percent Completions": lambda x: (x["completions"] / days_in_period * 100).map(lambda v: f"{v:.2f}%")
                    })
                    .drop(columns=["completions"])
                )
                st.success("Report generated successfully!")
                st.dataframe(summary.rename(columns={"habit_name": "Habit Name"}), use_container_width=True)
                # Visualization: Mobile-optimized Altair bar chart for percent completions
                st.subheader("Percent Completions by Habit")
                chart_data = summary.rename(columns={"habit_name": "Habit Name"})
                chart_data["Percent Completions (numeric)"] = chart_data["Percent Completions"].str.rstrip('%').astype(float)
                bar_chart = alt.Chart(chart_data).mark_bar(size=32).encode(
                    y=alt.Y("Habit Name:N", sort='-x', title=None, axis=alt.Axis(labelLimit=250, labelFontSize=16)),
                    x=alt.X("Percent Completions (numeric):Q", title="Percent Completions (%)", axis=alt.Axis(format=".2f", labelFontSize=16)),
                    color=alt.Color("Habit Name:N", scale=alt.Scale(scheme="category20b"), legend=None),
                    tooltip=[
                        alt.Tooltip("Habit Name:N"),
                        alt.Tooltip("Percent Completions (numeric):Q", format=".2f")
                    ]
                ).properties(
                    width="container",
                    height=80 * max(1, len(chart_data))
                ).configure_axis(
                    labelFontSize=16,
                    titleFontSize=16
                ).configure_view(
                    strokeWidth=0
                )
                st.altair_chart(bar_chart, use_container_width=True)
            else:
                summary = (
                    df.groupby("habit_name")["completions"]
                    .sum()
                    .reset_index()
                    .rename(columns={"habit_name": "Habit Name", "completions": "Total Completions"})
                )
                st.success("Report generated successfully!")
                st.dataframe(summary, use_container_width=True)
                # Visualization: Mobile-optimized Altair bar chart for total completions
                st.subheader("Total Completions by Habit")
                bar_chart = alt.Chart(summary).mark_bar(size=32).encode(
                    y=alt.Y("Habit Name:N", sort='-x', title=None, axis=alt.Axis(labelLimit=250, labelFontSize=16)),
                    x=alt.X("Total Completions:Q", title="Total Completions", axis=alt.Axis(labelFontSize=16)),
                    color=alt.Color("Habit Name:N", scale=alt.Scale(scheme="category20b"), legend=None),
                    tooltip=[
                        alt.Tooltip("Habit Name:N"),
                        alt.Tooltip("Total Completions:Q")
                    ]
                ).properties(
                    width="container",
                    height=80 * max(1, len(summary))
                ).configure_axis(
                    labelFontSize=16,
                    titleFontSize=16
                ).configure_view(
                    strokeWidth=0
                )
                st.altair_chart(bar_chart, use_container_width=True)