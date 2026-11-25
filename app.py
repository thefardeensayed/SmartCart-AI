import os
import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

from src.catalog import CATALOG, get_all_categories
from src.data_generator import generate_ecommerce_data
from src.analytics import run_bayesian_inference_engine, get_eda_summaries
from src.ml_engine import train_and_evaluate_models, FEATURE_COLS

st.set_page_config(page_title="SmartCart AI — Bengaluru Electronics Storefront", layout="wide")

# --- LOAD DATA & TRAINED MODEL (CACHED FOR SPEED) ---
@st.cache_data
def load_datasets():
    if not os.path.exists("data/transactions.csv"):
        generate_ecommerce_data(num_records=25000)
    tx_df = pd.read_csv("data/transactions.csv")
    sess_df = pd.read_csv("data/customer_sessions.csv")
    stores_df = pd.read_csv("data/bengaluru_electronics_stores.csv")
    bayes_rules = run_bayesian_inference_engine(tx_df, min_prior=0.015, min_lift=1.1)
    eda = get_eda_summaries(tx_df, sess_df)
    return tx_df, sess_df, stores_df, bayes_rules, eda

@st.cache_resource
def load_ai_artifacts(sess_df):
    _, metrics_df, importance_df, cm = train_and_evaluate_models(
        sess_df, save_model=not os.path.exists("models/random_forest_bundle.pkl")
    )
    rf_model = joblib.load("models/random_forest_bundle.pkl")
    return rf_model, metrics_df, importance_df, cm

transactions_df, sessions_df, stores_df, rules_df, eda_data = load_datasets()
rf_model, metrics_df, importance_df, cm = load_ai_artifacts(sessions_df)

# --- INITIALIZE SESSION STATE ---
if "cart" not in st.session_state:
    st.session_state.cart = []
if "last_added" not in st.session_state:
    st.session_state.last_added = None
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

# Initialize ECC Synced Control States
if "ecc_discount" not in st.session_state:
    st.session_state.ecc_discount = 15
if "ecc_past_orders" not in st.session_state:
    st.session_state.ecc_past_orders = 6
if "ecc_time_site" not in st.session_state:
    st.session_state.ecc_time_site = 10.0

def sync_discount_from_slider():
    st.session_state.ecc_discount = st.session_state.discount_slider

def sync_discount_from_input():
    st.session_state.ecc_discount = st.session_state.discount_input

def sync_orders_from_slider():
    st.session_state.ecc_past_orders = st.session_state.orders_slider

def sync_orders_from_input():
    st.session_state.ecc_past_orders = st.session_state.orders_input

def sync_time_from_slider():
    st.session_state.ecc_time_site = st.session_state.time_slider

def sync_time_from_input():
    st.session_state.ecc_time_site = st.session_state.time_input


# --- POP-UP DIALOG FOR "FREQUENTLY BOUGHT TOGETHER / SMART COMBO" ---
@st.dialog("🔥 Frequently Bought Together — Smart Combo!")
def show_bundle_popup(trigger_item, matching_rules, buy_prob):
    st.session_state.show_popup = False

    icon = CATALOG[trigger_item]["icon"]
    st.markdown(f"Because you added **{icon} {trigger_item}** to your cart:")

    top_recs = matching_rules.head(3)
    rec_items = [
        r for r in top_recs["Recommended_Accessory"].tolist()
        if r in CATALOG and r not in st.session_state.cart
    ]

    if not rec_items:
        st.info("You already have all top recommended accessories for this item in your cart!")
        if st.button("Close"):
            st.rerun()
        return

    combo_all = [trigger_item] + rec_items
    total_original = sum(CATALOG[i]["price"] for i in combo_all)
    discount_rate = 0.15 if buy_prob >= 50 else 0.10
    discounted_price = int(total_original * (1 - discount_rate))

    for _, row in top_recs.iterrows():
        rec_name = row["Recommended_Accessory"]
        if rec_name in rec_items:
            st.success(
                f"{CATALOG[rec_name]['icon']} **{rec_name}** — ₹{CATALOG[rec_name]['price']:,}  \n"
                f"*Posterior P(Add|Cart): {row['Posterior_Prob']*100:.0f}% "
                f"(Bayesian Lift: {row['Bayesian_Lift']:.2f}× | Bundle Score: {row['Bundle_Score']}/100)*"
            )

    st.divider()
    st.markdown(
        f"**Complete Combo Deal ({int(discount_rate*100)}% AI-Triggered Bundle Discount):** "
        f"~~₹{total_original:,}~~ $\\rightarrow$ **₹{discounted_price:,}**"
    )

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("✅ Add Full Combo to Cart", type="primary", use_container_width=True):
            for item in rec_items:
                if item not in st.session_state.cart:
                    st.session_state.cart.append(item)
            st.rerun()
    with col_b2:
        if st.button("No thanks, continue", use_container_width=True):
            st.rerun()


# --- HEADER & EVALUATOR SESSION SIMULATOR ---
st.title("🛍️ SmartCart AI: Bengaluru Electronics Storefront & Logic Inspector")
st.caption("BAINB501 Project | Bayesian Inference + Forward-Chaining Rules (CO2/CO3) & Random Forest Propensity AI")

with st.expander("⚙️ Evaluator Context Controls (Simulate Customer & Store Profile)", expanded=True):
    ec1, ec2, ec3, ec4, ec5 = st.columns([1.4, 1, 0.9, 1, 1], gap="medium")

    with ec1:
        selected_store = st.selectbox("🏪 Bengaluru Store Branch", stores_df["Store_Name"].tolist())

    with ec2:
        st.slider(
            "🏷️ Bundle Discount (%)", 0, 30,
            value=st.session_state.ecc_discount, step=1,
            key="discount_slider", on_change=sync_discount_from_slider
        )
        st.number_input(
            "Type Discount (%)", min_value=0, max_value=30,
            value=st.session_state.ecc_discount, step=1,
            key="discount_input", on_change=sync_discount_from_input,
            label_visibility="collapsed"
        )

    with ec3:
        st.markdown("**🎉 Festival Season**")
        is_festival_toggle = st.toggle("Dasara / Diwali Active", value=True)
        sim_festival = "Yes" if is_festival_toggle else "No"

    with ec4:
        st.slider(
            "📦 Customer Past Orders", 0, 20,
            value=st.session_state.ecc_past_orders, step=1,
            key="orders_slider", on_change=sync_orders_from_slider
        )
        st.number_input(
            "Type Past Orders", min_value=0, max_value=20,
            value=st.session_state.ecc_past_orders, step=1,
            key="orders_input", on_change=sync_orders_from_input,
            label_visibility="collapsed"
        )

    with ec5:
        st.slider(
            "⏱️ Time on Site (mins)", 1.0, 30.0,
            value=float(st.session_state.ecc_time_site), step=0.5,
            key="time_slider", on_change=sync_time_from_slider
        )
        st.number_input(
            "Type Time (mins)", min_value=1.0, max_value=30.0,
            value=float(st.session_state.ecc_time_site), step=0.5,
            key="time_input", on_change=sync_time_from_input,
            label_visibility="collapsed"
        )

sim_discount = st.session_state.ecc_discount
sim_past_orders = st.session_state.ecc_past_orders
sim_time_site = st.session_state.ecc_time_site

st.divider()

# ================= SPLIT SCREEN LAYOUT =================
store_col, backend_col = st.columns([1.25, 1], gap="large")

# ---------------- LEFT: CUSTOMER STOREFRONT ----------------
with store_col:
    st.subheader("🛒 Customer Storefront")

    f_col1, f_col2 = st.columns([1.5, 1])
    search_query = f_col1.text_input("🔍 Search products (e.g., Laptop, Phone, Camera, Console...)", "")
    selected_cat = f_col2.selectbox("📂 Filter by Category", ["All Categories"] + get_all_categories())

    filtered_products = {}
    for prod_name, details in CATALOG.items():
        matches_search = search_query.lower() in prod_name.lower() or search_query.lower() in details["category"].lower()
        matches_cat = (selected_cat == "All Categories") or (details["category"] == selected_cat)
        if matches_search and matches_cat:
            filtered_products[prod_name] = details

    st.caption(f"Showing **{len(filtered_products)}** of {len(CATALOG)} products")

    with st.container(height=540):
        grid_cols = st.columns(2)
        for idx, (prod_name, details) in enumerate(filtered_products.items()):
            with grid_cols[idx % 2]:
                with st.container(border=True):
                    st.markdown(f"**{details['icon']} {prod_name}**")
                    st.caption(f"{details['category']}")
                    st.markdown(f"**₹{details['price']:,}**")
                    if st.button("Add to Cart", key=f"add_{prod_name}", use_container_width=True):
                        if prod_name not in st.session_state.cart:
                            st.session_state.cart.append(prod_name)
                        st.session_state.last_added = prod_name
                        st.session_state.show_popup = True
                        st.rerun()

    st.divider()
    st.markdown(f"### 🧺 Shopping Cart ({len(st.session_state.cart)} items) — *{selected_store}*")
    if st.session_state.cart:
        cart_total = sum(CATALOG[i]["price"] for i in st.session_state.cart)
        for idx, item in enumerate(st.session_state.cart):
            c_item, c_price, c_rem = st.columns([3, 1.2, 0.8])
            c_item.write(f"{CATALOG[item]['icon']} {item}")
            c_price.write(f"₹{CATALOG[item]['price']:,}")
            if c_rem.button("❌", key=f"rem_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()
        st.markdown(f"**Total Cart Value: ₹{cart_total:,}**")
        if st.button("🗑️ Clear Entire Cart"):
            st.session_state.cart = []
            st.session_state.last_added = None
            st.session_state.show_popup = False
            st.rerun()
    else:
        st.info("Your cart is empty. Search or filter by category above and click **Add to Cart**!")

# ---------------- RIGHT: EVALUATOR BACKEND X-RAY ----------------
with backend_col:
    st.subheader("🧠 Backend Logic Inspector")

    if st.session_state.last_added:
        active_item = st.session_state.last_added
        cart_val = sum(CATALOG[i]["price"] for i in st.session_state.cart)

        # 1. BAYESIAN INFERENCE & FORWARD-CHAINING TRACE (MODULE 2 & 3)
        st.markdown("#### 1️⃣ Module 3 Engine: Bayesian Inference & Rule Filtering")
        st.caption(f"Computing exact Bayes' Theorem posterior P(Accessory | Evidence = `{active_item}`)")

        matching_rules = rules_df[rules_df["Evidence_Item"] == active_item]
        if not matching_rules.empty:
            top_rule = matching_rules.iloc[0]
            st.code(
                f"BAYESIAN INFERENCE: P({top_rule['Recommended_Accessory']} | {active_item})\n"
                f"• Prior P(B)          = {top_rule['Prior_Prob']:.4f} ({top_rule['Prior_Prob']*100:.2f}% baseline purchase rate)\n"
                f"• Likelihood P(A|B)   = {top_rule['Likelihood']:.4f}\n"
                f"• Posterior P(B|A)    = {top_rule['Posterior_Prob']:.4f} ({top_rule['Posterior_Prob']*100:.1f}% conditional probability)\n"
                f"• Bayesian Lift       = {top_rule['Bayesian_Lift']:.2f}x  (Posterior / Prior > 1.0)\n"
                f"• Forward-Chain Rule  = PASSED (Target is_anchor == False)\n"
                f"• Bundle Score        = {top_rule['Bundle_Score']} / 100",
                language="yaml"
            )
            with st.expander("View Conditional Probability Table (CPT) for this Item"):
                st.dataframe(
                    matching_rules[[
                        "Evidence_Item", "Recommended_Accessory",
                        "Prior_Prob", "Likelihood", "Posterior_Prob",
                        "Bayesian_Lift", "Bundle_Score"
                    ]],
                    use_container_width=True
                )
        else:
            st.warning(f"`{active_item}` has no downstream accessory rules at current prior thresholds.")

        # 2. RANDOM FOREST BACKEND TRACE
        st.markdown("#### 2️⃣ Predictive AI: Random Forest Propensity Model")
        st.caption("Passing live session features through 100 trained Decision Trees (`models/random_forest_bundle.pkl`):")

        input_df = pd.DataFrame([{
            "Cart_Value": cart_val,
            "Items_In_Cart": len(st.session_state.cart),
            "Discount_Pct": sim_discount,
            "Is_Festival_Season": 1 if sim_festival == "Yes" else 0,
            "Past_Orders": sim_past_orders,
            "Time_On_Site_Mins": sim_time_site
        }])[FEATURE_COLS]

        st.dataframe(input_df, use_container_width=True)

        tree_votes = [tree.predict(input_df.values)[0] for tree in rf_model.estimators_]
        yes_votes = int(sum(tree_votes))
        no_votes = len(tree_votes) - yes_votes
        buy_prob = rf_model.predict_proba(input_df)[0][1] * 100

        v1, v2, v3 = st.columns(3)
        v1.metric("Trees Voting YES", f"{yes_votes} / 100")
        v2.metric("Trees Voting NO", f"{no_votes} / 100")
        v3.metric("Buy Propensity", f"{buy_prob:.1f}%")

        if buy_prob >= 50:
            st.success(f"**AI Action:** Propensity ({buy_prob:.1f}%) ≥ 50% $\\rightarrow$ **Trigger 15% VIP Combo Pop-Up!**")
        else:
            st.info(f"**AI Action:** Propensity ({buy_prob:.1f}%) < 50% $\\rightarrow$ **Trigger Standard 10% Combo Pop-Up.**")

        if st.session_state.show_popup and not matching_rules.empty:
            show_bundle_popup(active_item, matching_rules, buy_prob)
    else:
        st.info("👈 Search and add any item on the left storefront to inspect live Bayesian Inference and Random Forest 100-tree voting here!")

# ================= BOTTOM: FULL ANALYTICS & AI BENCHMARKS =================
st.divider()
with st.expander("📊 Open Full Bengaluru Data Analytics (EDA) & AI Model Evaluation", expanded=False):
    b_tab1, b_tab2, b_tab3 = st.tabs([
        "1. Category & Seasonal Analytics",
        "2. Bengaluru Store & Locality Insights",
        "3. Random Forest AI Benchmarks"
    ])

    with b_tab1:
        c1, c2 = st.columns(2)
        c1.plotly_chart(
            px.bar(eda_data["category_summary"], x="Category", y="Units_Sold", color="Category", title="Units Sold by Electronics Category"),
            use_container_width=True
        )
        c2.plotly_chart(
            px.bar(eda_data["season_summary"], x="Season", y="Conversion_Pct", color="Season", title="Festival Season Bundle Conversion Rate (%)"),
            use_container_width=True
        )

    with b_tab2:
        st.plotly_chart(
            px.bar(eda_data["locality_summary"].head(12), x="Locality", y="Revenue", color="Bundle_Rate", title="Top 12 Bengaluru Localities by Electronics Revenue & Bundle Acceptance %"),
            use_container_width=True
        )

    with b_tab3:
        m1, m2 = st.columns(2)
        with m1:
            st.markdown("#### Model Accuracy Comparison (20% Unseen Test Set)")
            st.dataframe(metrics_df, use_container_width=True)
            st.markdown("#### Confusion Matrix (Random Forest)")
            cm_df = pd.DataFrame(cm, index=["Actual: No", "Actual: Yes"], columns=["Predicted: No", "Predicted: Yes"])
            st.dataframe(cm_df, use_container_width=True)
        with m2:
            st.markdown("#### Explainable AI: Feature Importance")
            fig_imp = px.bar(importance_df, x="Importance", y="Feature", orientation="h", title="Which Factors Drive Bundle Acceptance?")
            fig_imp.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig_imp, use_container_width=True)