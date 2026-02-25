import streamlit as st
from render_awol_issue import render_awol
from render_annual_issue import render_annual
from render_abeyance import render_abeyance
from render_audio import render_audio_podcast
from render_furlough import render_furlough
from render_quiz import run_quiz
from render_powerpoint import render_powerpoint
from oral_reply_filing import render_orfiling
from render_jeopardy import run_jeopardy_game

st.title("Federal Advocacy Support Toolkit \n FAST - Provided by NTEU CH. 66")

st.subheader("📌 Select Grievance Type")

grievance_type = st.radio(
    "Choose the type of grievance you'd like to file:",
    [
        "Annual Appraisal",
        "AWOL - Annual/Sick Leave",
        "EO Abeyance",
        "Furlough",
        "Test Your Knowledge",
        "Steward Jeopardy",
        "Audio Clips - Podcast for Stewards",
        "Oral Reply Filing Form/POA",
        "PowerPoint Presentations",
    ],
    index=0,
)

if grievance_type == "Annual Appraisal":
    render_annual()

if grievance_type == "AWOL - Annual/Sick Leave":
    render_awol()

if grievance_type == "Furlough":
    render_furlough()

if grievance_type == "EO Abeyance":
    render_abeyance()

if grievance_type == "Audio Clips - Podcast for Stewards":
    render_audio_podcast()

if grievance_type == "Test Your Knowledge":
    run_quiz()

if grievance_type == "PowerPoint Presentations":
    render_powerpoint()

if grievance_type == "Oral Reply Filing Form/POA":
    render_orfiling()

if grievance_type == "Steward Jeopardy":
    run_jeopardy_game()
