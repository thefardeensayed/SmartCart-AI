# 🛍️ SmartCart AI: E-Commerce Product Bundle & Propensity Modeler

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/AI-Random%20Forest-F7931E.svg)](https://scikit-learn.org/)
[![Course](https://img.shields.io/badge/Syllabus-BAINB501%20(CO2%20%26%20CO3)-green.svg)](#)

**SmartCart AI** is a hybrid **Bayesian Probabilistic Reasoning + Machine Learning** application designed for multi-store electronics retail networks (modeled across **30 Bengaluru retail branches** and **52 products**). Aligned with **BAINB501 (Artificial Intelligence Concepts and Practice — Module 2 & Module 3)**, it combines **Exact Bayesian Inference & Forward-Chaining Rules** with a **Supervised Random Forest Classifier** to recommend relevant product bundles and dynamically trigger personalized discounts based on real-time customer purchase propensity.

---

## 🎯 Key Features

1. **Interactive Customer E-Commerce Storefront:**
   - Browse, search, and filter **52 electronics products across 8 categories** (Laptops, Smartphones, Audio, Wearables, Cameras, Gaming Consoles, Smart Home, Networking & Storage).
   - **Smart "Frequently Bought Together" Pop-Up Modal:** Dynamically suggests high-lift accessory bundles with 1-click **"Add Full Combo to Cart"** functionality.
   - **Forward-Chaining Domain Filtering (`is_anchor`):** Enforces catalog hierarchy rules so primary devices recommend accessories and accessories only recommend complementary accessories—never up-selling expensive main devices onto small accessory orders.

2. **Evaluator's Live Backend Logic Inspector (X-Ray Mode):**
   - **Module 3 Bayesian Inference Trace:** Displays real-time **Prior $P(B)$**, **Likelihood $P(A \mid B)$**, **Exact Posterior $P(B \mid A)$**, **Bayesian Lift**, and composite **Bundle Score (0–100)** formulas for every item added to the cart.
   - **Predictive AI Propensity Trace:** Feeds live session context (`Cart_Value`, `Items_In_Cart`, `Discount_Pct`, `Is_Festival_Season`, `Past_Orders`, `Time_On_Site_Mins`) into a serialized **100-tree Random Forest Classifier** (`models/random_forest_bundle.pkl`), displaying live **YES vs. NO tree voting**.
   - **Synced Evaluator Context Controls:** Adjust customer and store scenarios in real time using synchronized sliders, numeric typeboxes, and seasonal toggles.

3. **Bengaluru Retail Analytics & Model Benchmarks:**
   - Interactive Plotly visualizations for category sales, festival season spikes (Dasara/Diwali), and Bengaluru locality revenue (Indiranagar, Koramangala, Whitefield, Electronic City, SP Road, etc.).
   - Benchmark comparison table pitting **Random Forest (100 trees)** against a **Logistic Regression** baseline alongside Confusion Matrix and Gini Feature Importance charts.

---

## 🏗️ Project Architecture

```text
SmartCartAI/
├── data/                                    # Generated retail datasets (CSV)
│   ├── bengaluru_electronics_stores.csv     # 30 Bengaluru retail store locations
│   ├── customer_sessions.csv                # 25,000 customer behavioral sessions
│   └── transactions.csv                     # ~70,000+ line-item product transactions
├── models/                                  # Serialized ML artifacts
│   └── random_forest_bundle.pkl             # Trained 100-tree Random Forest classifier
├── src/                                     # Core modular source code
│   ├── catalog.py                           # 52-product catalog with is_anchor hierarchy
│   ├── data_generator.py                    # Bengaluru retail & seasonal data pipeline
│   ├── analytics.py                         # Bayesian Inference, Forward-Chaining & EDA engine
│   └── ml_engine.py                         # Random Forest vs. Logistic Regression pipeline
├── train_model.py                           # Standalone offline model training & benchmark CLI
├── app.py                                   # Main Streamlit split-screen storefront & X-ray app
├── Requirements.txt                         # Python package dependencies
├── .gitignore                               # Git ignore rules
└── README.md                                # Project documentation
```

---

## 🚀 Quickstart Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/thefardeensayed/SmartCart-AI.git
cd SmartCart-AI
```

### 2. Create & Activate a Virtual Environment (Recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
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

## 🧠 How the Hybrid AI Pipeline Works

1. **Step 1 — Bayesian Inference & Forward-Chaining Rules (Module 2 & 3 / CO2 & CO3):**  
   Using 25,000 historical orders, the engine builds Conditional Probability Tables (CPTs) and computes exact posterior probabilities via **Bayes' Theorem**:
   $$P(B \mid A) = \frac{P(A \mid B) \cdot P(B)}{P(A)}$$
   Forward-chaining domain rules prune anchor devices (`is_anchor == True`) from consequent recommendations, and pairs are ranked using **Bayesian Lift** $\left(\frac{P(B \mid A)}{P(B)}\right)$ and a weighted composite **Bundle Score (0–100)**.
2. **Step 2 — Propensity Scoring (Supervised Ensemble Learning):**  
   A **Random Forest Classifier** (`n_estimators=100`, `max_depth=8`) predicts the probability $P(\text{Bundle\_Accepted} = 1 \mid X)$. If propensity $\ge 50\%$, a **15% VIP Combo Discount** is unlocked; otherwise, a **10% Standard Combo Discount** is offered.

---

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Data Manipulation:** Pandas, NumPy
* **Probabilistic & Rule Engine:** Exact Bayesian Inference, Forward-Chaining Domain Filtering
* **Machine Learning:** Scikit-Learn (Random Forest, Logistic Regression), Joblib
* **Frontend & Visualization:** Streamlit, Plotly Express
