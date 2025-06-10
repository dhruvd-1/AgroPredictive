from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Complete Enhanced Indian States Crop Data
INDIAN_CROPS_DATA = {
    "Uttar Pradesh": {
        "crops": [
            "wheat",
            "rice",
            "maize",
            "sugarcane",
            "pulses",
            "potato",
            "fruits & vegetables",
        ],
        "climate": "Subtropical, 600-1200mm rainfall, 5-45°C temperature",
        "soil_types": "Alluvial soil, clayey soil, sandy loam",
        "major_rivers": "Ganga, Yamuna, Gomti, Ghaghra",
        "agricultural_seasons": {
            "Kharif": "June-October (Rice, Sugarcane, Maize)",
            "Rabi": "November-April (Wheat, Potato, Pulses)",
            "Zaid": "April-June (Fodder, Vegetables)",
        },
        "crop_details": {
            "wheat": {
                "icon": "🌾",
                "season": "Rabi",
                "area": "9.7 million hectares",
                "reasons": [
                    "🌊 Fertile Gangetic alluvial plains provide rich nutrients",
                    "❄️ Cool winter temperatures (5-20°C) ideal for wheat growth",
                    "💧 Extensive canal and tube well irrigation network",
                    "🚜 Mechanized farming with modern equipment",
                    "🏪 Assured government procurement at Minimum Support Price",
                ],
                "varieties": "HD-2967, PBW-550, DBW-88",
                "economic_importance": "Largest wheat producer in India (32% of national production), food security",
            },
            "sugarcane": {
                "icon": "🎋",
                "season": "Annual",
                "area": "2.3 million hectares",
                "reasons": [
                    "🌡️ Hot humid climate (20-35°C) perfect for sugarcane growth",
                    "💧 High water availability from rivers and canals",
                    "🏭 Well-established sugar mills and processing industry",
                    "🚚 Good transportation network for heavy crop",
                    "💰 High returns per hectare compared to cereals",
                ],
                "varieties": "CoS-767, CoS-8436, UP-05-142",
                "economic_importance": "45% of India's sugar production, supports 50+ sugar mills",
            },
            "potato": {
                "icon": "🥔",
                "season": "Rabi",
                "area": "0.6 million hectares",
                "reasons": [
                    "❄️ Cool winter climate (10-20°C) ideal for tuber development",
                    "🌱 Fertile alluvial soil with good drainage",
                    "💧 Adequate irrigation during winter season",
                    "🏪 Large urban markets for fresh consumption",
                    "🍟 Growing demand from food processing industry",
                ],
                "varieties": "Kufri Jyoti, Kufri Pukhraj, Kufri Badshah",
                "economic_importance": "35% of India's potato production, major vegetable crop",
            },
            "rice": {
                "icon": "🌾",
                "season": "Kharif",
                "area": "5.8 million hectares",
                "reasons": [
                    "🌊 Abundant water from Ganga river system",
                    "🌡️ Hot humid summer (25-35°C) for rice germination",
                    "🌧️ Adequate monsoon rainfall (800-1200mm)",
                    "👥 Traditional paddy cultivation expertise",
                    "🍚 Staple food for eastern UP population",
                ],
                "varieties": "Sarjoo-52, NDR-359, Pusa-44",
                "economic_importance": "12% of India's rice production, food security for 200+ million people",
            },
            "pulses": {
                "icon": "🫘",
                "season": "Rabi/Kharif",
                "area": "3.2 million hectares",
                "reasons": [
                    "🧬 Nitrogen fixation improves soil fertility",
                    "🥗 High protein content for nutritional security",
                    "🌵 Drought-tolerant varieties for marginal lands",
                    "🔄 Excellent crop rotation with cereals",
                    "💰 Premium prices for quality pulses",
                ],
                "varieties": "Pant U-19 (Arhar), K-851 (Lentil), Pant G-114 (Gram)",
                "economic_importance": "15% of India's pulse production, protein security",
            },
        },
    },
    "Maharashtra": {
        "crops": [
            "rice",
            "wheat",
            "jowar",
            "bajra",
            "cotton",
            "soybean",
            "sugarcane",
            "groundnut",
            "onion",
            "banana",
            "grapes",
        ],
        "climate": "Tropical to semi-arid, 400-3000mm rainfall, 10-40°C temperature",
        "soil_types": "Black cotton soil, red soil, alluvial soil",
        "major_rivers": "Godavari, Krishna, Tapi, Narmada",
        "agricultural_seasons": {
            "Kharif": "June-October (Cotton, Sugarcane, Rice, Soybean)",
            "Rabi": "November-March (Wheat, Jowar, Gram)",
            "Summer": "March-June (Groundnut, Fodder)",
        },
        "crop_details": {
            "cotton": {
                "icon": "🌸",
                "season": "Kharif",
                "area": "4.0 million hectares",
                "reasons": [
                    "🖤 Deep black cotton soil (regur) retains moisture perfectly",
                    "☀️ 200+ sunny days ideal for cotton fiber quality",
                    "🌤️ Semi-arid climate (600-1000mm) prevents diseases",
                    "🏭 Well-established textile industry in Mumbai region",
                    "👨‍🌾 Traditional cotton cultivation expertise for centuries",
                ],
                "varieties": "Bt Cotton RCH-2, MRC-7017, Bollgard-II",
                "economic_importance": "32% of India's cotton production, textile industry backbone",
            },
            "sugarcane": {
                "icon": "🎋",
                "season": "Annual",
                "area": "1.0 million hectares",
                "reasons": [
                    "🌊 Assured irrigation from major river projects",
                    "🏭 Cooperative sugar mills model - farmer ownership",
                    "🌡️ Favorable temperature and humidity in western region",
                    "🚚 Good road connectivity to mills",
                    "💰 Highest sugar recovery rates in India",
                ],
                "varieties": "CoM-0265, MS-12/104, CoS-8436",
                "economic_importance": "35% of India's sugar production, cooperative movement leader",
            },
            "soybean": {
                "icon": "🫛",
                "season": "Kharif",
                "area": "3.8 million hectares",
                "reasons": [
                    "🌧️ Adequate monsoon rainfall (700-1200mm)",
                    "🖤 Black soil provides good drainage and nutrients",
                    "🛢️ Growing edible oil industry demand",
                    "🧬 Nitrogen fixation improves soil health",
                    "💰 Export potential and good market prices",
                ],
                "varieties": "JS-335, MACS-450, DS-228",
                "economic_importance": "55% of India's soybean production, oilseed security",
            },
            "onion": {
                "icon": "🧅",
                "season": "Rabi/Kharif",
                "area": "0.5 million hectares",
                "reasons": [
                    "🌡️ Moderate temperature ideal for bulb formation",
                    "🌱 Well-drained black soil perfect for onions",
                    "🌍 Major export crop - Nashik onions world famous",
                    "🏪 Storage and processing facilities available",
                    "💰 High value crop with premium varieties",
                ],
                "varieties": "Bhima Super, Bhima Kiran, Agrifound Dark Red",
                "economic_importance": "25% of India's onion production, major export revenue",
            },
            "grapes": {
                "icon": "🍇",
                "season": "Perennial",
                "area": "0.15 million hectares",
                "reasons": [
                    "🌡️ Mediterranean-like climate in western region",
                    "🍷 Ideal for both table grapes and wine production",
                    "💧 Drip irrigation technology adoption",
                    "✈️ Export-oriented cultivation to Europe/Middle East",
                    "🏭 Growing wine industry in Nashik region",
                ],
                "varieties": "Thompson Seedless, Bangalore Blue, Sonaka",
                "economic_importance": "75% of India's grape production, wine industry hub",
            },
        },
    },
    "Punjab": {
        "crops": ["wheat", "rice", "maize", "cotton", "sugarcane", "sunflower"],
        "climate": "Semi-arid subtropical, 300-700mm rainfall, 5-45°C temperature",
        "soil_types": "Alluvial soil, sandy loam soil",
        "major_rivers": "Sutlej, Beas, Ravi",
        "agricultural_seasons": {
            "Kharif": "April-October (Rice, Cotton, Sugarcane)",
            "Rabi": "November-April (Wheat, Sunflower)",
            "Zaid": "April-June (Fodder, Vegetables)",
        },
        "crop_details": {
            "wheat": {
                "icon": "🌾",
                "season": "Rabi",
                "area": "3.5 million hectares",
                "reasons": [
                    "❄️ Cool winter temperature (5-20°C) ideal for wheat growth",
                    "💧 Excellent canal irrigation system from rivers",
                    "🚜 Highly mechanized farming with modern equipment",
                    "🧬 High-yielding variety (HYV) seeds from Green Revolution",
                    "🏪 Assured procurement by government at MSP",
                ],
                "varieties": "PBW-725, HD-3086, WH-1105",
                "economic_importance": "India's granary, 20% of national wheat production, food security",
            },
            "rice": {
                "icon": "🌾",
                "season": "Kharif",
                "area": "3.1 million hectares",
                "reasons": [
                    "🌊 Extensive canal irrigation network ensures water supply",
                    "🌡️ Hot summer (35-40°C) perfect for rice germination",
                    "🚜 Complete mechanization from sowing to harvesting",
                    "🧬 High-yielding Basmati and non-Basmati varieties",
                    "💰 Government procurement and export potential",
                ],
                "varieties": "PUSA-44, PR-126, Basmati-1121",
                "economic_importance": "15% of India's rice production, Basmati export hub",
            },
        },
    },
    "Rajasthan": {
        "crops": ["wheat", "bajra", "maize", "pulses", "oilseeds", "cotton", "barley"],
        "climate": "Hot arid to semi-arid, 100-700mm rainfall, 2-50°C temperature",
        "soil_types": "Sandy soil, alluvial soil, red soil",
        "major_rivers": "Limited - mostly canal irrigation",
        "agricultural_seasons": {
            "Kharif": "July-October (Bajra, Cotton, Maize)",
            "Rabi": "November-April (Wheat, Mustard, Gram)",
            "Summer": "April-June (Fodder crops)",
        },
        "crop_details": {
            "bajra": {
                "icon": "🌾",
                "season": "Kharif",
                "area": "4.5 million hectares",
                "reasons": [
                    "🌵 Extremely drought-resistant, survives with 250mm rainfall",
                    "🏜️ Adapted to sandy arid soils of Thar desert",
                    "🌡️ Heat-tolerant, withstands temperatures up to 45°C",
                    "🐄 Dual purpose - grain for food, stalk for fodder",
                    "⚡ Short duration crop (70-90 days) suits erratic rainfall",
                ],
                "varieties": "HHB-67, Raj-171, ICMH-356",
                "economic_importance": "50% of India's bajra production, dryland farming backbone",
            },
            "mustard": {
                "icon": "🌻",
                "season": "Rabi",
                "area": "2.8 million hectares",
                "reasons": [
                    "❄️ Cool winter climate ideal for mustard flowering",
                    "🌵 Low water requirement suits arid conditions",
                    "🛢️ High oil content (38-42%) for edible oil",
                    "🌱 Grows well in sandy soils with low fertility",
                    "💰 Premium prices for quality mustard oil",
                ],
                "varieties": "Pusa Bold, RH-30, Kranti",
                "economic_importance": "45% of India's mustard production, cooking oil security",
            },
            "wheat": {
                "icon": "🌾",
                "season": "Rabi",
                "area": "3.0 million hectares",
                "reasons": [
                    "💧 Canal irrigation from Indira Gandhi Canal",
                    "❄️ Cool winter temperatures in northern districts",
                    "🌱 Improved varieties adapted to arid conditions",
                    "🚜 Mechanization increasing productivity",
                    "🏪 Government support and procurement facilities",
                ],
                "varieties": "Raj-3765, HD-2967, WH-147",
                "economic_importance": "8% of India's wheat production, desert agriculture success",
            },
        },
    },
    "West Bengal": {
        "crops": [
            "rice",
            "potato",
            "jute",
            "tea",
            "sugarcane",
            "oilseeds",
            "maize",
            "pulses",
            "fruits & vegetables",
        ],
        "climate": "Tropical humid, 1500-2500mm rainfall, 15-40°C temperature",
        "soil_types": "Alluvial soil, laterite soil, hill soil",
        "major_rivers": "Ganga, Hooghly, Brahmaputra",
        "agricultural_seasons": {
            "Boro": "December-May (Summer rice)",
            "Aman": "July-December (Monsoon rice)",
            "Rabi": "November-April (Potato, Wheat, Oilseeds)",
        },
        "crop_details": {
            "rice": {
                "icon": "🌾",
                "season": "Aman/Boro/Aus",
                "area": "5.5 million hectares",
                "reasons": [
                    "🌊 Abundant water from Ganga delta and high rainfall",
                    "🌡️ Hot humid climate ideal for rice cultivation",
                    "🌧️ Long monsoon season (June-October)",
                    "👥 Traditional expertise in three-season rice cultivation",
                    "🍚 Staple food supporting 100+ million people",
                ],
                "varieties": "IET-4786, Lalat, Ranjit, Satabdi",
                "economic_importance": "15% of India's rice production, food security for eastern India",
            },
            "potato": {
                "icon": "🥔",
                "season": "Rabi",
                "area": "0.4 million hectares",
                "reasons": [
                    "❄️ Cool winter climate (10-25°C) perfect for tuber formation",
                    "🌱 Fertile alluvial soil of Ganga plains",
                    "💧 Adequate irrigation during winter season",
                    "🏙️ Large urban markets in Kolkata and surrounding areas",
                    "🚚 Good transportation network for perishable crop",
                ],
                "varieties": "Kufri Jyoti, Kufri Chandramukhi, Cardinal",
                "economic_importance": "25% of India's potato production, major commercial crop",
            },
            "jute": {
                "icon": "🌿",
                "season": "Kharif",
                "area": "0.6 million hectares",
                "reasons": [
                    "🌧️ High humidity and rainfall (1500mm+) ideal for jute",
                    "🌊 Alluvial soil of delta region perfect for fiber quality",
                    "🏭 Traditional jute mills and processing infrastructure",
                    "🌍 Natural fiber demand for eco-friendly products",
                    "👨‍🌾 Generations of expertise in jute cultivation",
                ],
                "varieties": "JRO-204, JRO-632, Suren",
                "economic_importance": "80% of India's jute production, textile industry raw material",
            },
            "tea": {
                "icon": "🍃",
                "season": "Perennial",
                "area": "0.13 million hectares",
                "reasons": [
                    "🏔️ Darjeeling hills provide ideal altitude (1000-2000m)",
                    "🌧️ High rainfall and humidity perfect for tea leaves",
                    "🌡️ Cool temperature in hills ideal for quality tea",
                    "🌍 World-famous Darjeeling tea with international demand",
                    "👨‍🌾 British-era established tea garden infrastructure",
                ],
                "varieties": "China Bush, Assam Bush, Clonal varieties",
                "economic_importance": "25% of India's tea production, premium export quality",
            },
        },
    },
    "Gujarat": {
        "crops": [
            "cotton",
            "groundnut",
            "wheat",
            "rice",
            "maize",
            "bajra",
            "tur",
            "gram",
            "sesame",
            "onion",
            "potato",
        ],
        "climate": "Semi-arid to arid, 300-1500mm rainfall, 10-45°C temperature",
        "soil_types": "Black cotton soil, alluvial soil, sandy soil",
        "major_rivers": "Narmada, Tapi, Sabarmati, Mahi",
        "agricultural_seasons": {
            "Kharif": "June-October (Cotton, Groundnut, Rice)",
            "Rabi": "November-April (Wheat, Gram, Mustard)",
            "Summer": "April-June (Fodder, Vegetables)",
        },
        "crop_details": {
            "cotton": {
                "icon": "🌸",
                "season": "Kharif",
                "area": "2.6 million hectares",
                "reasons": [
                    "🖤 Deep black cotton soil ideal for cotton cultivation",
                    "☀️ Abundant sunshine (200+ clear days) for fiber development",
                    "🌤️ Semi-arid climate prevents fungal diseases",
                    "🏭 Well-developed textile industry in Ahmedabad region",
                    "💧 Narmada canal irrigation ensuring water supply",
                ],
                "varieties": "Bt Cotton, RCH-2, MRC-7017, BGII-1534",
                "economic_importance": "35% of India's cotton production, textile industry leader",
            },
            "groundnut": {
                "icon": "🥜",
                "season": "Kharif/Summer",
                "area": "1.9 million hectares",
                "reasons": [
                    "🏖️ Sandy loam soil provides excellent drainage",
                    "🌵 Drought-resistant crop suitable for semi-arid climate",
                    "🛢️ High oil content (48-50%) for edible oil industry",
                    "🌡️ Warm temperature ideal for pod development",
                    "🏭 Well-established oil extraction industry",
                ],
                "varieties": "GG-20, TAG-24, GPBD-4, TG-37A",
                "economic_importance": "40% of India's groundnut production, oilseed leader",
            },
            "wheat": {
                "icon": "🌾",
                "season": "Rabi",
                "area": "0.8 million hectares",
                "reasons": [
                    "💧 Narmada irrigation project provides assured water",
                    "❄️ Cool winter climate in northern Gujarat",
                    "🌱 Fertile alluvial soil in irrigated areas",
                    "🚜 Modern farming techniques adoption",
                    "🏪 Good market infrastructure and storage facilities",
                ],
                "varieties": "GW-366, Lok-1, HD-2967",
                "economic_importance": "4% of India's wheat production, irrigation success story",
            },
        },
    },
    "Karnataka": {
        "crops": [
            "rice",
            "ragi",
            "maize",
            "jowar",
            "pulses",
            "coffee",
            "cotton",
            "sugarcane",
            "oilseeds",
            "cashew",
            "spices",
            "floriculture",
        ],
        "climate": "Tropical to temperate, 600-2500mm rainfall, 15-35°C temperature",
        "soil_types": "Red sandy soil, black cotton soil, laterite soil, alluvial soil",
        "major_rivers": "Cauvery, Krishna, Tungabhadra",
        "agricultural_seasons": {
            "Kharif": "June-October (Rice, Ragi, Cotton, Sugarcane)",
            "Rabi": "November-April (Jowar, Pulses, Oilseeds)",
            "Perennial": "Year-round (Coffee, Spices, Floriculture)",
        },
        "crop_details": {
            "coffee": {
                "icon": "☕",
                "season": "Perennial",
                "area": "0.23 million hectares",
                "reasons": [
                    "🏔️ Western Ghats elevation (1000-1500m) provides ideal altitude",
                    "🌧️ High rainfall (1500-2500mm) during monsoons",
                    "🌡️ Cool temperature (15-25°C) perfect for arabica coffee",
                    "🌳 Forest canopy provides natural shade for coffee plants",
                    "☁️ Misty climate reduces direct sunlight stress",
                ],
                "varieties": "Arabica (70%), Robusta (30%) - Coorg famous worldwide",
                "economic_importance": "70% of India's coffee production, ₹3000+ crores revenue",
            },
            "ragi": {
                "icon": "🌾",
                "season": "Kharif",
                "area": "1.0 million hectares",
                "reasons": [
                    "🌵 Extremely drought-resistant, survives with 300mm rainfall",
                    "🏔️ Grows well in hilly terrains and marginal lands",
                    "⚡ High nutritional value - finger millet rich in calcium",
                    "🌡️ Heat-tolerant crop suitable for changing climate",
                    "🏪 Traditional food grain with increasing health-conscious demand",
                ],
                "varieties": "GPU-28, MR-1, KMR-204",
                "economic_importance": "Nutritional security, tribal economy, health food market",
            },
            "floriculture": {
                "icon": "🌸",
                "season": "Year-round",
                "area": "0.02 million hectares",
                "reasons": [
                    "🌡️ Pleasant climate year-round for flower cultivation",
                    "✈️ Proximity to Bangalore airport for flower export",
                    "🏭 Well-developed cold chain and processing facilities",
                    "💐 High demand from temple cities and urban markets",
                    "💰 Very high returns per unit area compared to cereals",
                ],
                "varieties": "Rose, Jasmine, Chrysanthemum, Carnation, Gerbera",
                "economic_importance": "₹2000+ crores industry, major flower exporter to Europe",
            },
            "spices": {
                "icon": "🌿",
                "season": "Perennial/Seasonal",
                "area": "0.5 million hectares",
                "reasons": [
                    "🌶️ Diverse agro-climatic zones support various spices",
                    "🏔️ Western Ghats biodiversity hotspot for spice cultivation",
                    "🌧️ High rainfall areas perfect for cardamom and pepper",
                    "🏭 Traditional knowledge and processing expertise",
                    "🌍 International demand for organic Indian spices",
                ],
                "varieties": "Cardamom (Queen of Spices), Black Pepper, Turmeric, Coriander",
                "economic_importance": "High value crops, export potential, rural employment",
            },
        },
    },
    "Andhra Pradesh": {
        "crops": [
            "rice",
            "maize",
            "cotton",
            "groundnut",
            "chilies",
            "tobacco",
            "pulses",
        ],
        "climate": "Hot semi-arid to tropical, 600-1200mm rainfall, 15-45°C temperature",
        "soil_types": "Black cotton soil, red sandy soil, alluvial soil",
        "major_rivers": "Krishna, Godavari, Pennar",
        "agricultural_seasons": {
            "Kharif": "June-October (Rice, Cotton, Maize, Groundnut)",
            "Rabi": "November-April (Wheat, Gram, Tobacco)",
            "Summer": "April-June (Groundnut, Sesame)",
        },
        "crop_details": {
            "rice": {
                "icon": "🌾",
                "season": "Kharif",
                "area": "2.4 million hectares",
                "reasons": [
                    "🌊 Abundant water from Krishna and Godavari delta regions",
                    "🌡️ High temperature (25-35°C) ideal for rice growth",
                    "💧 Monsoon rainfall (600-1200mm) perfect for paddy cultivation",
                    "🏞️ Flat deltaic plains suitable for flood irrigation",
                    "👥 Traditional expertise in paddy cultivation for centuries",
                ],
                "varieties": "BPT-5204, MTU-1010, Improved Samba Mahsuri",
                "economic_importance": "Staple food for 50+ million people, major export commodity",
            },
            "chilies": {
                "icon": "🌶️",
                "season": "Kharif/Rabi",
                "area": "0.3 million hectares",
                "reasons": [
                    "🔥 Hot dry climate perfect for capsaicin development",
                    "☀️ Intense sunlight increases pungency and color",
                    "🌬️ Low humidity prevents fungal diseases",
                    "🏭 Well-established spice processing industry",
                    "🌍 World's largest chili exporter - Guntur famous globally",
                ],
                "varieties": "Guntur Sannam, Teja, Byadgi",
                "economic_importance": "₹5000+ crores export value, supports 2+ million farmers",
            },
        },
    },
    "Tamil Nadu": {
        "crops": [
            "rice",
            "sugarcane",
            "banana",
            "coconut",
            "tapioca",
            "cloves",
            "cotton",
            "maize",
            "groundnut",
            "millets",
            "oilseeds",
        ],
        "climate": "Tropical, 600-1500mm rainfall, 20-40°C temperature",
        "soil_types": "Alluvial soil, red soil, black soil, coastal sandy soil",
        "major_rivers": "Cauvery, Vaigai, Tamiraparani",
        "agricultural_seasons": {
            "Kuruvai": "June-September (Early rice)",
            "Samba": "August-January (Main rice season)",
            "Navarai": "December-April (Summer rice)",
        },
        "crop_details": {
            "rice": {
                "icon": "🌾",
                "season": "Samba/Kuruvai",
                "area": "2.0 million hectares",
                "reasons": [
                    "🌊 Cauvery delta provides fertile alluvial soil",
                    "🌡️ Tropical climate ideal for year-round cultivation",
                    "💧 Traditional tank irrigation system",
                    "🍚 Staple food for Tamil population",
                    "🏛️ Ancient rice cultivation heritage dating back 2000+ years",
                ],
                "varieties": "ADT-43, CO-47, BPT-5204, Ponni",
                "economic_importance": "8% of India's rice production, cultural significance",
            },
            "sugarcane": {
                "icon": "🎋",
                "season": "Annual",
                "area": "0.35 million hectares",
                "reasons": [
                    "🌡️ Year-round warm climate ideal for sugarcane",
                    "💧 Cauvery river irrigation facilities",
                    "🏭 Well-established cooperative sugar mills",
                    "🚚 Good transportation to processing centers",
                    "💰 High sugar recovery rates due to climate",
                ],
                "varieties": "CoC-671, Co-86032, CoC-24",
                "economic_importance": "15% of India's sugar production, rural employment",
            },
            "banana": {
                "icon": "🍌",
                "season": "Year-round",
                "area": "0.08 million hectares",
                "reasons": [
                    "🌡️ Tropical climate suitable for continuous cultivation",
                    "🌊 Coastal humidity ideal for banana growth",
                    "💧 Adequate water supply from rivers and wells",
                    "🏪 Large domestic and export markets",
                    "🍽️ Traditional food and religious significance",
                ],
                "varieties": "Robusta, Rasthali, Poovan, Red Banana",
                "economic_importance": "20% of India's banana production, major fruit crop",
            },
        },
    },
    "Haryana": {
        "crops": ["wheat", "rice", "maize", "bajra", "sunflower", "sugarcane"],
        "climate": "Semi-arid subtropical, 300-700mm rainfall, 5-45°C temperature",
        "soil_types": "Alluvial soil, sandy loam soil",
        "major_rivers": "Yamuna, Ghaggar, Western Yamuna Canal",
        "agricultural_seasons": {
            "Kharif": "April-October (Rice, Cotton, Sugarcane)",
            "Rabi": "November-April (Wheat, Sunflower)",
            "Zaid": "April-June (Fodder, Vegetables)",
        },
        "crop_details": {
            "wheat": {
                "icon": "🌾",
                "season": "Rabi",
                "area": "2.5 million hectares",
                "reasons": [
                    "❄️ Cool winter climate (5-20°C) perfect for wheat",
                    "💧 Extensive canal and tube well irrigation",
                    "🚜 Complete farm mechanization adoption",
                    "🧬 High-yielding varieties from Green Revolution",
                    "🏪 Assured government procurement system",
                ],
                "varieties": "WH-1105, HD-3086, PBW-725",
                "economic_importance": "12% of India's wheat production, Green Revolution success",
            },
            "rice": {
                "icon": "🌾",
                "season": "Kharif",
                "area": "1.4 million hectares",
                "reasons": [
                    "🌊 Canal irrigation ensures adequate water supply",
                    "🌡️ Hot summer temperatures for rice germination",
                    "🚜 Mechanized cultivation practices",
                    "🧬 High-yielding Basmati varieties",
                    "💰 Premium prices for Basmati rice export",
                ],
                "varieties": "Pusa-44, PR-126, Basmati-370",
                "economic_importance": "7% of India's rice production, Basmati hub",
            },
        },
    },
    "Bihar": {
        "crops": ["rice", "wheat", "maize", "lentil", "litchi", "mango"],
        "climate": "Subtropical humid, 1000-1400mm rainfall, 5-40°C temperature",
        "soil_types": "Alluvial soil, sandy loam",
        "major_rivers": "Ganga, Sone, Gandak, Kosi",
        "agricultural_seasons": {
            "Kharif": "June-October (Rice, Maize, Sugarcane)",
            "Rabi": "November-April (Wheat, Lentil, Gram)",
            "Zaid": "April-June (Vegetables, Fodder)",
        },
        "crop_details": {
            "rice": {
                "icon": "🌾",
                "season": "Kharif",
                "area": "3.2 million hectares",
                "reasons": [
                    "🌊 Fertile Gangetic alluvial plains",
                    "🌧️ Adequate monsoon rainfall (1000-1400mm)",
                    "🌡️ Hot humid climate ideal for paddy",
                    "💧 Multiple rivers provide irrigation",
                    "👥 Traditional rice cultivation expertise",
                ],
                "varieties": "Rajendra Bhagwati, Sahbhagi Dhan, Swarna",
                "economic_importance": "7% of India's rice production, food security for 100+ million",
            },
            "wheat": {
                "icon": "🌾",
                "season": "Rabi",
                "area": "2.1 million hectares",
                "reasons": [
                    "❄️ Cool winter temperatures ideal for wheat",
                    "🌱 Rich alluvial soil provides nutrients",
                    "💧 Post-monsoon soil moisture and canal irrigation",
                    "🚜 Increasing mechanization adoption",
                    "🏪 Government procurement facilities",
                ],
                "varieties": "HD-2967, HD-3086, DBW-88",
                "economic_importance": "8% of India's wheat production, rural livelihood",
            },
            "litchi": {
                "icon": "🍇",
                "season": "Summer harvest",
                "area": "0.032 million hectares",
                "reasons": [
                    "🌡️ Hot humid climate perfect for litchi cultivation",
                    "🌧️ High humidity and adequate rainfall",
                    "🌱 Fertile Gangetic soil ideal for fruit trees",
                    "🏪 Traditional cultivation in Muzaffarpur region",
                    "🌍 World-famous Shahi litchi variety",
                ],
                "varieties": "Shahi, China, Rose Scented, Bombai",
                "economic_importance": "65% of India's litchi production, export potential",
            },
        },
    },
}


def get_location_info(lat, lng):
    """Get location information using reverse geocoding"""
    try:
        url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lng}&localityLanguage=en"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            city = data.get("city", data.get("locality", "Unknown"))
            region = data.get("principalSubdivision", "Unknown")
            country = data.get("countryName", "Unknown")

            return {
                "country": country,
                "region": region,
                "city": city,
                "full_location": f"{city}, {region}, {country}",
            }
    except Exception as e:
        print(f"Error getting location info: {str(e)}")

    return {
        "country": "Unknown",
        "region": "Unknown",
        "city": "Unknown",
        "full_location": "Unknown Location",
    }


def create_enhanced_crop_response(state_name, location_info, state_data):
    """Create a comprehensive, HTML formatted crop response"""

    # Header Section
    html_response = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #e0e0e0;">
        <div style="background: linear-gradient(135deg, #16a32a, #128724); padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
            <h2 style="color: white; margin: 0; font-size: 24px;">🌍 AGRICULTURAL PROFILE: {state_name.upper()}</h2>
            <p style="color: #f0f0f0; margin: 10px 0 0 0; font-size: 16px;">📍 {location_info["full_location"]}</p>
        </div>

        <div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #333;">
            <h3 style="color: #16a32a; margin-top: 0;">🌦️ CLIMATE OVERVIEW</h3>
            <p style="margin: 10px 0;">{state_data.get("climate", "Varies across the state")}</p>
            
            <h3 style="color: #16a32a;">🌱 SOIL TYPES</h3>
            <p style="margin: 10px 0;">{state_data.get("soil_types", "Mixed soil types")}</p>
            
            <h3 style="color: #16a32a;">🌊 MAJOR WATER SOURCES</h3>
            <p style="margin: 10px 0;">{state_data.get("major_rivers", "Various rivers and irrigation systems")}</p>
            
            <h3 style="color: #16a32a;">📅 AGRICULTURAL SEASONS</h3>
    """

    # Add seasonal information
    seasons = state_data.get("agricultural_seasons", {})
    for season, details in seasons.items():
        html_response += (
            f"<p style='margin: 8px 0;'><strong>{season}:</strong> {details}</p>"
        )

    html_response += "</div>"

    # Crops Header
    html_response += f"""
        <div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; border: 1px solid #333;">
            <h3 style="color: #16a32a; margin-top: 0; text-align: center;">🌾 MAJOR CROPS ANALYSIS ({len(state_data["crops"])} Main Crops)</h3>
    """

    # Detailed crop information
    crop_details = state_data.get("crop_details", {})

    for i, crop in enumerate(state_data["crops"], 1):
        if crop in crop_details:
            crop_info = crop_details[crop]

            html_response += f"""
            <div style="background-color: #2a2a2a; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #16a32a;">
                <h4 style="color: #16a32a; margin-top: 0; font-size: 18px;">
                    {i}. {crop_info.get("icon", "🌱")} {crop.upper()}
                </h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                    <div>
                        <p style="margin: 5px 0;"><strong>🗓️ Season:</strong> {crop_info.get("season", "Multiple seasons")}</p>
                        {f"<p style='margin: 5px 0;'><strong>📏 Area:</strong> {crop_info['area']}</p>" if "area" in crop_info else ""}
                    </div>
                    <div>
                        {f"<p style='margin: 5px 0;'><strong>🧬 Varieties:</strong> {crop_info['varieties']}</p>" if "varieties" in crop_info else ""}
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <h5 style="color: #16a32a; margin: 10px 0;">🎯 Why Suitable for {state_name}:</h5>
                    <ul style="padding-left: 20px; margin: 0;">
            """

            for reason in crop_info.get("reasons", []):
                html_response += (
                    f"<li style='margin: 8px 0; color: #e0e0e0;'>{reason}</li>"
                )

            html_response += "</ul></div>"

            if "economic_importance" in crop_info:
                html_response += f"""
                <div style="background-color: #333; padding: 10px; border-radius: 5px;">
                    <p style="margin: 0;"><strong>💰 Economic Impact:</strong> {crop_info["economic_importance"]}</p>
                </div>
                """

            html_response += "</div>"
        else:
            # Fallback for crops without detailed data
            html_response += f"""
            <div style="background-color: #2a2a2a; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #16a32a;">
                <h4 style="color: #16a32a; margin-top: 0;">{i}. 🌱 {crop.upper()}</h4>
                <p style="margin: 0;">Important crop adapted to local climate and soil conditions of {state_name}</p>
            </div>
            """

    # Summary section
    html_response += f"""
        </div>
        
        <div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; margin-top: 20px; border: 1px solid #333;">
            <h3 style="color: #16a32a; margin-top: 0;">📊 AGRICULTURAL SUMMARY</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <p style="margin: 8px 0;"><strong>Total Major Crops:</strong> {len(state_data["crops"])}</p>
                    <p style="margin: 8px 0;"><strong>Agricultural Diversity:</strong> High diversity suited to local conditions</p>
                </div>
                <div>
                    <p style="margin: 8px 0;"><strong>Economic Role:</strong> Significant contributor to state economy</p>
                    <p style="margin: 8px 0;"><strong>Food Security:</strong> Important for state and national food supply</p>
                </div>
            </div>
            
            <h4 style="color: #16a32a; margin-bottom: 10px;">🚜 KEY ADVANTAGES:</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div>✅ Diverse agro-climatic zones</div>
                <div>✅ Traditional + modern farming techniques</div>
                <div>✅ Good market linkages</div>
                <div>✅ Government agricultural support</div>
            </div>
        </div>
    </div>
    """

    return html_response


def get_crops_for_location(lat, lng, location_info):
    """Get enhanced crops information based on Indian state/region"""

    # Check if location is in India
    if location_info["country"] != "India":
        return f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #e0e0e0;">
            <div style="background: linear-gradient(135deg, #ff6b35, #f7931e); padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
                <h2 style="color: white; margin: 0;">🌍 GLOBAL LOCATION DETECTED</h2>
                <p style="color: #f0f0f0; margin: 10px 0 0 0;">📍 {location_info["full_location"]}</p>
            </div>
            
            <div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; border: 1px solid #333;">
                <p style="color: #ff6b35; font-weight: bold;">❗ SYSTEM SCOPE: This system provides detailed crop information specifically for Indian states.</p>
                
                <h3 style="color: #16a32a;">🌾 GENERAL CROP GUIDANCE FOR GLOBAL LOCATIONS:</h3>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                    <div style="background-color: #2a2a2a; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #16a32a;">🌡️ Climate-Based Crops:</h4>
                        <p><strong>Tropical:</strong> Rice, Sugarcane, Banana, Coconut</p>
                        <p><strong>Temperate:</strong> Wheat, Barley, Apples, Potatoes</p>
                        <p><strong>Arid:</strong> Millets, Sorghum, Cotton, Dates</p>
                    </div>
                    
                    <div style="background-color: #2a2a2a; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #16a32a;">🌱 Soil-Based Crops:</h4>
                        <p><strong>Alluvial:</strong> Rice, Wheat, Sugarcane</p>
                        <p><strong>Black Cotton:</strong> Cotton, Sorghum, Pulses</p>
                        <p><strong>Sandy:</strong> Groundnut, Watermelon, Pulses</p>
                    </div>
                </div>
                
                <p style="text-align: center; margin-top: 20px; color: #16a32a; font-weight: bold;">
                    For detailed crop recommendations, please select a location within India.
                </p>
            </div>
        </div>
        """

    # Get state/region name
    state_name = location_info["region"]

    # Check if state exists in our enhanced data
    if state_name in INDIAN_CROPS_DATA:
        state_data = INDIAN_CROPS_DATA[state_name]
        return create_enhanced_crop_response(state_name, location_info, state_data)

    else:
        # Enhanced generic response for other Indian states
        return f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #e0e0e0;">
            <div style="background: linear-gradient(135deg, #16a32a, #128724); padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
                <h2 style="color: white; margin: 0;">🌍 INDIAN LOCATION DETECTED</h2>
                <p style="color: #f0f0f0; margin: 10px 0 0 0;">📍 {location_info["full_location"]}</p>
            </div>
            
            <div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; border: 1px solid #333;">
                <h3 style="color: #16a32a; margin-top: 0;">📊 GENERAL INDIAN AGRICULTURE PATTERN</h3>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div style="background-color: #2a2a2a; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #16a32a;">🌾 CEREALS</h4>
                        <p>Rice, Wheat, Maize - basic food grains</p>
                    </div>
                    
                    <div style="background-color: #2a2a2a; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #16a32a;">🫘 PULSES</h4>
                        <p>Tur, Gram, Moong - protein sources</p>
                    </div>
                    
                    <div style="background-color: #2a2a2a; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #16a32a;">🛢️ OILSEEDS</h4>
                        <p>Groundnut, Mustard, Sesame - oil extraction</p>
                    </div>
                    
                    <div style="background-color: #2a2a2a; padding: 15px; border-radius: 8px;">
                        <h4 style="color: #16a32a;">💰 CASH CROPS</h4>
                        <p>Cotton, Sugarcane - commercial cultivation</p>
                    </div>
                </div>
                
                <p style="text-align: center; margin-top: 20px; color: #16a32a; font-weight: bold;">
                    For detailed state-specific information, our database covers major Indian states with comprehensive crop analysis.
                </p>
            </div>
        </div>
        """


@app.route("/")
def index():
    return render_template("map.html")


@app.route("/predict_crop", methods=["POST"])
def predict_crop():
    try:
        data = request.get_json()
        if not data or "polygon_coords" not in data:
            return jsonify({"error": "No polygon coordinates provided"}), 400

        polygon_coords = data["polygon_coords"]
        if not polygon_coords or len(polygon_coords) == 0:
            return jsonify({"error": "Empty polygon coordinates"}), 400

        # Get center coordinates
        center_lat = sum(coord[0] for coord in polygon_coords) / len(polygon_coords)
        center_lng = sum(coord[1] for coord in polygon_coords) / len(polygon_coords)

        print(f"Location: lat={center_lat:.4f}, lng={center_lng:.4f}")

        # Get location details
        location_info = get_location_info(center_lat, center_lng)
        print(f"Location: {location_info['full_location']}")

        # Get enhanced crops information
        crops_response = get_crops_for_location(center_lat, center_lng, location_info)

        return jsonify(
            {
                "location": location_info["full_location"],
                "ai_response": crops_response,
                "coordinates": f"{center_lat:.4f}, {center_lng:.4f}",
                "status": "success",
            }
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/health")
def health_check():
    return jsonify(
        {
            "status": "healthy",
            "service": "Enhanced Indian Agricultural Information System",
        }
    )


if __name__ == "__main__":
    print("🚀 Starting Enhanced Indian Agricultural Information System...")
    print("🌾 Get comprehensive crop analysis for Indian states!")
    print(f"🌐 Server running on http://localhost:5000")

    app.run(debug=True, host="127.0.0.1", port=5000)
