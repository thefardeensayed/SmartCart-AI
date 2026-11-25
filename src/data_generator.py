import os
import random
import numpy as np
import pandas as pd
from src.catalog import CATALOG

BENGALURU_STORES = [
    ("BLR-01", "Croma - Indiranagar 100ft Rd", "Indiranagar"),
    ("BLR-02", "Reliance Digital - Koramangala 4th Block", "Koramangala"),
    ("BLR-03", "Pai International - Jayanagar 4th Block", "Jayanagar"),
    ("BLR-04", "Croma - Whitefield Phoenix Marketcity", "Whitefield"),
    ("BLR-05", "Reliance Digital - Orion Mall Malleshwaram", "Malleshwaram"),
    ("BLR-06", "Girias - Hebbal Ring Road", "Hebbal"),
    ("BLR-07", "Croma - Electronic City Phase 1", "Electronic City"),
    ("BLR-08", "SP Road Tech Hub - City Market", "SP Road"),
    ("BLR-09", "Reliance Digital - HSR Layout Sector 2", "HSR Layout"),
    ("BLR-10", "Pai International - Marathahalli Bridge", "Marathahalli"),
    ("BLR-11", "Croma - Yelahanka New Town", "Yelahanka"),
    ("BLR-12", "Reliance Digital - Bannerghatta Road", "Bannerghatta Road"),
    ("BLR-13", "Pai International - Rajajinagar", "Rajajinagar"),
    ("BLR-14", "Croma - JP Nagar 6th Phase", "JP Nagar"),
    ("BLR-15", "Reliance Digital - Bellandur Central", "Bellandur"),
    ("BLR-16", "Girias - BTM Layout 2nd Stage", "BTM Layout"),
    ("BLR-17", "Croma - Sarjapur Road", "Sarjapur Road"),
    ("BLR-18", "Reliance Digital - Banashankari 2nd Stage", "Banashankari"),
    ("BLR-19", "Pai International - Vijayanagar", "Vijayanagar"),
    ("BLR-20", "Croma - Kalyan Nagar HRBR", "Kalyan Nagar"),
    ("BLR-21", "Reliance Digital - RT Nagar", "RT Nagar"),
    ("BLR-22", "Girias - Basavanagudi", "Basavanagudi"),
    ("BLR-23", "Croma - MG Road Brigade Junction", "MG Road"),
    ("BLR-24", "Reliance Digital - Kengeri Satellite Town", "Kengeri"),
    ("BLR-25", "Pai International - Peenya Industrial Area", "Peenya"),
    ("BLR-26", "Croma - KR Puram Tin Factory", "KR Puram"),
    ("BLR-27", "Reliance Digital - Sahakarnagar", "Sahakarnagar"),
    ("BLR-28", "Girias - Ulsoor Lake Road", "Ulsoor"),
    ("BLR-29", "Croma - Sadashivanagar", "Sadashivanagar"),
    ("BLR-30", "Reliance Digital - Brookefield ITPL", "Brookefield"),
]

# Domain-realistic co-purchase patterns for generating realistic transactions
BUNDLE_AFFINITIES = {
    "Ultrabook Laptop": [("Wireless Ergonomic Mouse", 0.65), ("USB-C Multiport Hub", 0.55), ("Waterproof Laptop Backpack", 0.50), ("1TB Portable NVMe SSD", 0.35)],
    "Gaming Laptop": [("Mechanical RGB Keyboard", 0.70), ("7.1 Surround Gaming Headset", 0.65), ("Laptop Cooling Pad", 0.55), ("1TB Portable NVMe SSD", 0.45)],
    "MacBook Air M2": [("USB-C Multiport Hub", 0.75), ("Waterproof Laptop Backpack", 0.45), ("1TB Portable NVMe SSD", 0.40)],
    "All-in-One Desktop PC": [("Wireless Ergonomic Mouse", 0.60), ("Mechanical RGB Keyboard", 0.50), ("Surge Protector Power Strip", 0.45)],
    "Mini PC Workstation": [("27-inch 4K IPS Monitor", 0.65), ("Mechanical RGB Keyboard", 0.55), ("Wireless Ergonomic Mouse", 0.55)],
    "27-inch 4K IPS Monitor": [("Ultra High-Speed HDMI 2.1 Cable", 0.60), ("USB-C Multiport Hub", 0.40), ("Surge Protector Power Strip", 0.35)],
    "Flagship 5G Smartphone": [("65W GaN Fast Charger", 0.72), ("Tempered Glass & Armor Case", 0.68), ("MagSafe 10000mAh Powerbank", 0.45)],
    "Mid-Range 5G Phone": [("Tempered Glass & Armor Case", 0.75), ("65W GaN Fast Charger", 0.50), ("MagSafe 10000mAh Powerbank", 0.35)],
    "Foldable Smartphone": [("65W GaN Fast Charger", 0.70), ("MagSafe 10000mAh Powerbank", 0.55), ("Active Stylus Pen", 0.40)],
    "11-inch Pro Tablet": [("Active Stylus Pen", 0.68), ("65W GaN Fast Charger", 0.45), ("Tempered Glass & Armor Case", 0.55)],
    "E-Ink Digital Reader": [("Tempered Glass & Armor Case", 0.50), ("65W GaN Fast Charger", 0.30)],
    "ANC Over-Ear Headphones": [("Hard-Shell Headphone Case", 0.65), ("65W GaN Fast Charger", 0.30)],
    "True Wireless Earbuds": [("Tempered Glass & Armor Case", 0.35), ("65W GaN Fast Charger", 0.30)],
    "AMOLED Fitness Smartwatch": [("Silicone Watch Strap Pack", 0.70), ("65W GaN Fast Charger", 0.25)],
    "Dolby Atmos Soundbar": [("Ultra High-Speed HDMI 2.1 Cable", 0.65), ("Surge Protector Power Strip", 0.45)],
    "Portable Bluetooth Speaker": [("65W GaN Fast Charger", 0.40), ("MagSafe 10000mAh Powerbank", 0.35)],
    "Mirrorless 4K Camera": [("50mm f/1.8 Prime Lens", 0.62), ("128GB High-Speed SDXC Card", 0.75), ("Carbon Fiber Tripod", 0.55)],
    "4K Waterproof Action Camera": [("128GB High-Speed SDXC Card", 0.78), ("Carbon Fiber Tripod", 0.48), ("MagSafe 10000mAh Powerbank", 0.40)],
    "Foldable GPS Camera Drone": [("128GB High-Speed SDXC Card", 0.72), ("MagSafe 10000mAh Powerbank", 0.45)],
    "Next-Gen Gaming Console": [("Extra Wireless Controller", 0.68), ("Dual Controller Charging Dock", 0.58), ("7.1 Surround Gaming Headset", 0.50), ("Ultra High-Speed HDMI 2.1 Cable", 0.45)],
    "Handheld Gaming PC": [("1TB Portable NVMe SSD", 0.65), ("65W GaN Fast Charger", 0.55), ("7.1 Surround Gaming Headset", 0.42)],
    "VR Headset 128GB": [("65W GaN Fast Charger", 0.50), ("Hard-Shell Headphone Case", 0.45)],
    "55-inch 4K QLED Smart TV": [("Heavy-Duty Swivel TV Wall Mount", 0.70), ("Ultra High-Speed HDMI 2.1 Cable", 0.62), ("Surge Protector Power Strip", 0.55)],
    "4K Laser Home Projector": [("Ultra High-Speed HDMI 2.1 Cable", 0.65), ("Carbon Fiber Tripod", 0.45), ("Surge Protector Power Strip", 0.45)],
    "Smart Home Hub Display": [("Surge Protector Power Strip", 0.40), ("Wi-Fi Mesh Extender", 0.35)],
    "Robotic Vacuum & Mop": [("Surge Protector Power Strip", 0.35), ("Wi-Fi Mesh Extender", 0.30)],
    "Wi-Fi 6 Dual-Band Router": [("Cat-6 Ethernet Cable (10m)", 0.65), ("Wi-Fi Mesh Extender", 0.50), ("Surge Protector Power Strip", 0.35)],
}

def generate_ecommerce_data(num_records: int = 25000, seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    os.makedirs("data", exist_ok=True)

    stores_df = pd.DataFrame(BENGALURU_STORES, columns=["Store_ID", "Store_Name", "Locality"])
    stores_df.to_csv("data/bengaluru_electronics_stores.csv", index=False)

    anchor_items = [k for k, v in CATALOG.items() if v["is_anchor"]]
    accessory_items = [k for k, v in CATALOG.items() if not v["is_anchor"]]

    tx_rows = []
    session_rows = []

    for idx in range(1, num_records + 1):
        tx_id = f"BLR-TX-{idx:06d}"
        store_id, store_name, locality = random.choice(BENGALURU_STORES)

        # Pick 1 primary anchor item
        primary = random.choice(anchor_items)
        basket = [primary]

        # Add correlated accessories based on domain affinities
        for acc, prob in BUNDLE_AFFINITIES.get(primary, []):
            if random.random() < prob:
                basket.append(acc)

        # Small random noise item
        if random.random() < 0.12:
            extra = random.choice(accessory_items)
            if extra not in basket:
                basket.append(extra)

        cart_value = sum(CATALOG[item]["price"] for item in basket)
        items_in_cart = len(basket)
        discount_pct = random.choice([0, 5, 10, 15, 20, 25])
        is_festival = 1 if random.random() < 0.32 else 0
        past_orders = int(np.clip(np.random.poisson(4.5), 0, 20))
        time_on_site = round(float(np.clip(np.random.normal(9.5, 4.5), 1.5, 30.0)), 1)

        # Realistic behavioral propensity logit for Bundle_Accepted (target variable)
        logit = (
            -2.6
            + 0.14 * discount_pct
            + 0.85 * is_festival
            + 0.11 * past_orders
            + 0.06 * time_on_site
            + (0.45 if cart_value > 40000 else 0.0)
            + np.random.normal(0, 0.55)
        )
        prob_accept = 1.0 / (1.0 + np.exp(-logit))
        bundle_accepted = 1 if random.random() < prob_accept else 0

        for item in basket:
            tx_rows.append({
                "TransactionID": tx_id,
                "Store_ID": store_id,
                "Locality": locality,
                "Item": item,
                "Category": CATALOG[item]["category"],
                "Price": CATALOG[item]["price"]
            })

        session_rows.append({
            "TransactionID": tx_id,
            "Store_ID": store_id,
            "Store_Name": store_name,
            "Locality": locality,
            "Cart_Value": cart_value,
            "Items_In_Cart": items_in_cart,
            "Discount_Pct": discount_pct,
            "Is_Festival_Season": is_festival,
            "Past_Orders": past_orders,
            "Time_On_Site_Mins": time_on_site,
            "Bundle_Accepted": bundle_accepted
        })

    pd.DataFrame(tx_rows).to_csv("data/transactions.csv", index=False)
    pd.DataFrame(session_rows).to_csv("data/customer_sessions.csv", index=False)
    print(f"Generated {num_records:,} Bengaluru sessions and {len(tx_rows):,} line-item transactions.")

if __name__ == "__main__":
    generate_ecommerce_data(num_records=25000)