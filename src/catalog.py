# src/catalog.py

CATALOG = {
    # 1. COMPUTERS & LAPTOPS (9 items)
    "Gaming Laptop": {"price": 85000, "category": "Computers & Laptops", "icon": "💻", "is_anchor": True},
    "Ultrabook Laptop": {"price": 65000, "category": "Computers & Laptops", "icon": "💻", "is_anchor": True},
    "Desktop Mini PC": {"price": 42000, "category": "Computers & Laptops", "icon": "🖥️", "is_anchor": True},
    "27-inch 4K Monitor": {"price": 24000, "category": "Computers & Laptops", "icon": "🖥️", "is_anchor": False},
    "Wireless Mouse": {"price": 1200, "category": "Computers & Laptops", "icon": "🖱️", "is_anchor": False},
    "Mechanical Keyboard": {"price": 3200, "category": "Computers & Laptops", "icon": "⌨️", "is_anchor": False},
    "Laptop Cooling Pad": {"price": 1600, "category": "Computers & Laptops", "icon": "❄️", "is_anchor": False},
    "Laptop Backpack": {"price": 1900, "category": "Computers & Laptops", "icon": "🎒", "is_anchor": False},
    "USB-C Multiport Hub": {"price": 2400, "category": "Computers & Laptops", "icon": "🔌", "is_anchor": False},

    # 2. SMARTPHONES & TABLETS (8 items)
    "Flagship Smartphone": {"price": 68000, "category": "Smartphones & Tablets", "icon": "📱", "is_anchor": True},
    "5G Mid-Range Phone": {"price": 28000, "category": "Smartphones & Tablets", "icon": "📱", "is_anchor": True},
    "Pro Tablet 11-inch": {"price": 45000, "category": "Smartphones & Tablets", "icon": "📲", "is_anchor": True},
    "65W GaN Fast Charger": {"price": 1800, "category": "Smartphones & Tablets", "icon": "⚡", "is_anchor": False},
    "MagSafe Silicone Case": {"price": 800, "category": "Smartphones & Tablets", "icon": "🛡️", "is_anchor": False},
    "Privacy Tempered Glass": {"price": 500, "category": "Smartphones & Tablets", "icon": "🔲", "is_anchor": False},
    "20000mAh Power Bank": {"price": 2200, "category": "Smartphones & Tablets", "icon": "🔋", "is_anchor": False},
    "Stylus Pen": {"price": 3500, "category": "Smartphones & Tablets", "icon": "✒️", "is_anchor": False},

    # 3. AUDIO & HEADPHONES (6 items)
    "ANC Over-Ear Headphones": {"price": 18000, "category": "Audio & Headphones", "icon": "🎧", "is_anchor": True},
    "TWS Wireless Earbuds": {"price": 3500, "category": "Audio & Headphones", "icon": "🎵", "is_anchor": False},
    "Portable Bluetooth Speaker": {"price": 4800, "category": "Audio & Headphones", "icon": "🔊", "is_anchor": True},
    "Dolby Atmos Soundbar": {"price": 14500, "category": "Audio & Headphones", "icon": "📢", "is_anchor": False},
    "USB Condenser Mic": {"price": 5200, "category": "Audio & Headphones", "icon": "🎙️", "is_anchor": False},
    "Headphone Stand": {"price": 900, "category": "Audio & Headphones", "icon": "🗼", "is_anchor": False},

    # 4. CAMERAS & DRONES (6 items)
    "Mirrorless DSLR Camera": {"price": 58000, "category": "Cameras & Drones", "icon": "📷", "is_anchor": True},
    "4K Action Camera": {"price": 29000, "category": "Cameras & Drones", "icon": "📹", "is_anchor": True},
    "50mm Prime Lens": {"price": 16500, "category": "Cameras & Drones", "icon": "🔭", "is_anchor": False},
    "128GB High-Speed SD Card": {"price": 1400, "category": "Cameras & Drones", "icon": "💾", "is_anchor": False},
    "Heavy-Duty Tripod": {"price": 2600, "category": "Cameras & Drones", "icon": "📐", "is_anchor": False},
    "Waterproof Camera Bag": {"price": 2300, "category": "Cameras & Drones", "icon": "👜", "is_anchor": False},

    # 5. GAMING & CONSOLES (6 items)
    "Next-Gen Gaming Console": {"price": 49990, "category": "Gaming & Consoles", "icon": "🎮", "is_anchor": True},
    "Handheld Gaming PC": {"price": 54000, "category": "Gaming & Consoles", "icon": "🕹️", "is_anchor": True},
    "Wireless Dual Controller": {"price": 5600, "category": "Gaming & Consoles", "icon": "🎮", "is_anchor": False},
    "7.1 Surround Gaming Headset": {"price": 4500, "category": "Gaming & Consoles", "icon": "🎧", "is_anchor": False},
    "Dual Controller Charging Dock": {"price": 1900, "category": "Gaming & Consoles", "icon": "⚡", "is_anchor": False},
    "Ultra High-Speed HDMI 2.1 Cable": {"price": 850, "category": "Gaming & Consoles", "icon": "➰", "is_anchor": False},

    # 6. SMART TV & HOME ENTERTAINMENT (6 items)
    "55-inch 4K QLED Smart TV": {"price": 52000, "category": "Smart TV & Home", "icon": "📺", "is_anchor": True},
    "43-inch Full HD Smart TV": {"price": 26000, "category": "Smart TV & Home", "icon": "📺", "is_anchor": True},
    "4K Streaming Stick": {"price": 3999, "category": "Smart TV & Home", "icon": "スティック", "is_anchor": False},
    "Swivel TV Wall Mount": {"price": 1400, "category": "Smart TV & Home", "icon": "🔩", "is_anchor": False},
    "Surge Protector Extension": {"price": 1100, "category": "Smart TV & Home", "icon": "🔌", "is_anchor": False},
    "Smart Wi-Fi LED Strip": {"price": 1300, "category": "Smart TV & Home", "icon": "💡", "is_anchor": False},

    # 7. WEARABLES & HEALTH TECH (5 items)
    "AMOLED GPS Smartwatch": {"price": 7500, "category": "Wearables", "icon": "⌚", "is_anchor": True},
    "Fitness Tracker Band": {"price": 2499, "category": "Wearables", "icon": "📟", "is_anchor": True},
    "Magnetic Sport Watch Strap": {"price": 750, "category": "Wearables", "icon": "🎗️", "is_anchor": False},
    "Smart Bluetooth Weighing Scale": {"price": 1800, "category": "Wearables", "icon": "⚖️", "is_anchor": False},
    "Watch Magnetic Charging Cable": {"price": 600, "category": "Wearables", "icon": "🔌", "is_anchor": False},

    # 8. NETWORKING & STORAGE (6 items)
    "Wi-Fi 6 Dual-Band Router": {"price": 4200, "category": "Networking & Storage", "icon": "📡", "is_anchor": True},
    "1TB Portable NVMe SSD": {"price": 7800, "category": "Networking & Storage", "icon": "💽", "is_anchor": False},
    "2TB External Hard Drive": {"price": 5400, "category": "Networking & Storage", "icon": "🗄️", "is_anchor": False},
    "Wi-Fi Mesh Range Extender": {"price": 2600, "category": "Networking & Storage", "icon": "📶", "is_anchor": False},
    "Cat-6 Ethernet Cable (10m)": {"price": 450, "category": "Networking & Storage", "icon": "🔗", "is_anchor": False},
    "64GB USB 3.2 Flash Drive": {"price": 650, "category": "Networking & Storage", "icon": "💾", "is_anchor": False},
}

# Fix icon typo for Streaming Stick
CATALOG["4K Streaming Stick"]["icon"] = "📼"

def get_all_categories():
    return sorted(list(set(item["category"] for item in CATALOG.values())))