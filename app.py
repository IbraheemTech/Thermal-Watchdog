import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from groq import Groq
from analysis import (
    load_and_prepare, compute_monthly_trends,
    compute_annual_means, compute_overall_trend, project_temperature,
    MONTH_NAMES
)

# ---------- Page Configuration ----------
st.set_page_config(page_title="Bahawalpur Climate Detective", layout="wide")

# Custom CSS to make the Problem Statement look like a nice box
st.markdown("""
<style>
    .problem-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Load Data ----------
@st.cache_data
def get_data():
    df = load_prepare = load_and_prepare()
    return df, compute_monthly_trends(df), compute_annual_means(df), compute_overall_trend(df)

df, trends_df, annual_df, overall = get_data()

# ---------- Header & Problem Statement ----------
st.title("🌍 Thermal Watchdog ")
st.markdown("**25-Year NASA MERRA-2 Air Temperature Analysis (2002–2026)**")

st.markdown("""
<div class="problem-box">
    <h4>🎯 Problem Statement</h4>
    <p>Bahawalpur is a semi-arid agricultural hub where farmers rely on predictable seasonal temperatures for wheat (sown Nov-Dec) and cotton (summer). However, annual averages hide the real story. By analyzing 25 years of satellite data, we detect <b>hidden month-by-month climate signals</b> to reveal which specific seasons are statistically changing and what it means for local agriculture and livestock.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Overall Trend ----------
st.subheader("1. The Big Picture (All Months Mixed)")
col1, col2, col3 = st.columns(3)
col1.metric("Rate per decade", f"{overall['slope_per_decade']:+.3f} °C", help="The overall trend when all 12 months are mixed together.")
col2.metric("p-value", f"{overall['p_value']:.4f}", help="A p-value below 0.05 means the trend is statistically significant (not just random noise).")
col3.metric("Significant?", "No" if not overall['significant'] else "Yes")
st.caption("💡 **Why 'No'?** When you average all 12 months together, the extreme changes in summer are diluted by the stable temperatures in winter. This 'mixed' average hides the real story. That is why a true Trend Detective must look at each month individually below.")

st.divider()

# ---------- 12-Month Bar Chart ----------
st.subheader("2. Month-by-Month Fingerprint")
st.markdown("This chart shows **how fast** each month is changing per decade. **Red bars** indicate a statistically significant change (p < 0.05).")

plot_df = trends_df.copy()
plot_df['Color'] = plot_df['Significant'].map({True: 'Significant Change', False: 'No Significant Change'})

fig = px.bar(
    plot_df, x='Month', y='Rate_per_decade', color='Color',
    color_discrete_map={'Significant Change': '#d62728', 'No Significant Change': '#aec7e8'},
    labels={'Rate_per_decade': 'Change Rate (°C / decade)'},
    hover_data={'p_value': True}
)
fig.add_hline(y=0, line_width=2, line_color="black")
fig.update_layout(height=400, legend_title="", margin=dict(l=0, r=0, t=20, b=0))
st.plotly_chart(fig, use_container_width=True)

st.info("""
**📖 How to read this:** 
Bahawalpur is still extremely hot (reaching 40°C+ in summer). This chart shows the *rate of change*, not absolute temperature. 
The downward red bars mean June, July, and August are experiencing a **cooling trend** (about -0.9°C per decade). 
Scientists attribute this regional summer cooling to **increased irrigation** (evaporative cooling) and **aerosol pollution** blocking sunlight. 
*Note: Winters (Nov-Feb) show no significant change.*
""")

st.divider()

# ---------- Annual Line Chart ----------
st.subheader("3. Annual Average Temperature (2002–2025)")
fig_ann = px.line(annual_df, x='year', y='temp_c', markers=True,
                  labels={'year': 'Year', 'temp_c': 'Temperature (°C)'})
fig_ann.update_traces(line_color='#2ca02c', line_width=3, marker=dict(size=8))
fig_ann.update_layout(height=350, margin=dict(l=0, r=0, t=20, b=0))
st.plotly_chart(fig_ann, use_container_width=True)
st.caption("💡 This shows the year-over-year average. Because it mixes all seasons, it looks like a flat line, proving why month-by-month detection is necessary.")

st.divider()

# ---------- Month Explorer ----------
st.subheader("4. Deep Dive into a Specific Month")
selected = st.selectbox("Choose a month to analyze:", MONTH_NAMES, index=7) # Default to August
m_num = MONTH_NAMES.index(selected) + 1
m_df = df[df['month'] == m_num]

fig_m = px.scatter(m_df, x='year', y='temp_c', trendline='ols',
                   labels={'year': 'Year', 'temp_c': 'Temperature (°C)'},
                   title=f"Actual {selected} Temperatures in Bahawalpur (2002-2026)")
fig_m.update_traces(marker=dict(size=10, color='#1f77b4'), line=dict(color='red', width=3))
fig_m.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
st.plotly_chart(fig_m, use_container_width=True)

row = trends_df[trends_df['Month'] == selected].iloc[0]
sig_text = "a **Statistically Significant** change" if row['Significant'] else "**No Statistically Significant** change"
st.markdown(f"**Result for {selected}:** There is {sig_text} of `{row['Rate_per_decade']:+.3f} °C` per decade (p = `{row['p_value']:.4f}`).")

st.divider()

# ---------- Future Projection ----------
st.subheader("5. Future Projection (Linear Extrapolation)")
st.markdown(f"Based on the 25-year trend for **{selected}**, here is what the temperature might look like in the future if the trend continues.")
target_year = st.slider("Drag to select a target year:", 2026, 2050, 2035)
proj = project_temperature(df, m_num, target_year)

col_a, col_b = st.columns(2)
col_a.metric(
    f"Projected {selected} Temp in {target_year}",
    f"{proj['projected_temp']} °C",
    delta=f"{proj['change_from_baseline']:+.2f} °C vs {proj['baseline_year']}",
    delta_color="inverse" # Red for increase, Green for decrease
)
col_b.write("")
col_b.write("")
col_b.caption("⚠️ **Disclaimer:** This is a simple linear extrapolation, not a complex climate model prediction. It shows the direction of the current trend, but real climate factors can change.")

st.divider()

# ---------- AI Report ----------
st.subheader("6. AI Impact Report")
st.markdown("Click below to generate a localized impact report for farmers and livestock owners based on this specific analysis.")

if st.button("🤖 Generate Report with Groq AI", use_container_width=True):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        facts = trends_df[['Month', 'Rate_per_decade', 'p_value', 'Significant']].to_string(index=False)
        
        prompt = f"""You are an agricultural climate analyst writing for farmers and livestock owners in Bahawalpur, Pakistan.
Use ONLY the facts below. Do NOT invent numbers. Label any statement beyond the data as "inference".

Full 12-Month Temperature Trends (NASA MERRA-2, 2002-2026):
{facts}

The user is specifically looking at {selected}. 
Projected {selected} temperature for {target_year}: {proj['projected_temp']} °C (Change of {proj['change_from_baseline']:+.2f} °C vs {proj['baseline_year']}).

Background: Bahawalpur is semi-arid. Wheat is sown Nov-Dec. Cotton is heat-sensitive in summer. Goats suffer heat stress in hot months.

Write a well-structured, justified 150-200 word report (use bullet points for readability) covering:
1. Which months show statistically significant change (name them and direction).
2. Specifically address the outlook for {selected} based on the projection.
3. What this might mean for wheat sowing, cotton, and goat heat stress.
4. One sentence noting that projections need local validation.
"""
        resp = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        # Justify the text and add a nice styling
        st.markdown(f"<div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; border-left: 5px solid #2ca02c;'>{resp.choices[0].message.content}</div>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")