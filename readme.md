The Thermal Watchdog is an interactive, AI-assisted web application that analyzes 25 years (2002–2026) of NASA satellite data to detect hidden climate trends. By isolating monthly temperature data, the tool reveals that while annual averages appear stable, there is a statistically significant cooling trend in peak summer months (June, July, August) due to localized factors like irrigation and aerosols. The app translates these complex statistical findings into actionable insights for local agriculture and livestock management.
2. Problem Statement
Bahawalpur is a semi-arid agricultural hub in South Punjab, Pakistan. The local economy heavily relies on predictable seasonal temperatures for winter wheat, summer cotton, and livestock (goats). However, analyzing raw annual weather data dilutes extreme seasonal changes with stable months. Farmers and policymakers lack a tool that:
Isolates month-by-month trends.
Proves whether these changes are statistically significant.
Translates satellite data into localized, easy-to-understand agricultural impacts.
3. Goals & Objectives
Data Acquisition: Fetch and clean 25 years of 2-meter air temperature data from NASA MERRA-2.
Statistical Rigor: Apply linear regression and p-value testing (p≤0.05p≤0.05) to determine statistical significance.
Interactive Visualization: Provide a user-friendly dashboard for non-technical users to explore historical trends and future projections.
AI Integration: Use a Large Language Model (Groq/Llama 3) to generate localized impact reports for farmers (crops and livestock).
4. Target Audience
Local Farmers & Livestock Owners: To understand shifting planting windows and heat stress periods.
Agricultural Policymakers: To allocate resources for irrigation and heat mitigation.
Climate Researchers & Students: To visualize regional climate anomalies.
5. Key Features & Functional Requirements
F1: The Big Picture (Annual Trend): Displays overall trend metrics (Rate per decade, p-value) to demonstrate how mixing seasons dilutes the climate signal.
F2: 12-Month Fingerprint: A bar chart showing the rate of change per decade for each month. Red bars indicate statistically significant changes.
F3: Deep Dive Explorer: A dropdown menu allowing users to view historical scatter plots with linear trendlines for specific months.
F4: Future Projection: An interactive slider that extrapolates the historical trend to a target year (up to 2050) and displays the delta from the 2002 baseline.
F5: AI Impact Report: A Groq AI integration that synthesizes the statistical data and generates a custom, plain-English report for farmers based on the user's selected month and projection year.
6. Technical Architecture
Frontend/Backend: Streamlit (Python)
Data Source: NASA Giovanni (MERRA-2 Reanalysis M2TMNXSLV), exported as CSV.
Data Processing: pandas, scipy.stats (Linear Regression).
Visualization: plotly.express, plotly.graph_objects.
AI Integration: Groq API (openai/gpt-oss-120b).
7. Data & Methodology
Data Cleaning: The raw NASA CSV is loaded (skipping metadata headers). Temperature is converted from Kelvin to Celsius.
Trend Calculation: Data is grouped by month. For each month, a linear regression is performed against the year.
Significance Testing: The p-value from the regression determines if the trend is a real signal or just noise (threshold < 0.05).
Projection: Simple linear extrapolation based on the slope of the trendline.
8. Key Findings (Results)
Overall Trend: Not statistically significant (p=0.986p=0.986).
Summer Cooling: June (−0.70∘C/decade−0.70∘C/decade, p=0.017p=0.017), July (−0.96∘C/decade−0.96∘C/decade, p=0.011p=0.011), and August (−0.87∘C/decade−0.87∘C/decade, p=0.020p=0.020) show statistically significant cooling.
Winter Stability: November–February show no significant change, meaning winter sowing conditions for wheat are currently stable.
Hypothesis for Summer Cooling: Increased regional irrigation (evaporative cooling) and aerosol pollution blocking sunlight in the Indo-Gangetic Plain.
9. UI/UX Design Principles
Judge/User Friendly: No raw code visible. Explanations (tooltips and info boxes) are provided directly under every chart so non-technical users know exactly what they are looking at.
Accessibility: High-contrast charts (Red for significant, Blue for non-significant).
Defensive AI: The AI prompt explicitly forbids hallucination and requires the output to be labeled as "inference" where appropriate.
10. Future Scope
Integrate precipitation and soil moisture data from NASA GLDAS to see how the summer cooling correlates with rainfall.
Add a localized map overlay using NASA Worldview to visually show the expanding irrigation in Punjab.
Allow users to draw their own custom bounding boxes on a map to analyze any city globally.