import streamlit as st, pandas as pd, asyncio, json
from datascout.engine import search_all
from datascout.history_manager import save_search, get_history
from datascout.download_manager import safe_download

st.set_page_config(page_title="DataScout AI", layout="wide", page_icon="🔍")
st.title("🔍 DataScout AI — Intelligent Dataset Discovery Agent")

with st.sidebar:
    st.header("Settings")
    st.caption("Supported: HF • OpenML • Zenodo • GitHub • WorldBank • Kaggle*")
    st.info("*Kaggle needs KAGGLE_USERNAME/KEY in .env")
    sort=st.selectbox("Sort by", ["relevance","newest","largest","source"])
    fmt_filter=st.multiselect("Format", ["csv","json","parquet","images","text"])
    if st.button("View History"):
        st.write(get_history())

query=st.text_input("Describe dataset you need:", placeholder="Find medical image datasets for pneumonia detection in CSV format...")
col1,col2=st.columns([1,5])
search_btn=col1.button("Search", type="primary")
export_btn=col2.button("Export last results")

if "results" not in st.session_state: st.session_state.results=[]

if search_btn and query:
    with st.spinner("Searching 6 sources concurrently..."):
        data=asyncio.run(search_all(query))
        st.session_state.results=data["results"]
        st.session_state.statuses=data["statuses"]
        save_search(query, [r.model_dump() for r in data["results"]])
    st.success(f"Found {len(st.session_state.results)} datasets")
    st.json(st.session_state.statuses)

if st.session_state.results:
    # filters
    filtered=st.session_state.results
    if fmt_filter:
        filtered=[r for r in filtered if any(f.lower() in [x.lower() for x in r.formats] for f in fmt_filter)]
    # sorting
    if sort=="newest": filtered.sort(key=lambda x: x.last_updated or x.title, reverse=True)
    elif sort=="largest": filtered.sort(key=lambda x: x.size_bytes or 0, reverse=True)
    elif sort=="relevance": filtered.sort(key=lambda x: x.relevance_score, reverse=True)

    for r in filtered[:20]:
        with st.container(border=True):
            c1,c2=st.columns([3,1])
            with c1:
                st.subheader(r.title)
                st.caption(f"{r.source} • {r.license} • {r.access_type.value} • Score {r.relevance_score} — {r.relevance_explanation}")
                st.write(r.description[:400])
                st.write(f"**Formats:** {', '.join(r.formats) or 'Unknown'} | **URL:** {r.dataset_url}")
                if r.download_url: st.code(r.download_url)
            with c2:
                st.link_button("Open Dataset Page", r.dataset_url)
                if r.download_url:
                    if st.button(f"Download {r.id}", key=r.id):
                        try:
                            path=asyncio.run(safe_download(r.download_url, "./downloads"))
                            st.success(f"Saved to {path}")
                            if path.endswith(".csv"):
                                df=pd.read_csv(path, nrows=5)
                                st.dataframe(df)
                        except Exception as e:
                            st.error(f"Download blocked: {e}")
                            st.info("Authentication required or host not allowlisted. Open dataset page.")
                else:
                    st.caption("No direct download — see landing page")

    if export_btn:
        df=pd.DataFrame([r.model_dump() for r in filtered])
        st.download_button("Download CSV", df.to_csv(index=False), "datascout_results.csv")
        st.download_button(
            "Download JSON",
            json.dumps([r.model_dump(mode="json") for r in filtered], indent=2),
            "datascout_results.json",
        )