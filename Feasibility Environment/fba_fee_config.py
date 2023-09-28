# fee_config.py


# US-specific fee dictionary
FBA_SIZES_US = {
    'size_tiers': {
        'Small standard-size': {'unit_weight': 1, 'unit': 'lb', 'longest_side': 15, 'median_side': 12, 'shortest_side': 0.75, 'sides_unit': 'inches'},
        'Large standard-size': {'unit_weight': 20, 'unit': 'lb', 'longest_side': 18, 'median_side': 14, 'shortest_side': 8, 'sides_unit': 'inches'},
        'Small oversize': {'unit_weight': 70, 'unit': 'lb', 'longest_side': 60, 'median_side': 30, 'sides_unit': 'inches'},
        'Medium oversize': {'unit_weight': 150, 'unit': 'lb', 'longest_side': 108, 'sides_unit': 'inches'},
        'Large oversize': {'unit_weight': 150, 'unit': 'lb', 'longest_side': 108, 'sides_unit': 'inches'},
        'Special oversize': {'unit_weight': 'Over 150', 'unit': 'lb', 'longest_side': 'Over 108', 'sides_unit': 'inches'}
    },
}

FBA_FEES_US = {
    'Small standard-size': [
        {'min_weight': 0, 'max_weight': 0.25, 'fee': 3.22},
        {'min_weight': 0.25, 'max_weight': 0.5, 'fee': 3.40},
        {'min_weight': 0.5, 'max_weight': 0.75, 'fee': 3.58},
        {'min_weight': 0.75, 'max_weight': 1, 'fee': 3.77}
    ],
    'Large standard-size': [
        {'min_weight': 0, 'max_weight': 0.25, 'fee': 3.86},
        {'min_weight': 0.25, 'max_weight': 0.5, 'fee': 4.08},
        {'min_weight': 0.5, 'max_weight': 0.75, 'fee': 4.24},
        {'min_weight': 0.75, 'max_weight': 1, 'fee': 4.75},
        {'min_weight': 1, 'max_weight': 1.5, 'fee': 5.40},
        {'min_weight': 1.5, 'max_weight': 2, 'fee': 5.69},
        {'min_weight': 2, 'max_weight': 2.5, 'fee': 6.10},
        {'min_weight': 2.5, 'max_weight': 3, 'fee': 6.39},
        {'min_weight': 3, 'max_weight': 20, 'fee': 7.17, 'additional_fee': 0.16, 'additional_unit': 'per-halflb'}
    ],
    'Small oversize': [
        {'min_weight': 0, 'max_weight': 75, 'fee': 9.73, 'additional_fee': 0.42, 'additional_unit': 'per-lb'}
    ],
    'Medium oversize': [
        {'min_weight': 0, 'max_weight': 150, 'fee': 19.05, 'additional_fee': 0.42, 'additional_unit': 'per-lb'}
    ],
    'Large oversize': [
        {'min_weight': 0, 'max_weight': 150, 'fee': 89.98, 'additional_fee': 0.83, 'additional_unit': 'per-lb'}
    ],
    'Special oversize': [
        {'min_weight': 150, 'max_weight': None, 'fee': 158.49, 'additional_fee': 0.83, 'additional_unit': 'per-lb'}
    ]    
}

FBA_FEES_US_LOWPRICE = {
    'Small standard-size': [
        {'min_weight': 0, 'max_weight': 0.25, 'fee': 2.45},
        {'min_weight': 0.25, 'max_weight': 0.5, 'fee': 2.63},
        {'min_weight': 0.5, 'max_weight': 0.75, 'fee': 2.81},
        {'min_weight': 0.75, 'max_weight': 1, 'fee': 3.00}
    ],
    'Large standard-size': [
        {'min_weight': 0, 'max_weight': 0.25, 'fee': 3.09},
        {'min_weight': 0.25, 'max_weight': 0.5, 'fee': 3.31},
        {'min_weight': 0.5, 'max_weight': 0.75, 'fee': 3.47},
        {'min_weight': 0.75, 'max_weight': 1, 'fee': 3.98},
        {'min_weight': 1, 'max_weight': 1.5, 'fee': 4.63},
        {'min_weight': 1.5, 'max_weight': 2, 'fee': 4.92},
        {'min_weight': 2, 'max_weight': 2.5, 'fee': 5.33},
        {'min_weight': 2.5, 'max_weight': 3, 'fee': 5.62},
        {'min_weight': 3, 'max_weight': 20, 'fee': 6.40, 'additional_fee': 0.16, 'additional_unit': 'per-halflb'}
    ],
    'Small oversize': [
        {'min_weight': 0, 'max_weight': 70, 'fee': 8.96, 'additional_fee': 0.42, 'additional_unit': 'per-lb'}
    ],
    'Medium oversize': [
        {'min_weight': 0, 'max_weight': 150, 'fee': 18.28, 'additional_fee': 0.42, 'additional_unit': 'per-lb'}
    ],
    'Large oversize': [
        {'min_weight': 0, 'max_weight': 150, 'fee': 89.21, 'additional_fee': 0.83, 'additional_unit': 'per-lb'}
    ],
    'Special oversize': [
        {'min_weight': 150, 'max_weight': None, 'fee': 157.72, 'additional_fee': 0.83, 'additional_unit': 'per-lb'}
    ]    
}

# Canada-specific fee dictionary
FBA_SIZES_CA = {
    'size_tiers': {
        'Envelope': {'unit_weight': 500, 'unit': 'g', 'longest_side': 38, 'median_side': 27, 'shortest_side': 2, 'sides_unit': 'cm'},
        'Standard-Size': {'unit_weight': 9000, 'unit': 'g', 'longest_side': 45, 'median_side': 35, 'shortest_side': 20, 'sides_unit': 'cm'},
        'Small Oversize': {'unit_weight': 32000, 'unit': 'g', 'longest_side': 152, 'median_side': 76, 'sides_unit': 'cm', 'length_girth': 330, 'girth_unit': 'cm'},
        'Medium Oversize': {'unit_weight': 68000, 'unit': 'g', 'longest_side': 270, 'sides_unit': 'cm', 'length_girth': 330, 'girth_unit': 'cm'},
        'Large Oversize': {'unit_weight': 68000, 'unit': 'g', 'longest_side': 270, 'sides_unit': 'cm', 'length_girth': 419, 'girth_unit': 'cm'},
        'Special Oversize': {'unit_weight': 'Over 68000', 'unit': 'g', 'longest_side': 'Over 270', 'sides_unit': 'cm', 'length_girth': 'Over 419', 'girth_unit': 'cm'}
    }
}

FBA_FEES_CA = {
    
        'Envelope': [
            {'min_weight': 0, 'max_weight': 100, 'fee': 4.32},
            {'min_weight': 100, 'max_weight': 200, 'fee': 4.65},
            {'min_weight': 200, 'max_weight': 300, 'fee': 4.99},
            {'min_weight': 300, 'max_weight': 400, 'fee': 5.28},
            {'min_weight': 400, 'max_weight': 500, 'fee': 5.45}
        ],
        'Standard-Size': [
            {'min_weight': 0, 'max_weight': 100, 'fee': 5.92},
            {'min_weight': 100, 'max_weight': 200, 'fee': 6.12},
            {'min_weight': 200, 'max_weight': 300, 'fee': 6.36},
            {'min_weight': 300, 'max_weight': 400, 'fee': 6.69},
            {'min_weight': 400, 'max_weight': 500, 'fee': 7.13},
            {'min_weight': 500, 'max_weight': 600, 'fee': 7.38},
            {'min_weight': 600, 'max_weight': 700, 'fee': 7.62},
            {'min_weight': 700, 'max_weight': 800, 'fee': 7.80},
            {'min_weight': 800, 'max_weight': 900, 'fee': 8.04},
            {'min_weight': 900, 'max_weight': 1000, 'fee': 8.23},
            {'min_weight': 1000, 'max_weight': 1100, 'fee': 8.40},
            {'min_weight': 1100, 'max_weight': 1200, 'fee': 8.62},
            {'min_weight': 1200, 'max_weight': 1300, 'fee': 8.79},
            {'min_weight': 1300, 'max_weight': 1400, 'fee': 9.01},
            {'min_weight': 1400, 'max_weight': 1500, 'fee': 9.20},
            {'min_weight': 1500, 'max_weight': 9000, 'fee': 9.74, 'additional_fee': 0.09, 'additional_unit': 'per-100gram'}
        ],
        'Small Oversize': [
            {'min_weight': 0, 'max_weight': 500, 'fee': 13.75},
            {'min_weight': 500, 'max_weight': None, 'fee': 13.75, 'additional_fee': 0.46, 'additional_unit': 'per-500gram'}
        ],
        'Medium Oversize': [
            {'min_weight': 0, 'max_weight': 500, 'fee': 33.24},
            {'min_weight': 500, 'max_weight': None, 'fee': 33.24, 'additional_fee': 0.52, 'additional_unit': 'per-500gram'}
        ],
        'Large Oversize': [
            {'min_weight': 0, 'max_weight': 500, 'fee': 72.74},
            {'min_weight': 500, 'max_weight': None, 'fee': 72.74, 'additional_fee': 0.58, 'additional_unit': 'per-500gram'}
        ],
        'Special Oversize': [
            {'min_weight': 0, 'max_weight': 500, 'fee': 141.65},
            {'min_weight': 500, 'max_weight': None, 'fee': 141.65, 'additional_fee': 0.58, 'additional_unit': 'per-500gram'}
        ]
    
}
# Japan-specific fee dictionary
FBA_SIZES_JAP = {
    'size_tiers': {
        'Small': {'unit_weight': 250, 'unit': 'g', 'longest_side': 25, 'median_side': 18, 'shortest_side': 2, 'sides_unit': 'cm', 'dimension': 45},
        'Standard': {'unit_weight': 9000, 'unit': 'g', 'longest_side': 45, 'median_side': 35, 'shortest_side': 20, 'sides_unit': 'cm', 'dimension': 100},
        'Oversize': {'unit_weight': 40000, 'unit': 'g', 'sides_unit': 'cm', 'dimension': 200},
        'Supersize': {'unit_weight': 50000, 'unit': 'g', 'sides_unit': 'cm', 'dimension': 260}
    }
}
#japan fees are wrong, check later
"""
FBA_FEES_JAP = {
    'fees': {
        'Small standard-size': [
            {'min_weight': 0, 'max_weight': 4, 'fee': 3.22},
            {'min_weight': 4, 'max_weight': 8, 'fee': 3.40},
            {'min_weight': 8, 'max_weight': 12, 'fee': 3.58},
            {'min_weight': 12, 'max_weight': 16, 'fee': 3.77}
        ],
        'Large standard-size': [
            {'min_weight': 0, 'max_weight': 4, 'fee': 3.86},
            {'min_weight': 4, 'max_weight': 8, 'fee': 4.08},
            {'min_weight': 8, 'max_weight': 12, 'fee': 4.24},
            {'min_weight': 12, 'max_weight': 16, 'fee': 4.75},
            {'min_weight': 16, 'max_weight': 24, 'fee': 5.40},
            {'min_weight': 24, 'max_weight': 32, 'fee': 5.69},
            {'min_weight': 32, 'max_weight': 40, 'fee': 6.10},
            {'min_weight': 40, 'max_weight': 48, 'fee': 6.39},
            {'min_weight': 48, 'max_weight': 320, 'fee': 7.17 'additional_fee': 0.16, 'additional_unit': 'per-halflb'}
        ],
        'Small oversize': [
            {'min_weight': 0, 'max_weight': 1120, 'fee': 9.73 'additional_fee': 0.42, 'additional_unit': 'per-lb'}
        ],
        'Medium oversize': [
            {'min_weight': 0, 'max_weight': 2400, 'fee': 19.05 'additional_fee': 0.42, 'additional_unit': 'per-lb'}
        ],
        'Large oversize': [
            {'min_weight': 0, 'max_weight': 2400,  'fee': 89.98 'additional_fee': 0.83, 'additional_unit': 'per-lb'}
        ],
        'Special oversize': [
            {'min_weight': 2400, 'max_weight': None, 'fee': '158.49 + $0.83/lb above first 90 lb'}
        ]
    }
}
"""
# EU-specific fee dictionary
FBA_SIZES_EU = {
    'size_tiers': {
        'Small envelope': {'unit_weight': 80, 'unit': 'g', 'longest_side': 20, 'median_side': 15, 'shortest_side': 1, 'sides_unit': 'cm'},
        'Standard envelope': {'unit_weight': 460, 'unit': 'g', 'longest_side': 33, 'median_side': 23, 'shortest_side': 2.5, 'sides_unit': 'cm'},
        'Large envelope': {'unit_weight': 960, 'unit': 'g', 'longest_side': 33, 'median_side': 23, 'shortest_side': 4, 'sides_unit': 'cm'},
        'Extra-large envelope': {'unit_weight': 960, 'unit': 'g', 'longest_side': 33, 'median_side': 23, 'shortest_side': 6, 'sides_unit': 'cm'},
        'Small parcel': {'unit_weight': 3900, 'unit': 'g', 'longest_side': 35, 'median_side': 25, 'shortest_side': 12, 'sides_unit': 'cm'},
        'Standard parcel': {'unit_weight': 11900, 'unit': 'g', 'longest_side': 45, 'median_side': 34, 'shortest_side': 26, 'sides_unit': 'cm'},
        'Small oversize': {'unit_weight': 1760, 'unit': 'g', 'longest_side': 61, 'median_side': 46, 'shortest_side': 46, 'sides_unit': 'cm'},
        'Standard oversize': {'unit_weight': 2976, 'unit': 'g', 'longest_side': 120, 'median_side': 60, 'shortest_side': 60, 'sides_unit': 'cm'},
        'Large oversize': {'unit_weight': 3150, 'unit': 'g', 'longest_side': 'Over 120', 'median_side': 'Over 60', 'shortest_side': 'Over 60', 'sides_unit': 'cm'},
        'Special oversize': {'unit_weight': 'Over 31.5', 'unit': 'g', 'longest_side': 'Over 175', 'sides_unit': 'cm', 'girth': 'Over 360'}
    }
}

FBA_FEES_UK = {
    'Small envelope': [
        {'max_weight': 80, 'fee': 1.71}
    ],
    'Standard envelope': [
        {'max_weight': 60, 'fee': 1.81},
        {'max_weight': 210, 'fee': 1.98},
        {'max_weight': 460, 'fee': 2.11}
    ],
    'Large envelope': [
        {'max_weight': 960, 'fee': 2.58}
    ],
    'Extra-large envelope': [
        {'max_weight': 960, 'fee': 2.79}
    ],
    'Small parcel': [
        {'max_weight': 150, 'fee': 2.79},
        {'max_weight': 400, 'fee': 2.81},
        {'max_weight': 900, 'fee': 2.85},
        {'max_weight': 1400, 'fee': 3.02},
        {'max_weight': 1900, 'fee': 3.31},
        {'max_weight': 3900, 'fee': 5.30}
    ],
    'Standard parcel': [
        {'max_weight': 150, 'fee': 2.81},
        {'max_weight': 400, 'fee': 2.92},
        {'max_weight': 900, 'fee': 3.15},
        {'max_weight': 1400, 'fee': 3.36},
        {'max_weight': 1900, 'fee': 3.68},
        {'max_weight': 2900, 'fee': 5.38},
        {'max_weight': 3900, 'fee': 5.68},
        {'max_weight': 5900, 'fee': 5.84},
        {'max_weight': 8900, 'fee': 6.66},
        {'max_weight': 11900, 'fee': 7.04}
    ],
    'Small oversize': [
        {'max_weight': 760, 'fee': 5.06},
        {'max_weight': 1260, 'fee': 5.87},
        {'max_weight': 1760, 'fee': 6.05},
        {'max_weight': float('inf'), 'fee': 0.01}  # For weights above 1.76 kg
    ],
    'Standard oversize': [
        {'max_weight': 760, 'fee': 6.01},
        {'max_weight': 1760, 'fee': 6.35},
        {'max_weight': 2760, 'fee': 6.50},
        {'max_weight': 3760, 'fee': 6.53},
        {'max_weight': 4760, 'fee': 6.56},
        {'max_weight': 9760, 'fee': 7.85},
        {'max_weight': 14760, 'fee': 8.40},
        {'max_weight': 19760, 'fee': 8.80},
        {'max_weight': 29760, 'fee': 9.77},
        {'max_weight': float('inf'), 'fee': 0.01}  # For weights above 29.76 kg
    ],
    'Large oversize': [
        {'max_weight': 4760, 'fee': 10.91},
        {'max_weight': 9760, 'fee': 11.93},
        {'max_weight': 14760, 'fee': 12.60},
        {'max_weight': 19760, 'fee': 13.20},
        {'max_weight': 31500, 'fee': 14.40},
        {'max_weight': float('inf'), 'fee': 0.01}  # For weights above 31.5 kg
    ],
    'Special oversize': [
        {'max_weight': 20000, 'fee': 15.43},
        {'max_weight': 30000, 'fee': 18.48},
        {'max_weight': 40000, 'fee': 19.16},
        {'max_weight': 50000, 'fee': 42.98},
        {'max_weight': 60000, 'fee': 44.25},
        {'max_weight': float('inf'), 'fee': 0.39}  # For weights above 60 kg
    ]
}

FBA_FEES_DE = {
    'Small envelope': [
        {'max_weight': 80, 'fee': 1.90}
    ],
    'Standard envelope': [
        {'max_weight': 60, 'fee': 2.09},
        {'max_weight': 210, 'fee': 2.23},
        {'max_weight': 460, 'fee': 2.39}
    ],
    'Large envelope': [
        {'max_weight': 960, 'fee': 2.74}
    ],
    'Extra-large envelope': [
        {'max_weight': 960, 'fee': 3.12}
    ],
    'Small parcel': [
        {'max_weight': 150, 'fee': 3.12},
        {'max_weight': 400, 'fee': 3.32},
        {'max_weight': 900, 'fee': 3.70},
        {'max_weight': 1400, 'fee': 4.37},
        {'max_weight': 1900, 'fee': 4.76},
        {'max_weight': 3900, 'fee': 5.97}
    ],
    'Standard parcel': [
        {'max_weight': 150, 'fee': 3.22},
        {'max_weight': 400, 'fee': 3.63},
        {'max_weight': 900, 'fee': 4.11},
        {'max_weight': 1400, 'fee': 4.84},
        {'max_weight': 1900, 'fee': 5.32},
        {'max_weight': 2900, 'fee': 5.98},
        {'max_weight': 3900, 'fee': 6.55},
        {'max_weight': 5900, 'fee': 6.89},
        {'max_weight': 8900, 'fee': 7.44},
        {'max_weight': 11900, 'fee': 7.73}
    ],
    'Small oversize': [
        {'max_weight': 760, 'fee': 6.39},
        {'max_weight': 1260, 'fee': 6.41},
        {'max_weight': 1760, 'fee': 6.43},
        {'max_weight': float('inf'), 'fee': 0.01}  # For weights above 1.76 kg
    ],
    'Standard oversize': [
        {'max_weight': 760, 'fee': 6.46},
        {'max_weight': 1760, 'fee': 6.77},
        {'max_weight': 2760, 'fee': 7.59},
        {'max_weight': 3760, 'fee': 7.65},
        {'max_weight': 4760, 'fee': 7.68},
        {'max_weight': 9760, 'fee': 8.07},
        {'max_weight': 14760, 'fee': 8.79},
        {'max_weight': 19760, 'fee': 9.34},
        {'max_weight': 29760, 'fee': 10.59},
        {'max_weight': float('inf'), 'fee': 0.01}  # For weights above 29.76 kg
    ],
    'Large oversize': [
        {'max_weight': 4760, 'fee': 9.26},
        {'max_weight': 9760, 'fee': 10.66},
        {'max_weight': 14760, 'fee': 11.00},
        {'max_weight': 19760, 'fee': 11.63},
        {'max_weight': 31500, 'fee': 12.90},
        {'max_weight': float('inf'), 'fee': 0.01}  # For weights above 31.5 kg
    ],
    'Special oversize': [
        {'max_weight': 20000, 'fee': 19.98},
        {'max_weight': 30000, 'fee': 27.16},
        {'max_weight': 40000, 'fee': 28.46},
        {'max_weight': 50000, 'fee': 59.97},
        {'max_weight': 60000, 'fee': 61.17},
        {'max_weight': float('inf'), 'fee': 0.38}  # For weights above 60 kg
    ]
}

FBA_FEES_FR = {
    'Small envelope': [
        {'max_weight': 80, 'fee': 2.70}
    ],
    'Standard envelope': [
        {'max_weight': 60, 'fee': 2.80},
        {'max_weight': 210, 'fee': 3.34},
        {'max_weight': 460, 'fee': 3.82}
    ],
    'Large envelope': [
        {'max_weight': 960, 'fee': 4.45}
    ],
    'Extra-large envelope': [
        {'max_weight': 960, 'fee': 4.79}
    ],
    'Small parcel': [
        {'max_weight': 150, 'fee': 4.79},
        {'max_weight': 400, 'fee': 5.18},
        {'max_weight': 900, 'fee': 5.92},
        {'max_weight': 1400, 'fee': 6.16},
        {'max_weight': 1900, 'fee': 6.24},
        {'max_weight': 3900, 'fee': 9.55}
    ],
    'Standard parcel': [
        {'max_weight': 150, 'fee': 4.84},
        {'max_weight': 400, 'fee': 5.50},
        {'max_weight': 900, 'fee': 6.40},
        {'max_weight': 1400, 'fee': 6.77},
        {'max_weight': 1900, 'fee': 6.97},
        {'max_weight': 2900, 'fee': 9.55},
        {'max_weight': 3900, 'fee': 9.74},
        {'max_weight': 5900, 'fee': 10.22},
        {'max_weight': 8900, 'fee': 11.12},
        {'max_weight': 11900, 'fee': 11.65}
    ],
    'Small oversize': [
        {'max_weight': 760, 'fee': 9.36},
        {'max_weight': 1260, 'fee': 9.75},
        {'max_weight': 1760, 'fee': 10.39},
        {'max_weight': float('inf'), 'fee': 0.01}  # For weights above 1.76 kg
    ],
    'Standard oversize': [
        {'max_weight': 760, 'fee': 9.37},
        {'max_weight': 1760, 'fee': 10.57},
        {'max_weight': 2760, 'fee': 11.10},
        {'max_weight': 3760, 'fee': 11.56},
        {'max_weight': 4760, 'fee': 11.64},
        {'max_weight': 9760, 'fee': 12.54},
        {'max_weight': 14760, 'fee': 13.46},
        {'max_weight': 19760, 'fee': 14.14},
        {'max_weight': 29760, 'fee': 15.75},
        {'max_weight': float('inf'), 'fee': 0.01}  # For weights above 29.76 kg
    ],
    'Large oversize': [
        {'max_weight': 4760, 'fee': 16.91},
        {'max_weight': 9760, 'fee': 20.60},
        {'max_weight': 14760, 'fee': 21.69},
        {'max_weight': 19760, 'fee': 22.76},
        {'max_weight': 31500, 'fee': 25.45},
        {'max_weight': float('inf'), 'fee': 0.01}  # For weights above 31.5 kg
    ],
    'Special oversize': [
        {'max_weight': 20000, 'fee': 23.95},
        {'max_weight': 30000, 'fee': 30.88},
        {'max_weight': 40000, 'fee': 31.76},
        {'max_weight': 50000, 'fee': 54.04},
        {'max_weight': 60000, 'fee': 55.63},
        {'max_weight': float('inf'), 'fee': 0.42}  # For weights above 60 kg
    ]
}

FBA_FEES_IT = {
    'Small envelope': [
        {'max_weight': 80, 'fee': 3.11}
    ],
    'Standard envelope': [
        {'max_weight': 60, 'fee': 3.24},
        {'max_weight': 210, 'fee': 3.37},
        {'max_weight': 460, 'fee': 3.60}
    ],
    'Large envelope': [
        {'max_weight': 960, 'fee': 3.90}
    ],
    'Extra-large envelope': [
        {'max_weight': 960, 'fee': 4.13}
    ],
    'Small parcel': [
        {'max_weight': 150, 'fee': 4.13},
        {'max_weight': 400, 'fee': 4.44},
        {'max_weight': 900, 'fee': 4.97},
        {'max_weight': 1400, 'fee': 5.59},
        {'max_weight': 1900, 'fee': 5.84},
        {'max_weight': 3900, 'fee': 7.70}
    ],
    'Standard parcel': [
        {'max_weight': 150, 'fee': 4.50},
        {'max_weight': 400, 'fee': 5.08},
        {'max_weight': 900, 'fee': 5.78},
        {'max_weight': 1400, 'fee': 6.52},
        {'max_weight': 1900, 'fee': 6.78},
        {'max_weight': 2900, 'fee': 7.72},
        {'max_weight': 3900, 'fee': 8.01},
        {'max_weight': 5900, 'fee': 9.14},
        {'max_weight': 8900, 'fee': 10.13},
        {'max_weight': 11900, 'fee': 10.87}
    ],
    'Small oversize': [
        {'max_weight': 760, 'fee': 9.24},
        {'max_weight': 1260, 'fee': 9.72},
        {'max_weight': 1760, 'fee': 9.86},
        {'max_weight': None, 'fee': 9.86, 'additional_fee_per_kg': 0.01, }
    ],
    'Standard oversize': [
        {'max_weight': 760, 'fee': 9.79},
        {'max_weight': 1760, 'fee': 9.94},
        {'max_weight': 2760, 'fee': 9.96},
        {'max_weight': None, 'fee': 9.96, 'additional_fee_per_kg': 0.01}
    ],
    'Large oversize': [
        {'max_weight': 4760, 'fee': 10.84},
        {'max_weight': 9760, 'fee': 12.33},
        {'max_weight': None, 'fee': 12.33, 'additional_fee_per_kg': 0.01}
    ],
    'Special oversize': [
        {'max_weight': 20000, 'fee': 17.41},
        {'max_weight': None, 'fee': 17.41, 'additional_fee_per_kg': 0.01}
    ]
}

FBA_FEES_ES = {
    'Small envelope': [
        {'max_weight': 80, 'fee': 2.53}
    ],
    'Standard envelope': [
        {'max_weight': 60, 'fee': 2.84},
        {'max_weight': 210, 'fee': 3.18},
        {'max_weight': 460, 'fee': 3.42}
    ],
    'Large envelope': [
        {'max_weight': 960, 'fee': 3.57}
    ],
    'Extra-large envelope': [
        {'max_weight': 960, 'fee': 3.80}
    ],
    'Small parcel': [
        {'max_weight': 150, 'fee': 3.80},
        {'max_weight': 400, 'fee': 4.03},
        {'max_weight': 900, 'fee': 4.26},
        {'max_weight': 1400, 'fee': 4.75},
        {'max_weight': 1900, 'fee': 4.82},
        {'max_weight': 3900, 'fee': 6.27}
    ],
    'Standard parcel': [
        {'max_weight': 150, 'fee': 3.82},
        {'max_weight': 400, 'fee': 4.39},
        {'max_weight': 900, 'fee': 4.73},
        {'max_weight': 1400, 'fee': 5.44},
        {'max_weight': 1900, 'fee': 5.54},
        {'max_weight': 2900, 'fee': 6.29},
        {'max_weight': 3900, 'fee': 7.70},
        {'max_weight': 5900, 'fee': 7.95},
        {'max_weight': 8900, 'fee': 7.97},
        {'max_weight': 11900, 'fee': 7.98}
    ],
    'Small oversize': [
        {'max_weight': 760, 'fee': 7.32},
        {'max_weight': 1260, 'fee': 8.03},
        {'max_weight': 1760, 'fee': 8.13},
        {'max_weight': None, 'fee': 8.13, 'additional_fee_per_kg': 0.01}
    ],
    'Standard oversize': [
        {'max_weight': 760, 'fee': 7.37},
        {'max_weight': 1760, 'fee': 8.16},
        {'max_weight': 2760, 'fee': 8.95},
        {'max_weight': None, 'fee': 8.95, 'additional_fee_per_kg': 0.01}
    ],
    'Large oversize': [
        {'max_weight': 4760, 'fee': 11.19},
        {'max_weight': 9760, 'fee': 15.01},
        {'max_weight': None, 'fee': 15.01, 'additional_fee_per_kg': 0.01}
    ],
    'Special oversize': [
        {'max_weight': 20000, 'fee': 17.75},
        {'max_weight': None, 'fee': 17.75, 'additional_fee_per_kg': 0.01}
    ]
}

FBA_FEES_NL = {
    'Small envelope': [
        {'max_weight': 80, 'fee': 1.77}
    ],
    'Standard envelope': [
        {'max_weight': 60, 'fee': 1.92},
        {'max_weight': 210, 'fee': 2.11},
        {'max_weight': 460, 'fee': 2.24}
    ],
    'Large envelope': [
        {'max_weight': 960, 'fee': 2.71}
    ],
    'Extra-large envelope': [
        {'max_weight': 960, 'fee': 2.97}
    ],
    'Small parcel': [
        {'max_weight': 150, 'fee': 2.97},
        {'max_weight': 400, 'fee': 2.99},
        {'max_weight': 900, 'fee': 3.48},
        {'max_weight': 1400, 'fee': 4.09},
        {'max_weight': 1900, 'fee': 4.38},
        {'max_weight': 3900, 'fee': 5.68}
    ],
    'Standard parcel': [
        {'max_weight': 150, 'fee': 2.98},
        {'max_weight': 400, 'fee': 3.27},
        {'max_weight': 900, 'fee': 3.76},
        {'max_weight': 1400, 'fee': 4.48},
        {'max_weight': 1900, 'fee': 4.91},
        {'max_weight': 2900, 'fee': 5.69},
        {'max_weight': 3900, 'fee': 5.72},
        {'max_weight': 5900, 'fee': 5.94},
        {'max_weight': 8900, 'fee': 6.26},
        {'max_weight': 11900, 'fee': 6.67}
    ],
    'Small oversize': [
        {'max_weight': 760, 'fee': 6.68},
        {'max_weight': 1260, 'fee': 6.85},
        {'max_weight': 1760, 'fee': 6.92},
        {'max_weight': None, 'fee': 6.92, 'additional_fee_per_kg': 0.01}
    ],
    'Standard oversize': [
        {'max_weight': 760, 'fee': 6.74},
        {'max_weight': 1760, 'fee': 7.04},
        {'max_weight': 2760, 'fee': 8.22},
        {'max_weight': None, 'fee': 8.22, 'additional_fee_per_kg': 0.01}
    ],
    'Large oversize': [
        {'max_weight': 4760, 'fee': 9.58},
        {'max_weight': 9760, 'fee': 11.05},
        {'max_weight': None, 'fee': 11.05, 'additional_fee_per_kg': 0.01}
    ],
    'Special oversize': [
        {'max_weight': 20000, 'fee': 17.75},
        {'max_weight': None, 'fee': 17.75, 'additional_fee_per_kg': 0.01}
    ]
}


FBA_FEES_SE = {
    'Small standard': [
        {'max_weight': 100, 'fee': 27.61},
        {'max_weight': 200, 'fee': 28.36},
        {'max_weight': 300, 'fee': 29.60},
        {'max_weight': 400, 'fee': 34.09},
        {'max_weight': 500, 'fee': 35.43},
        {'max_weight': 600, 'fee': 40.14},
        {'max_weight': 700, 'fee': 42.05},
        {'max_weight': 800, 'fee': 42.63},
        {'max_weight': 900, 'fee': 43.90},
        {'max_weight': 1000, 'fee': 45.38},
        {'max_weight': 1100, 'fee': 54.03},
        {'max_weight': 1200, 'fee': 54.17},
        {'max_weight': None, 'fee': 54.17, 'additional_fee_per_kg': 0.16}
    ],
    'Large standard': [
        {'max_weight': 100, 'fee': 43.28},
        {'max_weight': 200, 'fee': 45.91},
        {'max_weight': 300, 'fee': 46.02},
        {'max_weight': 400, 'fee': 48.10},
        {'max_weight': 500, 'fee': 50.77},
        {'max_weight': 600, 'fee': 54.17},
        {'max_weight': 700, 'fee': 54.33},
        {'max_weight': 800, 'fee': 58.31},
        {'max_weight': 900, 'fee': 59.90},
        {'max_weight': 1000, 'fee': 78.41},
        {'max_weight': None, 'fee': 78.41, 'additional_fee_per_kg': 0.16}
    ],
    'Small oversize': [
        {'max_weight': 760, 'fee': 75.66},
        {'max_weight': 1260, 'fee': 77.58},
        {'max_weight': 1760, 'fee': 78.36},
        {'max_weight': None, 'fee': 78.36, 'additional_fee_per_kg': 0.1}
    ],
    'Standard oversize': [
        {'max_weight': 760, 'fee': 76.37},
        {'max_weight': 1760, 'fee': 79.71},
        {'max_weight': 2760, 'fee': 93.07},
        {'max_weight': None, 'fee': 93.07, 'additional_fee_per_kg': 0.1}
    ],
    'Large oversize': [
        {'max_weight': 4760, 'fee': 108.47},
        {'max_weight': 9760, 'fee': 125.13},
        {'max_weight': None, 'fee': 125.13, 'additional_fee_per_kg': 0.1}
    ],
    'Special oversize': [
        {'max_weight': 20000, 'fee': None},
        {'max_weight': None, 'fee': None, 'additional_fee_per_kg': 0.1}
    ]
}

FBA_FEES_PL = {
    'Small standard': [
        {'max_weight': 100, 'fee': 4.75},
        {'max_weight': 200, 'fee': 4.80},
        {'max_weight': 300, 'fee': 4.94},
        {'max_weight': 400, 'fee': 5.20},
        {'max_weight': 500, 'fee': 5.64},
        {'max_weight': 600, 'fee': 5.70},
        {'max_weight': 700, 'fee': 5.77},
        {'max_weight': 800, 'fee': 6.55},
        {'max_weight': 900, 'fee': 6.81},
        {'max_weight': 1000, 'fee': 6.82},
        {'max_weight': 1100, 'fee': 6.86},
        {'max_weight': 1200, 'fee': 6.95},
        {'max_weight': None, 'fee': 6.95, 'additional_fee_per_kg': 0.16}
    ],
    'Large standard': [
        {'max_weight': 100, 'fee': 5.79},
        {'max_weight': 200, 'fee': 5.83},
        {'max_weight': 300, 'fee': 6.61},
        {'max_weight': 400, 'fee': 6.88},
        {'max_weight': 500, 'fee': 6.89},
        {'max_weight': 600, 'fee': 6.95},
        {'max_weight': 700, 'fee': 7.00},
        {'max_weight': 800, 'fee': 7.08},
        {'max_weight': 900, 'fee': 7.46},
        {'max_weight': 1000, 'fee': 9.21},
        {'max_weight': None, 'fee': 9.21, 'additional_fee_per_kg': 0.16}
    ],
    'Small oversize': [
        {'max_weight': 760, 'fee': 8.05},
        {'max_weight': 1260, 'fee': 8.29},
        {'max_weight': 1760, 'fee': 8.40},
        {'max_weight': None, 'fee': 8.40, 'additional_fee_per_kg': 0.05}
    ],
    'Standard oversize': [
        {'max_weight': 760, 'fee': 8.05},
        {'max_weight': 1760, 'fee': 8.40},
        {'max_weight': 2760, 'fee': 9.81},
        {'max_weight': None, 'fee': 9.81, 'additional_fee_per_kg': 0.05}
    ],
    'Large oversize': [
        {'max_weight': 4760, 'fee': 10.74},
        {'max_weight': 9760, 'fee': 12.39},
        {'max_weight': None, 'fee': 12.39, 'additional_fee_per_kg': 0.05}
    ],
    'Special oversize': [
        {'max_weight': 20000, 'fee': None},
        {'max_weight': None, 'fee': None, 'additional_fee_per_kg': 0.05}
    ]
}
