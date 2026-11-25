# 🛍️ SmartCart AI: E-Commerce Product Bundle & Propensity Modeler

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/AI-Random%20Forest-F7931E.svg)](https://scikit-learn.org/)
[![MLxtend](https://img.shields.io/badge/Analytics-Apriori%20Mining-green.svg)](http://rasbt.github.io/mlxtend/)

**SmartCart AI** is a hybrid **Data Analytics + Artificial Intelligence** application designed for multi-store electronics retail networks (modeled across **30 Bengaluru retail branches** and **52 products**). It combines **Unsupervised Association Rule Mining (Apriori)** with a **Supervised Ensemble Classifier (Random Forest)** to recommend relevant product bundles and dynamically trigger personalized discounts based on real-time customer purchase propensity.

---

## 🎯 Key Features

1. **Interactive Customer E-Commerce Storefront:**
   - Browse, search, and filter **52 electronics products across 8 categories** (Laptops, Smartphones, Audio, Wearables, Cameras, Gaming Consoles, Smart Home, Networking & Storage).
   - **Smart "Frequently Bought Together" Pop-Up Modal:** Dynamically suggests high-lift accessory bundles with 1-click **"Add Full Combo to Cart"** functionality.
   - **Catalog Hierarchy Domain Filtering (`is_anchor`):** Ensures primary devices recommend accessories and accessories only recommend complementary accessories—never up-selling expensive main devices onto small accessory orders.

2. **Evaluator's Live Backend Logic Inspector (X-Ray Mode):**
   - **Data Analytics Trace:** Displays real-time **Support**, **Confidence**, **Lift**, and composite **Bundle Score (0–100)** formulas for every item added to the cart.
   - **AI Propensity Trace:** Feeds live session context (`Cart_Value`, `Items_In_Cart`, `Discount_Pct`, `Is_Festival_Season`, `Past_Orders`, `Time_On_Site_Mins`) into a serialized **100-tree Random Forest Classifier** (`models/random_forest_bundle.pkl`), displaying live **YES vs. NO tree voting**.
   - **Synced Evaluator Context Controls:** Adjust customer and store scenarios in real time using synchronized sliders, numeric typeboxes, and seasonal toggles.

3. **Bengaluru Retail Analytics & Model Benchmarks:**
   - Interactive Plotly visualizations for category sales, festival season spikes (Dasara/Diwali), and Bengaluru locality revenue (Indiranagar, Koramangala, Whitefield, Electronic City, SP Road, etc.).
   - Benchmark comparison table pitting **Random Forest (100 trees)** against a **Logistic Regression** baseline alongside Confusion Matrix and Gini Feature Importance charts.

---

## 🏗️ Project Architecture

```text
smart_bundle_ai/
├── data/                                    # Generated retail datasets (CSV)
│   ├── bengaluru_electronics_stores.csv     # 30 Bengaluru retail store locations
│   ├── customer_sessions.csv                # 25,000 customer behavioral sessions
│   └── transactions.csv                     # ~70,000+ line-item product transactions
├── models/                                  # Serialized ML artifacts
│   └── random_forest_bundle.pkl             # Trained 100-tree Random Forest classifier
├── src/                                     # Core modular source code
│   ├── catalog.py                           # 52-product catalog with is_anchor hierarchy
│   ├── data_generator.py                    # Bengaluru retail & seasonal data pipeline
│   ├── analytics.py                         # Apriori Market Basket Analysis & EDA engine
│   └── ml_engine.py                         # Random Forest vs. Logistic Regression pipeline
├── train_model.py                           # Standalone offline model training & benchmark CLI
├── app.py                                   # Main Streamlit split-screen storefront & X-ray app
├── Requirements.txt                         # Python package dependencies
└── README.md                                # Project documentation
```

---

## 🚀 Quickstart Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/smart-bundle-ai.git
cd smart-bundle-ai
```

### 2. Create & Activate a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r Requirements.txt
```

### 4. Generate Data & Train the AI Model
Run the training script to generate the 25,000 Bengaluru customer sessions, evaluate model metrics, and save `models/random_forest_bundle.pkl`:
```bash
python train_model.py
```

### 5. Launch the Web Application
```bash
streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.

---

## 🧠 How the Hybrid Pipeline Works

1. **Step 1 — Market Basket Analysis (Unsupervised):**  
   Transactions are one-hot encoded into a boolean basket matrix. The **Apriori algorithm** extracts frequent itemsets (`min_support=0.015`, `min_lift=1.1`) and scores rules using a weighted composite **Bundle Score**.
2. **Step 2 — Propensity Scoring (Supervised):**  
   A **Random Forest Classifier** (`n_estimators=100`, `max_depth=8`) predicts the probability $P(\text{Bundle\_Accepted} = 1 \mid X)$. If propensity $\ge 50\%$, a **15% VIP Combo Discount** is unlocked; otherwise, a **10% Standard Combo Discount** is offered.

---

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Data Manipulation:** Pandas, NumPy
* **Data Analytics:** MLxtend (Apriori & Association Rules)
* **Machine Learning:** Scikit-Learn (Random Forest, Logistic Regression), Joblib
* **Frontend & Visualization:** Streamlit, Plotly Express
