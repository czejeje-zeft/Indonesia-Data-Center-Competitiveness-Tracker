import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re

# --- 1. CONFIG & STYLE ---
st.set_page_config(
    page_title="Indonesia Data Center Competitiveness Tracker",
    page_icon="🇮🇩",
    layout="wide"
)

# CSS TEMA PROFESIONAL (ADAPTIVE DARK/LIGHT)
st.markdown("""
<style>
    /* Global Font */
    html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
    
    /* Header Styling */
    h1 { font-weight: 700; letter-spacing: -1px; }
    h2, h3 { font-weight: 600; }
    
    /* Kartu Insight (Adaptive Theme) */
    .insight-box {
        background-color: var(--secondary-background-color);
        border-left: 4px solid #2962FF;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        font-size: 15px;
    }
    
    /* Highlight Text */
    .highlight { color: #2962FF; font-weight: bold; }
    .alert { color: #D50000; font-weight: bold; }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        color: gray;
        font-size: 12px;
        margin-top: 50px;
        border-top: 1px solid #ddd;
        padding-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA CLEANING ENGINE ---
def clean_numeric(value):
    if pd.isna(value): return 0
    value = str(value).lower().replace(',', '')
    if '-' in value:
        parts = re.findall(r"[\d\.]+", value)
        if len(parts) >= 2:
            return (float(parts[0]) + float(parts[1])) / 2
    matches = re.findall(r"[\d\.]+", value)
    if matches: return float(matches[0])
    return 0

def clean_tier_score(value):
    if pd.isna(value): return 0
    val_str = str(value)
    tier3, tier4 = 0, 0
    match3 = re.search(r'III[:\s]*(\d+)%', val_str)
    if match3: tier3 = float(match3.group(1))
    match4 = re.search(r'IV[:\s]*(\d+)%', val_str)
    if match4: tier4 = float(match4.group(1))
    return tier3 + tier4

# --- 3. LOAD DATA ---
@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_csv('Book1 (1).csv')
        df['dc_count'] = df['total_data_centers'].apply(clean_numeric)
        df['power_mw'] = df['power_capacity_MW_total'].apply(clean_numeric)
        df['internet_pen'] = df['internet_penetration_percent'].apply(clean_numeric)
        df['renewable_pct'] = df['average_renewable_energy_usage_percent'].apply(clean_numeric)
        df['growth_rate'] = df['growth_rate_of_data_centers_percent_per_year'].apply(clean_numeric)
        
        cols_percent = ['internet_pen', 'renewable_pct']
        for col in cols_percent:
            df[col] = df[col].apply(lambda x: x*100 if x <= 1 and x > 0 else x)
            df[col] = df[col].apply(lambda x: 100 if x > 100 else x)

        df['quality_score'] = df['tier_distribution'].apply(clean_tier_score)
        df = df[(df['power_mw'] > 0) & (df['internet_pen'] > 0)]
        return df
    except Exception as e:
        st.error(f"System Error: Gagal memuat dataset. {e}")
        return pd.DataFrame()

df = load_and_process_data()
if df.empty: st.stop()

# --- 4. HELPER FUNGSI VISUAL (THEME FRIENDLY) ---
def apply_pro_theme(fig):
    """Menerapkan tema profesional yang bersih"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

# --- 5. SIDEBAR ---
st.sidebar.markdown("### ⚙️ Configuration")
country_list = df['country'].unique().tolist()
defaults = ['Indonesia', 'Singapore', 'Malaysia', 'United States', 'China', 'Germany', 'Australia']
valid_defaults = [c for c in defaults if c in country_list]
selected_countries = st.sidebar.multiselect("Select Benchmark Countries:", country_list, default=valid_defaults)
df_filtered = df[df['country'].isin(selected_countries)].copy()

st.sidebar.markdown("---")
st.sidebar.info("""
**Tentang Dashboard:**
Alat ini memvisualisasikan daya saing infrastruktur digital nasional berdasarkan parameter SDG 9 (Infrastruktur) & SDG 13 (Climate Action).
""")

# --- 6. MAIN HEADER ---
st.title("🇮🇩 Indonesia Data Center Competitiveness Tracker")
st.markdown("""
<div style='font-size: 18px; color: gray; margin-bottom: 30px;'>
    Strategic Benchmarking: Infrastructure Resilience, Market Positioning, and Sustainability Readiness.
</div>
""", unsafe_allow_html=True)

# Navigasi Tab dengan Nama Profesional
tab1, tab2, tab3, tab4 = st.tabs([
    "🏭 Capacity & Scale",
    "🌐 Market Dynamics",
    "🛡️ Quality Landscape",
    "🌱 ESG & Sustainability"
])

# ==============================================================================
# TAB 1: KAPASITAS (SKALA)
# ==============================================================================
with tab1:
    st.subheader("Infrastructure Gap Analysis")
    st.caption("Komparasi Skala Fasilitas (Jumlah Gedung) vs Kapasitas Riil (Total Megawatt).")

    if not df_filtered.empty:
        df_melt = df_filtered.melt(id_vars='country', value_vars=['dc_count', 'power_mw'], var_name='Metrik', value_name='Nilai')
        df_melt['Metrik'] = df_melt['Metrik'].replace({'dc_count': 'Total Facilities (Units)', 'power_mw': 'Power Capacity (MW)'})

        fig_bar = px.bar(
            df_melt, x='country', y='Nilai', color='Metrik',
            barmode='group', log_y=True, text_auto='.2s',
            color_discrete_map={'Total Facilities (Units)': '#64B5F6', 'Power Capacity (MW)': '#1565C0'},
            title="Capacity Disparity Index (Logarithmic Scale)"
        )
        st.plotly_chart(apply_pro_theme(fig_bar), use_container_width=True)
        
        try:
            indo_power = df[df['country']=='Indonesia']['power_mw'].values[0]
            sg_power = df[df['country']=='Singapore']['power_mw'].values[0]
            
            st.markdown(f"""
            <div class="insight-box">
                <b>💡 Key Strategic Insight:</b><br>
                Terdapat ketimpangan struktural yang signifikan. Meskipun Indonesia memiliki jumlah fasilitas yang kompetitif, 
                total kapasitas dayanya (<b>{indo_power} MW</b>) masih tertinggal jauh dibandingkan hub regional Singapore (<b>{sg_power} MW</b>). 
                <br><br>
                Ini mengindikasikan pasar Indonesia masih terfragmentasi dengan banyak Data Center skala kecil, 
                belum mencapai efisiensi <i>Hyperscale</i>.
            </div>
            """, unsafe_allow_html=True)
        except: pass

# ==============================================================================
# TAB 2: POSISI PASAR (SCATTER)
# ==============================================================================
with tab2:
    st.subheader("Supply vs. Demand Matrix")
    st.caption("Peta posisi pasar berdasarkan Permintaan Digital (Internet %) dan Ketersediaan Infrastruktur (Power MW).")
    
    avg_net = df['internet_pen'].median()
    avg_power = df['power_mw'].median()

    def get_color(c):
        if c == 'Indonesia': return 'Indonesia (Focus)'
        if c == 'Singapore': return 'Singapore (Benchmark)'
        return 'Global Peers'
    
    df_filtered['Category'] = df_filtered['country'].apply(get_color)

    fig_quad = px.scatter(
        df_filtered,
        x='internet_pen', y='power_mw',
        color='Category', size='growth_rate', text='country',
        hover_data=['dc_count'],
        color_discrete_map={
            'Indonesia (Focus)': '#D50000', 
            'Singapore (Benchmark)': '#2962FF', 
            'Global Peers': '#B0BEC5'
        },
        log_y=True, size_max=60,
        title="Market Maturity Quadrant"
    )

    fig_quad.add_hline(y=avg_power, line_dash="dot", line_color="gray", annotation_text="Global Avg Power")
    fig_quad.add_vline(x=avg_net, line_dash="dot", line_color="gray", annotation_text="Global Avg Internet")
    fig_quad.update_traces(textposition='top center')
    
    st.plotly_chart(apply_pro_theme(fig_quad), use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <b>📍 Market Positioning:</b><br>
        Indonesia teridentifikasi berada di kuadran <span class="alert">Opportunity Gap</span> (Kanan Bawah).
        <br><br>
        <b>Implikasi:</b> Tingkat adopsi digital (Internet Penetration) sudah setara negara maju, namun infrastruktur penunjang (Power) masih <i>Underserved</i>. 
        Ukuran lingkaran merah yang besar menunjukkan Indonesia memiliki <b>Laju Pertumbuhan (Growth Rate)</b> tertinggi untuk menutup celah ini.
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 3: RADAR CHART
# ==============================================================================
with tab3:
    st.subheader("Competitive Landscape Analysis")
    st.caption("Perbandingan multidimensi: Kesehatan Ekosistem dan Potensi Pertumbuhan.")
    
    target_countries = st.multiselect("Pilih Negara untuk Head-to-Head:", df_filtered['country'].unique(), default=['Indonesia', 'Singapore'])
    
    if len(target_countries) > 0:
        df_radar = df[df['country'].isin(target_countries)].copy()
        categories = ['power_mw', 'growth_rate', 'quality_score', 'internet_pen', 'renewable_pct']
        labels = ['Power Capacity', 'Annual Growth', 'Infra Quality (Tier III+)', 'Digital Adoption', 'Green Energy']
        
        fig_radar = go.Figure()

        for country in target_countries:
            row = df_radar[df_radar['country'] == country].iloc[0]
            values = []
            for col in categories:
                max_val = df[col].max()
                val = row[col] / max_val if max_val > 0 else 0
                values.append(val)
            values.append(values[0]) 
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values, theta=labels + [labels[0]],
                fill='toself', name=country
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], gridcolor='rgba(128,128,128,0.2)'),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=True, height=500,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# ==============================================================================
# TAB 4: SUSTAINABILITY
# ==============================================================================
with tab4:
    st.subheader("Green Energy Transition (SDG 13)")
    st.caption("Peringkat negara berdasarkan persentase penggunaan energi terbarukan pada fasilitas Data Center.")
    
    df_green = df_filtered.sort_values('renewable_pct', ascending=True)
    
    fig_green = go.Figure()
    
    # Garis Lollipop
    for i, row in df_green.iterrows():
        fig_green.add_shape(
            type='line', x0=0, y0=row['country'], x1=row['renewable_pct'], y1=row['country'],
            line=dict(color='gray', width=1)
        )
        
    # Titik Marker
    fig_green.add_trace(go.Scatter(
        x=df_green['renewable_pct'], y=df_green['country'],
        mode='markers+text',
        text=df_green['renewable_pct'].apply(lambda x: f"{x:.0f}%"),
        textposition="middle right", 
        marker=dict(
            color=df_green['renewable_pct'],
            colorscale='RdYlGn', size=16, showscale=True,
            colorbar=dict(title="% Renewable")
        )
    ))
    
    fig_green.update_layout(
        title="Renewable Energy Adoption Rate",
        xaxis_title="Renewable Energy Share (%)",
        xaxis=dict(range=[0, 115]),
        showlegend=False
    )
    st.plotly_chart(apply_pro_theme(fig_green), use_container_width=True)
    
    try:
        indo_green = df[df['country']=='Indonesia']['renewable_pct'].values[0]
        st.markdown(f"""
        <div class="insight-box" style="border-left: 5px solid #66BB6A;">
            🌱 <b>Sustainability Status:</b><br>
            Indonesia baru mencapai adopsi energi terbarukan sebesar <b>{indo_green:.1f}%</b>. 
            Ini adalah tantangan kritis mengingat investor global (Google/Microsoft/AWS) memiliki target <i>Net-Zero</i> yang ketat.
            Akses ke energi hijau akan menjadi faktor penentu daya saing di masa depan.
        </div>
        """, unsafe_allow_html=True)
    except: pass

# --- FOOTER ---
st.markdown("""
<div class='footer'>
    Data Center Intelligence Unit • Data Source: Internal Research Database (2025) • Processed with Python & Streamlit
</div>
""", unsafe_allow_html=True)