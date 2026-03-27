

 HOSDT: Healthcare Operations
## Simulation & Diagnostic Toolkit
HOSDT is a high-fidelity Python-based simulation engine designed to model the operational
flow of a single-doctor clinic. Unlike basic random generators, it uses sequential queue logic
to simulate realistic patient behavior, administrative bottlenecks, and financial performance.
##  Project Overview
This toolkit provides a "Command Center" for clinic administrators or operations consultants. It
allows users to visualize how micro-variables—like registration delays or doctor
efficiency—impact the macro-metrics of a healthcare facility.
## ✨ Key Features
## ●
Sequential Queue Engine: Calculates real-time wait durations based on doctor
availability.
## ●
Dynamic Chaos Factors: Simulates peak-hour spikes (10 AM - 12 PM & 4 PM - 6 PM).
## ●
## Conditional Logic:
## ○
Registration: New patients take 3x longer than returning ones.
## ○
Pharmacy: Elderly patients (65+) have a higher probability of medication spend.
## ●
What-If Analysis: Interactive sidebar to adjust patient load and doctor speed on the fly.
##  Tech Stack
## ●
## Core: Python 3.10+
## ●
## Dashboard: Streamlit
## ●
Visuals: Plotly (Interactive Charts)
## ●
Data: Pandas & NumPy
## ●
Environment: Optimized for GitHub Codespaces (Low resource usage)
##  Core Metrics Tracked
## Metric Definition
Wait Duration Time from end of registration to doctor
entry.
Reg Duration Administrative time for
intake/documentation.
Pharmacy Conv. Percentage of patients purchasing meds

post-consult.
Traffic Density Heatmap of arrival clusters throughout the
day.
##  Setup & Installation
To run this in GitHub Codespaces or your local terminal:
## 1.
Clone the repository
git clone
[https://github.com/YOUR_USERNAME/HOSDT-Clinic-Sim.git](https://github.com/YOUR_USERN
AME/HOSDT-Clinic-Sim.git)
cd HOSDT-Clinic-Sim

## 2.
Install requirements
pip install streamlit pandas numpy plotly

## 3.
Launch the app
streamlit run app.py

##  Usage Guide
## 1.
Simulate: Use the sliders in the sidebar to set the "Daily Patients" and "Doctor Work Pace".
## 2.
Analyze: Check the Flow & Bottlenecks tab to see where the queue builds up.
## 3.
Audit: Go to the Detailed Ledger to see a row-by-row breakdown of every patient's
journey.
## 4.
Export: Click Export Log as CSV to save the simulated data for external reporting.
Developed by: Sravan
## Version: 1.0.0
License: MIT
