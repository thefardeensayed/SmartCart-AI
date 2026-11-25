import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.catalog import CATALOG

def run_bayesian_inference_engine(
    transactions_df: pd.DataFrame,
    min_prior: float = 0.015,
    min_lift: float = 1.1
) -> pd.DataFrame:
    """
    Syllabus Alignment (BAINB501 - Module 2 & Module 3 / CO2 & CO3):
    1. Bayesian Inference: Computes Prior P(B), Likelihood P(A|B), and Exact Posterior P(B|A)
       using Bayes' Theorem: P(B|A) = [P(A|B) * P(B)] / P(A)
    2. Rule-Based Forward Chaining: Enforces domain compatibility rules (e.g., Anchor -> Accessory)
       so main devices are never recommended as add-on accessories.
    """
    total_orders = transactions_df["TransactionID"].nunique()
    if total_orders == 0:
        return pd.DataFrame()

    order_items = transactions_df.groupby("TransactionID")["Item"].apply(set)

    # 1. Marginal Prior Probabilities P(Item)
    item_counts = transactions_df.groupby("Item")["TransactionID"].nunique()
    priors = (item_counts / total_orders).to_dict()

    # 2. Co-occurrence Counts for Conditional Probability Tables (CPT)
    pair_counts = {}
    for items in order_items:
        item_list = list(items)
        for i in range(len(item_list)):
            for j in range(len(item_list)):
                if i != j:
                    pair = (item_list[i], item_list[j])
                    pair_counts[pair] = pair_counts.get(pair, 0) + 1

    # 3. Exact Bayes' Theorem & Forward-Chaining Domain Filtering
    records = []
    for (evidence_a, target_b), co_count in pair_counts.items():
        if evidence_a not in CATALOG or target_b not in CATALOG:
            continue

        # Forward-Chaining Rule: Never recommend an Anchor main device as an add-on
        if CATALOG[target_b]["is_anchor"]:
            continue

        p_a = priors.get(evidence_a, 0)
        p_b = priors.get(target_b, 0)

        if p_a == 0 or p_b < min_prior:
            continue

        p_a_and_b = co_count / total_orders
        likelihood_a_given_b = p_a_and_b / p_b
        posterior_b_given_a = (likelihood_a_given_b * p_b) / p_a
        bayesian_lift = posterior_b_given_a / p_b

        if bayesian_lift < min_lift:
            continue

        bundle_score = round(
            (posterior_b_given_a * 45)
            + (min(bayesian_lift, 10.0) / 10.0 * 40)
            + (min(p_a_and_b, 0.10) / 0.10 * 15),
            1
        )

        records.append({
            "Evidence_Item": evidence_a,
            "Recommended_Accessory": target_b,
            "Prior_Prob": round(p_b, 4),
            "Likelihood": round(likelihood_a_given_b, 4),
            "Posterior_Prob": round(posterior_b_given_a, 4),
            "Bayesian_Lift": round(bayesian_lift, 2),
            "Bundle_Score": bundle_score
        })

    if not records:
        return pd.DataFrame()

    rules_df = pd.DataFrame(records)
    return rules_df.sort_values(by=["Bundle_Score", "Posterior_Prob"], ascending=False).reset_index(drop=True)


def get_eda_summaries(transactions_df: pd.DataFrame, sessions_df: pd.DataFrame) -> dict:
    category_summary = (
        transactions_df.groupby("Category")
        .agg(Units_Sold=("Item", "count"), Total_Revenue=("Price", "sum"))
        .reset_index()
        .sort_values(by="Total_Revenue", ascending=False)
    )

    locality_summary = (
        sessions_df.groupby("Locality")
        .agg(Orders=("TransactionID", "count"), Revenue=("Cart_Value", "sum"), Bundle_Rate=("Bundle_Accepted", "mean"))
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
    )
    locality_summary["Bundle_Rate"] = (locality_summary["Bundle_Rate"] * 100).round(1)

    season_summary = (
        sessions_df.groupby("Is_Festival_Season")["Bundle_Accepted"]
        .mean().reset_index()
    )
    season_summary["Season"] = season_summary["Is_Festival_Season"].map({0: "Regular Days", 1: "Festival Season (Dasara/Diwali)"})
    season_summary["Conversion_Pct"] = (season_summary["Bundle_Accepted"] * 100).round(1)

    return {
        "category_summary": category_summary,
        "locality_summary": locality_summary,
        "season_summary": season_summary
    }