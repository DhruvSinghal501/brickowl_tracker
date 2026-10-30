import json
import os
import streamlit as st

st.set_page_config(
    page_title="LEGO Star Wars Collector Assistant", layout="wide"
)

st.title("🛸 LEGO Star Wars BrickOwl Collector Dashboard")
st.write(
    "Talk to your assistant, view images, and filter for Clone Wars or priority"
    " sets."
)

JSON_FILE = "brickowl_starwars_tracker.json"


@st.cache_data(ttl=60)
def load_data():
  if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r", encoding="utf-8") as f:
      return json.load(f).get("items", {})
  return {}


items_db = load_data()

# Sidebar Controls
st.sidebar.header("🔍 Collector Controls")
filter_theme = st.sidebar.selectbox(
    "Sub-Theme Filter", ["All Star Wars", "Clone Wars Only"]
)
max_price_filter = st.sidebar.slider("Max Price ($)", 10.0, 300.0, 300.0)

# Natural Language / Conversational Filter Box
st.subheader("💬 Ask Gemini Assistant")
user_prompt = st.text_input(
    "Describe what you're looking for (e.g., 'Show me Clone Trooper sets',"
    " 'Gunship')",
    "",
)

# Filtering logic
filtered_items = []
for item in items_db.values():
  name = item.get("name", "")
  tags = item.get("tags", [])

  # Auto-tag Clone Wars if missing in old json entries
  if (
      "clone" in name.lower()
      or "501st" in name.lower()
      or "gunship" in name.lower()
      or "at-te" in name.lower()
  ):
    if "Clone Wars" not in tags:
      tags.append("Clone Wars")

  # Theme Filter
  if filter_theme == "Clone Wars Only" and "Clone Wars" not in tags:
    continue

  # Conversational Prompt Matching
  if user_prompt and user_prompt.lower() not in name.lower():
    if "clone" in user_prompt.lower() and "clone" not in name.lower():
      continue

  filtered_items.append(item)

st.write(f"Showing **{len(filtered_items)}** matched sets:")

# Grid Display with Safe Key Access & Fallbacks
cols = st.columns(3)
for idx, item in enumerate(filtered_items):
  with cols[idx % 3]:
    img_url = item.get("image_url", "")

    # Display image safely
    if img_url and img_url.startswith("http"):
      try:
        st.image(img_url, width=180, caption=item.get("name"))
      except Exception:
        st.info("🖼️ [Image preview unavailable]")
    else:
      st.info("🖼️ [Image preview unavailable]")

    st.markdown(f"**[{item.get('name')}]({item.get('url', '#')})**")
    st.caption(f"Condition: {item.get('condition', 'New / Sealed')}")

    # Top 3 Competitive Sellers Table with .get() fallbacks
    st.markdown("**Top 3 Competitive Sellers:**")
    sellers = item.get("top_3_sellers", [])
    if sellers:
      for s in sellers:
        rank = s.get("seller_rank", 1)
        price = s.get("price", "N/A")
        store = s.get("store_name", "BrickOwl Verified Store")
        st.write(f"• Rank {rank}: **${price}** ({store})")
    else:
      st.write("• Rank 1: **Best Retail Listing** (BrickOwl Verified Store)")

    st.divider()