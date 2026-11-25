import os
import sys
import numpy as np
import pandas as pd

# Ensure root folder is in path when running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.catalog import CATALOG

def generate_ecommerce_data(num_records=25000, seed=42):
    np.random.seed(seed)
    os.makedirs("data", exist_ok=True)
    
    # 1. 30 Bengaluru Electronics Stores Master Data
    stores_data = [
        ("BLR_001", "Croma - Indiranagar 100ft Rd", "Croma", "Indiranagar", "560038", "Flagship Retail"),
        ("BLR_002", "Reliance Digital - Mantri Square", "Reliance Digital", "Malleshwaram", "560003", "Mall Retail"),
        ("BLR_003", "Pai International - Jayanagar 4th Block", "Pai International", "Jayanagar", "560011", "Multi-Brand Retail"),
        ("BLR_004", "Croma - Koramangala 80ft Rd", "Croma", "Koramangala", "560029", "Flagship Retail"),
        ("BLR_005", "Reliance Digital - Phoenix Marketcity", "Reliance Digital", "Whitefield", "560048", "Mall Retail"),
        ("BLR_006", "Sangeetha Gadgets - Marathahalli", "Sangeetha Gadgets", "Marathahalli", "560037", "Mobile & Audio Hub"),
        ("BLR_007", "Girias - Shantinagar", "Girias", "Shantinagar", "560027", "Home & Electronics"),
        ("BLR_008", "Croma - Electronic City Phase 1", "Croma", "Electronic City", "560100", "IT Hub Retail"),
        ("BLR_009", "Kanchan Computers - SP Road", "Independent", "SP Road", "560002", "Wholesale & Hardware"),
        ("BLR_010", "Sri Lakshmi Electronics - SP Road", "Independent", "SP Road", "560002", "Wholesale & Hardware"),
        ("BLR_011", "Pai International - Hebbal", "Pai International", "Hebbal", "560024", "Multi-Brand Retail"),
        ("BLR_012", "Reliance Digital - Galleria Mall", "Reliance Digital", "Yelahanka", "560064", "Mall Retail"),
        ("BLR_013", "Croma - HSR Layout Sector 2", "Croma", "HSR Layout", "560102", "Flagship Retail"),
        ("BLR_014", "Devi International - Jayanagar", "Devi International", "Jayanagar", "560011", "Multi-Brand Retail"),
        ("BLR_015", "iPlanet - Indiranagar", "iPlanet", "Indiranagar", "560038", "Brand Exclusive"),
        ("BLR_016", "Croma - Orion Mall", "Croma", "Rajajinagar", "560055", "Mall Retail"),
        ("BLR_017", "Reliance Digital - Nexus Mall", "Reliance Digital", "Koramangala", "560095", "Mall Retail"),
        ("BLR_018", "Pai International - JP Nagar", "Pai International", "JP Nagar", "560078", "Multi-Brand Retail"),
        ("BLR_019", "Girias - Banashankari", "Girias", "Banashankari", "560070", "Home & Electronics"),
        ("BLR_020", "Croma - Bellandur ORR", "Croma", "Bellandur", "560103", "IT Hub Retail"),
        ("BLR_021", "Sangeetha Gadgets - MG Road", "Sangeetha Gadgets", "MG Road", "560001", "Mobile & Audio Hub"),
        ("BLR_022", "Reliance Digital - Vega City Mall", "Reliance Digital", "Bannerghatta Road", "560076", "Mall Retail"),
        ("BLR_023", "iPlanet - UB City", "iPlanet", "Vittal Mallya Road", "560001", "Brand Exclusive"),
        ("BLR_024", "Ankit Infotech - SP Road", "Independent", "SP Road", "560002", "Wholesale & Hardware"),
        ("BLR_025", "Pai International - BTM Layout", "Pai International", "BTM Layout", "560076", "Multi-Brand Retail"),
        ("BLR_026", "Croma - Kammanahalli", "Croma", "Kammanahalli", "560084", "Flagship Retail"),
        ("BLR_027", "Reliance Digital - Bhartiya Mall", "Reliance Digital", "Thanisandra", "560064", "Mall Retail"),
        ("BLR_028", "Sangeetha Gadgets - Vijayanagar", "Sangeetha Gadgets", "Vijayanagar", "560040", "Mobile & Audio Hub"),
        ("BLR_029", "Girias - RT Nagar", "Girias", "RT Nagar", "560032", "Home & Electronics"),
        ("BLR_030", "Poorvika Mobiles - Malleshwaram", "Poorvika", "Malleshwaram", "560003", "Mobile & Audio Hub"),
    ]
    stores_df = pd.DataFrame(stores_data, columns=["Store_ID", "Store_Name", "Chain", "Locality", "Pincode", "Store_Type"])
    stores_df.to_csv("data/bengaluru_electronics_stores.csv", index=False)

    # 2. Bundle Association Rules Map (Anchor -> [(Accessory, Probability), ...])
    bundle_patterns = {
        "Gaming Laptop": [("Wireless Mouse", 0.72), ("Mechanical Keyboard", 0.54), ("Laptop Cooling Pad", 0.45), ("Laptop Backpack", 0.38)],
        "Ultrabook Laptop": [("Wireless Mouse", 0.75), ("USB-C Multiport Hub", 0.58), ("Laptop Backpack", 0.44), ("1TB Portable NVMe SSD", 0.30)],
        "Desktop Mini PC": [("27-inch 4K Monitor", 0.68), ("Mechanical Keyboard", 0.65), ("Wireless Mouse", 0.70), ("Wi-Fi 6 Dual-Band Router", 0.28)],
        "Flagship Smartphone": [("65W GaN Fast Charger", 0.74), ("MagSafe Silicone Case", 0.66), ("Privacy Tempered Glass", 0.55), ("TWS Wireless Earbuds", 0.38)],
        "5G Mid-Range Phone": [("65W GaN Fast Charger", 0.65), ("MagSafe Silicone Case", 0.60), ("Privacy Tempered Glass", 0.58), ("20000mAh Power Bank", 0.34)],
        "Pro Tablet 11-inch": [("Stylus Pen", 0.68), ("65W GaN Fast Charger", 0.50), ("TWS Wireless Earbuds", 0.35), ("64GB USB 3.2 Flash Drive", 0.25)],
        "ANC Over-Ear Headphones": [("Headphone Stand", 0.52), ("USB-C Multiport Hub", 0.25), ("20000mAh Power Bank", 0.22)],
        "Portable Bluetooth Speaker": [("20000mAh Power Bank", 0.48), ("65W GaN Fast Charger", 0.35), ("Smart Wi-Fi LED Strip", 0.28)],
        "Mirrorless DSLR Camera": [("128GB High-Speed SD Card", 0.76), ("Heavy-Duty Tripod", 0.48), ("Waterproof Camera Bag", 0.52), ("50mm Prime Lens", 0.34)],
        "4K Action Camera": [("128GB High-Speed SD Card", 0.78), ("Heavy-Duty Tripod", 0.42), ("Waterproof Camera Bag", 0.40), ("20000mAh Power Bank", 0.36)],
        "Next-Gen Gaming Console": [("Wireless Dual Controller", 0.68), ("7.1 Surround Gaming Headset", 0.50), ("Dual Controller Charging Dock", 0.44), ("Ultra High-Speed HDMI 2.1 Cable", 0.40)],
        "Handheld Gaming PC": [("1TB Portable NVMe SSD", 0.58), ("65W GaN Fast Charger", 0.52), ("TWS Wireless Earbuds", 0.42), ("20000mAh Power Bank", 0.45)],
        "55-inch 4K QLED Smart TV": [("Dolby Atmos Soundbar", 0.58), ("Swivel TV Wall Mount", 0.64), ("Surge Protector Extension", 0.52), ("Ultra High-Speed HDMI 2.1 Cable", 0.45)],
        "43-inch Full HD Smart TV": [("4K Streaming Stick", 0.54), ("Swivel TV Wall Mount", 0.60), ("Surge Protector Extension", 0.50), ("Smart Wi-Fi LED Strip", 0.32)],
        "AMOLED GPS Smartwatch": [("Magnetic Sport Watch Strap", 0.62), ("Watch Magnetic Charging Cable", 0.44), ("TWS Wireless Earbuds", 0.38)],
        "Fitness Tracker Band": [("Magnetic Sport Watch Strap", 0.58), ("Smart Bluetooth Weighing Scale", 0.42), ("Watch Magnetic Charging Cable", 0.40)],
        "Wi-Fi 6 Dual-Band Router": [("Wi-Fi Mesh Range Extender", 0.56), ("Cat-6 Ethernet Cable (10m)", 0.64), ("Surge Protector Extension", 0.35)],
    }

    anchor_list = list(bundle_patterns.keys())
    date_pool = pd.date_range(start="2025-11-01", end="2026-10-31", freq="D")
    dates = np.random.choice(date_pool, size=num_records)

    transactions = []
    customer_sessions = []

    print(f"⏳ Generating {num_records:,} transactions across {len(stores_data)} Bengaluru stores & {len(CATALOG)} products...")

    for tx_id in range(1, num_records + 1):
        order_id = f"BLR_ORD_{tx_id:06d}"
        order_date = pd.Timestamp(dates[tx_id - 1])
        month = order_date.month

        store = stores_data[np.random.randint(0, len(stores_data))]
        store_id, store_name, chain, locality, pincode, store_type = store

        # Dasara/Diwali Festival Season Spike in Oct/Nov
        is_festival = 1 if (month in [10, 11] and np.random.rand() < 0.75) or (np.random.rand() < 0.15) else 0
        past_orders = np.random.randint(0, 20)
        time_on_site_mins = round(np.random.uniform(1.5, 30.0), 1)
        discount_pct = np.random.choice([0, 5, 10, 15, 20, 25, 30], p=[0.18, 0.18, 0.24, 0.16, 0.12, 0.07, 0.05])
        payment_mode = np.random.choice(["UPI", "Credit Card", "Debit Card", "EMI", "Cash"], p=[0.42, 0.28, 0.12, 0.13, 0.05])

        anchor_choice = anchor_list[np.random.randint(0, len(anchor_list))]
        basket = [anchor_choice]

        for accessory, prob in bundle_patterns[anchor_choice]:
            if np.random.rand() < prob:
                basket.append(accessory)

        cart_value = sum(CATALOG[item]["price"] for item in basket)

        for item in basket:
            transactions.append({
                "TransactionID": order_id,
                "Order_Date": order_date.strftime("%Y-%m-%d"),
                "Store_ID": store_id,
                "Store_Name": store_name,
                "Locality": locality,
                "Category": CATALOG[item]["category"],
                "Item": item,
                "Price": CATALOG[item]["price"],
                "Is_Festival": is_festival
            })

        # Supervised AI Target Logic
        prob_buy_bundle = (
            0.08 +
            (discount_pct * 0.017) +
            (is_festival * 0.22) +
            (min(time_on_site_mins, 20) * 0.010) +
            (min(past_orders, 12) * 0.014) +
            (0.05 if payment_mode in ["Credit Card", "EMI"] else 0.0)
        )
        prob_buy_bundle = np.clip(prob_buy_bundle + np.random.normal(0, 0.05), 0.05, 0.96)
        bundle_accepted = 1 if np.random.rand() < prob_buy_bundle else 0

        customer_sessions.append({
            "TransactionID": order_id,
            "Order_Date": order_date.strftime("%Y-%m-%d"),
            "Store_ID": store_id,
            "Store_Name": store_name,
            "Locality": locality,
            "Store_Type": store_type,
            "Payment_Mode": payment_mode,
            "Anchor_Product": anchor_choice,
            "Cart_Value": cart_value,
            "Items_In_Cart": len(basket),
            "Discount_Pct": discount_pct,
            "Is_Festival_Season": is_festival,
            "Past_Orders": past_orders,
            "Time_On_Site_Mins": time_on_site_mins,
            "Bundle_Accepted": bundle_accepted
        })

    tx_df = pd.DataFrame(transactions)
    sess_df = pd.DataFrame(customer_sessions)

    tx_df.to_csv("data/transactions.csv", index=False)
    sess_df.to_csv("data/customer_sessions.csv", index=False)
    print("✅ Step 2 Complete! Generated:")
    print(f"   • data/bengaluru_electronics_stores.csv ({len(stores_df)} stores)")
    print(f"   • data/transactions.csv ({len(tx_df):,} rows)")
    print(f"   • data/customer_sessions.csv ({len(sess_df):,} rows)")

if __name__ == "__main__":
    generate_ecommerce_data(num_records=25000)