import os
import sys
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.catalog import CATALOG

def run_apriori_analysis(transactions_df: pd.DataFrame, min_support: float = 0.015, min_lift: float = 1.1) -> pd.DataFrame:
    """
    Runs Apriori Market Basket Analysis and applies E-Commerce Domain Filtering:
    - Consequents (recommended add-ons) must NEVER be expensive main Anchor devices.
    - Supports both Anchor -> Accessory and Accessory -> Complementary Accessory rules.
    """
    # 1. One-Hot Encode: Rows = TransactionID, Columns = Product Item (True/False)
    basket = (
        transactions_df.groupby(['TransactionID', 'Item'])['Item']
        .count().unstack().reset_index().fillna(0)
        .set_index('TransactionID')
    )
    basket_bool = basket.astype(bool)

    # 2. Mine Frequent Itemsets
    frequent_itemsets = apriori(basket_bool, min_support=min_support, use_colnames=True)
    if frequent_itemsets.empty:
        return pd.DataFrame()

    # 3. Generate Association Rules
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)
    if rules.empty:
        return pd.DataFrame()

    # 4. Keep single-item rules
    rules = rules[
        (rules['antecedents'].apply(len) == 1) & 
        (rules['consequents'].apply(len) == 1)
    ].copy()

    rules['Antecedent'] = rules['antecedents'].apply(lambda x: list(x)[0])
    rules['Consequent'] = rules['consequents'].apply(lambda x: list(x)[0])

    # 5. BUSINESS LOGIC FILTER: Never recommend a main Anchor device as an add-on!
    def is_valid_recommendation(row):
        ant = row['Antecedent']
        con = row['Consequent']
        if ant not in CATALOG or con not in CATALOG:
            return False
        # Consequent must strictly be an accessory (is_anchor == False)
        if CATALOG[con]["is_anchor"]:
            return False
        return True

    rules = rules[rules.apply(is_valid_recommendation, axis=1)].copy()

    # 6. Compute Composite Bundle Score (0-100)
    rules['Bundle_Score'] = (
        (rules['confidence'] * 45) +
        (rules['lift'].clip(upper=10) / 10 * 40) +
        (rules['support'].clip(upper=0.10) / 0.10 * 15)
    ).round(1)

    cols = ['Antecedent', 'Consequent', 'support', 'confidence', 'lift', 'Bundle_Score']
    return rules[cols].sort_values(by=['Bundle_Score', 'confidence'], ascending=False).reset_index(drop=True)


def get_eda_summaries(transactions_df: pd.DataFrame, sessions_df: pd.DataFrame) -> dict:
    """
    Computes Data Analytics summaries for the Streamlit dashboard charts.
    """
    category_summary = (
        transactions_df.groupby('Category')
        .agg(Units_Sold=('Item', 'count'), Total_Revenue=('Price', 'sum'))
        .reset_index()
        .sort_values(by='Total_Revenue', ascending=False)
    )

    locality_summary = (
        sessions_df.groupby('Locality')
        .agg(Orders=('TransactionID', 'count'), Revenue=('Cart_Value', 'sum'), Bundle_Rate=('Bundle_Accepted', 'mean'))
        .reset_index()
        .sort_values(by='Revenue', ascending=False)
    )
    locality_summary['Bundle_Rate'] = (locality_summary['Bundle_Rate'] * 100).round(1)

    season_summary = (
        sessions_df.groupby('Is_Festival_Season')['Bundle_Accepted']
        .mean().reset_index()
    )
    season_summary['Season'] = season_summary['Is_Festival_Season'].map({0: 'Regular Days', 1: 'Festival Season (Dasara/Diwali)'})
    season_summary['Conversion_Pct'] = (season_summary['Bundle_Accepted'] * 100).round(1)

    return {
        "category_summary": category_summary,
        "locality_summary": locality_summary,
        "season_summary": season_summary
    }