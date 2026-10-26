"""Interactive Streamlit dashboard: Wisconsin Diagnostic Breast Cancer data."""
from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from analysis import DISPLAY_FEATURES, get_data, grouped_feature_stats, summary

st.set_page_config(page_title="CellScope | Breast Cancer Data Explorer", page_icon="🔬", layout="wide")

st.markdown("""<style>
.block-container {padding-top: 2rem; padding-bottom: 2.5rem;}
h1 {letter-spacing: -0.04em;}
[data-testid="stMetric"] {background: #F7F9FC; border: 1px solid #E5EAF1; border-radius: 12px; padding: 1.1rem;}
small, .stCaption {color:#67748B;}
</style>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return get_data()

df = load_data()

st.caption("CELLSCOPE  /  DATA EXPLORER  /  WDBC")
st.title("Breast Cancer Data Explorer")
st.write("Explore patterns in **569 diagnostic cell-image samples** using transparent, reproducible statistics.")
st.info("Educational analysis only. This dashboard does not diagnose disease or estimate personal cancer risk.", icon="ℹ️")

with st.sidebar:
    st.header("Filters")
    diagnosis_selection = st.multiselect("Diagnosis", ["Benign", "Malignant"], default=["Benign", "Malignant"])
    feature = st.selectbox("Analyze a measurement", list(DISPLAY_FEATURES.keys()),
                           format_func=lambda x: DISPLAY_FEATURES[x])
    st.caption("Source: UCI Wisconsin Diagnostic Breast Cancer dataset, via scikit-learn.")
    st.caption("Sample labels indicate diagnoses from the original dataset, not predictions.")

filtered = df[df["diagnosis"].isin(diagnosis_selection)].copy()
metrics = summary(filtered)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Samples shown", f"{metrics['total']:,}")
c2.metric("Benign", f"{metrics['benign']:,}")
c3.metric("Malignant", f"{metrics['malignant']:,}")
c4.metric("Malignant in selection", f"{metrics['malignant_pct']:.1f}%")

if filtered.empty:
    st.warning("Select at least one diagnosis in the sidebar.")
    st.stop()

palette = {"Benign":"#17A398", "Malignant":"#DB697B"}
left, right = st.columns([1, 1.25], gap="large")
with left:
    st.subheader("Diagnostic label distribution")
    counts = filtered["diagnosis"].value_counts().reindex(["Benign","Malignant"]).dropna()
    chart = go.Figure(go.Pie(labels=counts.index,values=counts.values,hole=.68,
                              marker_colors=[palette[x] for x in counts.index],
                              sort=False,textinfo="percent"))
    chart.update_layout(height=325,margin=dict(l=10,r=10,t=10,b=10),
                        legend=dict(orientation="h",x=0,y=-.08),
                        annotations=[dict(text=str(len(filtered)),font_size=34,showarrow=False)])
    st.plotly_chart(chart, use_container_width=True)
with right:
    st.subheader(f"{DISPLAY_FEATURES[feature]} by diagnosis")
    fig = px.box(filtered,x="diagnosis",y=feature,color="diagnosis",points="outliers",
                 color_discrete_map=palette,category_orders={"diagnosis":["Benign","Malignant"]})
    fig.update_layout(height=325,showlegend=False,margin=dict(l=10,r=10,t=12,b=12),
                      xaxis_title="Diagnostic label",yaxis_title=DISPLAY_FEATURES[feature],
                      plot_bgcolor="white")
    st.plotly_chart(fig,use_container_width=True)

st.subheader("Feature relationships")
scatter = px.scatter(filtered, x="mean radius", y="mean texture", color="diagnosis",
                     opacity=.68, color_discrete_map=palette,
                     hover_data=["sample_id","mean area","mean concavity"])
scatter.update_layout(height=380,plot_bgcolor="white",margin=dict(l=10,r=10,t=10,b=10),
                      xaxis_title="Mean radius",yaxis_title="Mean texture",
                      legend_title_text="Diagnosis")
st.plotly_chart(scatter,use_container_width=True)

st.subheader("Summary statistics")
st.dataframe(grouped_feature_stats(filtered, feature), hide_index=True, use_container_width=True)

with st.expander("Inspect and download the filtered dataset"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.download_button("Download filtered CSV", data=filtered.to_csv(index=False).encode("utf-8"),
                       file_name="cellscope_filtered_data.csv", mime="text/csv")

st.divider()
st.caption("Dataset: UCI Machine Learning Repository — Breast Cancer Wisconsin (Diagnostic). Features extracted from digitized fine-needle aspirate images. 569 specimens, 30 numeric measurements. No time variable, no personal identifiers in this analysis. The proportions reflect this dataset only, not general population cancer rates.")
