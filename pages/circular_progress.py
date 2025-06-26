import streamlit as st
from st_circular_progress import CircularProgress
import pandas as pd
import numpy as np

st.title("Circular Progress Component")



st.subheader("Install")
st.markdown("```pip install st-circular-progress```")
st.subheader("Sample Usage")            
with st.echo():
    def calculate_progress():
        if "slider" in st.session_state:
            cp.update_value(progress=st.session_state["slider"])
    columns = st.columns((1, 2))
    with columns[0]:
        cp = CircularProgress(
            value=0,
            label="Progress Indicator",
            size="Large",
            key="circular_progress_total",
        )
        cp.st_circular_progress()
    with columns[1]:
        st.slider(
            "Change progress to",
            min_value=0,
            max_value=100,
            on_change=calculate_progress,
            key="slider",
        )

data = [
    ["Feature #126", 55],
    ["Feature #95", 100],
    ["Feature #134", 24],
    ["Feature #77", 98],
    ["Feature #98", 32],
]
project_data = pd.DataFrame(data=data, columns=["Project Name", "Completion"])
project_data["color"] = project_data.apply(
    lambda x: "red"
    if x["Completion"] < 25
    else "orange"
    if x["Completion"] < 75
    else "green",
    axis=1,
)

widgets = {}
dashboard = st.columns(5)
for k, v in project_data.iterrows():
    with dashboard[k]:
        widgets[k] = CircularProgress(
            value=v["Completion"],
            label=v["Project Name"],
            size="Medium",
            key=f"dsh_{k}",
            color=v["color"],
        ).st_circular_progress()

st.write(project_data)