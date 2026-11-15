<div align="center">

# 🐕‍🦺 The Thermal Watchdog
### *Uncovering the Hidden Climate Signals of Bahawalpur*

[![NASA Space Apps Challenge](https://img.shields.io/badge/NASA-Space%20Apps%20Challenge-blue?style=for-the-badge&logo=nasa)](https://www.spaceappschallenge.org/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq AI](https://img.shields.io/badge/Groq%20AI-Enabled-purple?style=for-the-badge)](https://groq.com/)

**An interactive, AI-assisted web application analyzing 25 years (2002–2026) of NASA MERRA-2 satellite data.**

[Explore the App](#-key-features) • [Read the Findings](#-key-findings) • [Install Locally](#%EF%B8%8F-how-to-run-locally)

</div>

---

## 📌 Executive Summary

**The Thermal Watchdog** is a data-driven climate detective tool designed for **Bahawalpur, Pakistan**. By isolating monthly temperature data, the tool reveals that while annual averages appear stable, there is a **statistically significant cooling trend** in peak summer months (June, July, August) due to localized factors like irrigation and aerosols. 

The app translates these complex statistical findings into actionable insights for local agriculture and livestock management, empowering farmers to adapt to shifting thermal regimes.

---

## 🎯 Problem Statement

Bahawalpur is a semi-arid agricultural hub in South Punjab, Pakistan. The local economy heavily relies on predictable seasonal temperatures for winter wheat, summer cotton, and livestock (goats). However, analyzing raw annual weather data dilutes extreme seasonal changes with stable months. 

Farmers and policymakers currently lack a tool that:
1. **Isolates** month-by-month trends.
2. **Proves** whether these changes are statistically significant.
3. **Translates** satellite data into localized, easy-to-understand agricultural impacts.

---

## 🚀 Key Features & Functional Requirements

*   📊 **F1: The Big Picture (Annual Trend):** Displays overall trend metrics to demonstrate how mixing seasons dilutes the climate signal.
*   🔍 **F2: 12-Month Fingerprint:** A bar chart showing the rate of change per decade for each month. Red bars indicate statistically significant changes (\(p \le 0.05\)).
*   📈 **F3: Deep Dive Explorer:** A dropdown menu allowing users to view historical scatter plots with linear trendlines for specific months.
*   🔮 **F4: Future Projection:** An interactive slider that extrapolates the historical trend to a target year (up to 2050) and displays the delta from the 2002 baseline.
*   🤖 **F5: AI Impact Report:** A Groq AI integration (`openai/gpt-oss-120b`) that synthesizes the statistical data and generates a custom, plain-English report for farmers based on the user's selected month and projection year.

---

## 📊 Key Findings (Results)

*   **Overall Annual Trend:** Not statistically significant (\(p=0.986\)). *Seasonal noise dilutes the annual average.*
*   **Summer Cooling:** **June** (\(-0.70^\circ\text{C/decade}\), \(p=0.017\)), **July** (\(-0.96^\circ\text{C/decade}\), \(p=0.011\)), and **August** (\(-0.87^\circ\text{C/decade}\), \(p=0.020\)) show statistically significant cooling.
*   **Winter Stability:** November–February show no significant change, meaning winter sowing conditions for wheat are currently stable.
*   **Hypothesis for Summer Cooling:** Increased regional irrigation (evaporative cooling) and aerosol pollution blocking sunlight in the Indo-Gangetic Plain.

---

## 🛠️ Technical Architecture

| Component | Technology Used |
| :--- | :--- |
| **Frontend / Backend** | Streamlit (Python) |
| **Data Source** | [NASA Giovanni](https://giovanni.gsfc.nasa.gov/) (MERRA-2 Reanalysis `M2TMNXSLV`) |
| **Data Processing** | `pandas`, `scipy.stats` (Linear Regression) |
| **Visualization** | `plotly.express`, `plotly.graph_objects` |
| **AI Integration** | Groq API (Llama 3 / GPT-OSS) |

### 🧠 Data & Methodology
1.  **Data Cleaning:** The raw NASA CSV is loaded (skipping metadata headers). Temperature is converted from Kelvin to Celsius.
2.  **Trend Calculation:** Data is grouped by month. For each month, a linear regression is performed against the year.
3.  **Significance Testing:** The p-value from the regression determines if the trend is a real signal or just noise (threshold < 0.05).
4.  **Projection:** Simple linear extrapolation based on the slope of the trendline.

---

## 🎨 UI/UX Design Principles
*   **Judge/User Friendly:** No raw code visible. Explanations (tooltips and info boxes) are provided directly under every chart so non-technical users know exactly what they are looking at.
*   **Accessibility:** High-contrast charts (Red for significant, Blue for non-significant).
*   **Defensive AI:** The AI prompt explicitly forbids hallucination and requires the output to be labeled as "inference" where appropriate.

---

## ⚙️ How to Run Locally

Follow these steps to run the Thermal Watchdog on your machine:

**1. Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
cd YOUR-REPO-NAME
