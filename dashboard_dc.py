import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# --- 1. CONFIG & STYLE ---
st.set_page_config(
    page_title="Indonesia DC Tracker + AI",
    page_icon="🇮🇩",
    layout="wide"
)

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
    
    /* Highlight Box */
    .insight-box {
        background-color: var(--secondary-background-color);
        border-left: 4px solid #2962FF;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .footer { text-align: center; color: gray; font-size: 12px; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS (CLEANING & VISUAL) ---

def apply_pro_theme(fig):
    """Menerapkan tema profesional yang bersih dan transparan"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(128,128,128,0.1)'),
    )
    return fig

def clean_numeric(value):
    if pd.isna(value): return 0
    value = str(value).lower().replace(',', '')
    if '-' in value:
        parts = re.findall(r"[\d\.]+", value)
        if len(parts) >= 2: return (float(parts[0]) + float(parts[1])) / 2
    matches = re.findall(r"[\d\.]+", value)
    return float(matches[0]) if matches else 0

def clean_tier_score(value):
    if pd.isna(value): return 0
    val_str = str(value)
    match3 = re.search(r'III[:\s]*(\d+)%', val_str)
    tier3 = float(match3.group(1)) if match3 else 0
    match4 = re.search(r'IV[:\s]*(\d+)%', val_str)
    tier4 = float(match4.group(1)) if match4 else 0
    return tier3 + tier4

# --- 3. LOAD DATA & ML PROCESS ---
@st.cache_data
def load_data_with_ml():
    try:
        df = pd.read_csv('Book1 (1).csv')
        
        # Cleaning Standard
        df['dc_count'] = df['total_data_centers'].apply(clean_numeric)
        df['power_mw'] = df['power_capacity_MW_total'].apply(clean_numeric)
        df['internet_pen'] = df['internet_penetration_percent'].apply(clean_numeric)
        df['renewable_pct'] = df['average_renewable_energy_usage_percent'].apply(clean_numeric)
        df['growth_rate'] = df['growth_rate_of_data_centers_percent_per_year'].apply(clean_numeric)
        df['quality_score'] = df['tier_distribution'].apply(clean_tier_score)
        
        # Normalisasi Persen
        for col in ['internet_pen', 'renewable_pct']:
            df[col] = df[col].apply(lambda x: x*100 if x <= 1 and x > 0 else x)
            df[col] = df[col].apply(lambda x: 100 if x > 100 else x)

        # Filter Data Layak untuk ML (Hapus data kosong/nol)
        df_ml = df[(df['power_mw'] > 0) & (df['internet_pen'] > 0)].copy()
        
        # --- MACHINE LEARNING: K-MEANS CLUSTERING ---
        features = ['dc_count', 'power_mw', 'internet_pen', 'growth_rate', 'renewable_pct']
        X = df_ml[features].fillna(0)
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=4, random_state=42)
        df_ml['Cluster'] = kmeans.fit_predict(X_scaled)
        
        # Mapping label cluster berdasarkan Power Capacity rata-rata
        cluster_profile = df_ml.groupby('Cluster')['power_mw'].mean().sort_values(ascending=False)
        sorted_clusters = cluster_profile.index.tolist()
        
        mapping = {
            sorted_clusters[0]: 'Top Tier (Global Hub)',
            sorted_clusters[1]: 'Mature Market',
            sorted_clusters[2]: 'High Growth / Emerging',
            sorted_clusters[3]: 'Early Stage'
        }
        
        df_ml['Cluster Label'] = df_ml['Cluster'].map(mapping)
        
        return df_ml
    except Exception as e:
        st.error(f"System Error: {e}")
        return pd.DataFrame()

df = load_data_with_ml()
if df.empty: st.stop()

# --- 4. SIDEBAR ---
st.sidebar.header("🎛️ Kontrol Dashboard")
country_list = df['country'].unique().tolist()
defaults = ['Indonesia', 'Singapore', 'Malaysia', 'United States', 'China']
valid_defaults = [c for c in defaults if c in country_list]
selected_countries = st.sidebar.multiselect("Negara Pembanding:", country_list, default=valid_defaults)
df_filtered = df[df['country'].isin(selected_countries)].copy()

# --- 5. DASHBOARD LAYOUT ---
st.title("🇮🇩 AI-Powered Data Center Tracker")
st.markdown("Benchmarking Infrastruktur Digital menggunakan **Machine Learning K-Means Clustering**.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Scale", "🎯 Position", "🛡️ Quality", "🌱 Green", "🤖 AI Clustering (Baru)"
])

# === TAB 1: SCALE ===
with tab1:
    st.subheader("Infrastructure Gap Analysis")
    df_melt = df_filtered.melt(id_vars='country', value_vars=['dc_count', 'power_mw'], var_name='Metrik', value_name='Nilai')
    fig_bar = px.bar(df_melt, x='country', y='Nilai', color='Metrik', barmode='group', log_y=True, text_auto='.2s', title="Scale Comparison (Log Scale)")
    st.plotly_chart(apply_pro_theme(fig_bar), use_container_width=True)

# === TAB 2: POSITION ===
with tab2:
    st.subheader("Market Quadrant")
    avg_power = df['power_mw'].median()
    avg_net = df['internet_pen'].median()
    fig_quad = px.scatter(df_filtered, x='internet_pen', y='power_mw', size='growth_rate', color='country', log_y=True, title="Demand vs Supply")
    fig_quad.add_hline(y=avg_power, line_dash="dot", annotation_text="Global Avg Power")
    fig_quad.add_vline(x=avg_net, line_dash="dot", annotation_text="Global Avg Internet")
    st.plotly_chart(apply_pro_theme(fig_quad), use_container_width=True)

# === TAB 3: QUALITY ===
with tab3:
    st.subheader("Head-to-Head Radar")
    if len(selected_countries) > 0:
        fig_radar = go.Figure()
        categories = ['power_mw', 'growth_rate', 'quality_score', 'internet_pen', 'renewable_pct']
        for c in selected_countries:
            row = df[df['country'] == c].iloc[0]
            vals = [row[col]/df[col].max() for col in categories]
            fig_radar.add_trace(go.Scatterpolar(r=vals + [vals[0]], theta=categories + [categories[0]], fill='toself', name=c))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])))
        st.plotly_chart(apply_pro_theme(fig_radar), use_container_width=True)

# === TAB 4: GREEN ===
with tab4:
    st.subheader("Sustainability Ranking")
    df_green = df_filtered.sort_values('renewable_pct')
    fig_green = px.scatter(df_green, x='renewable_pct', y='country', color='renewable_pct', 
                           color_continuous_scale='RdYlGn', size_max=15, title="Renewable Energy Adoption (%)")
    fig_green.update_traces(marker=dict(size=15))
    st.plotly_chart(apply_pro_theme(fig_green), use_container_width=True)

# === TAB 5: AI CLUSTERING ===
with tab5:
    st.subheader("🤖 Segmentasi Negara dengan Unsupervised Learning (K-Means)")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Scatter Plot Clustering Global
        fig_cluster = px.scatter(
            df,
            x="internet_pen",
            y="power_mw",
            color="Cluster Label", # Hasil ML
            size="dc_count",
            hover_name="country",
            log_y=True,
            title="Peta Segmentasi Global (Hasil Clustering)",
            color_discrete_map={
                'Top Tier (Global Hub)': '#D32F2F', # Merah Tua
                'Mature Market': '#1976D2',         # Biru
                'High Growth / Emerging': '#388E3C',# Hijau
                'Early Stage': '#757575'            # Abu-abu
            }
        )
        st.plotly_chart(apply_pro_theme(fig_cluster), use_container_width=True)
    
    with col2:
        # Cek Posisi Indonesia
        try:
            indo_cluster = df[df['country']=='Indonesia']['Cluster Label'].values[0]
            st.markdown(f"""
            <div class="insight-box" style="border-left: 5px solid #FF9800;">
                <b>🔍 Hasil Diagnosa AI:</b><br>
                Indonesia diklasifikasikan ke dalam kelompok:<br>
                <h3 style="margin:5px 0; color:#E65100;">{indo_cluster}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.caption("Negara lain di cluster yang sama:")
            peers = df[df['Cluster Label'] == indo_cluster]['country'].tolist()
            st.write(", ".join(peers[:10]) + "...")
        except:
            st.error("Data Indonesia tidak ditemukan.")

# Footer
st.markdown("---")
st.caption("Powered by Python Scikit-Learn & Streamlit")
