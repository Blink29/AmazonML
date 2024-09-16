from logic.find_entity import findDepthEntity, findHeightEntity, findMaxWeightEntity, findVoltageEntity, findVolumeEntity, findWattageEntity, findWeightEntity, findWidthEntity

plural_rules = {
        'kilograms': 'kilogram',
        'grams': 'gram',
        'milligrams': 'milligram',
        'micrograms': 'microgram',
        'ounces': 'ounce',
        'pounds': 'pound',
        'tons': 'ton',
        'centimetres': 'centimetre',
        'metres': 'metre',
        'millimetres': 'millimetre',
        'inches': 'inch',
        'feet': 'foot',
        'yards': 'yard',
        'volts': 'volt',
        'watts': 'watt',
        'lbs': 'lb',
        'Ibs': 'lb',
    }

entity_name = {
    'width': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'depth': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'height': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'item_weight': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'maximum_weight_recommendation': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'voltage': {'kilovolt', 'millivolt', 'volt'},
    'wattage': {'kilowatt', 'watt'},
    'item_volume': {'centilitre', 'cubic foot', 'cubic inch', 'cup', 'decilitre', 'fluid ounce', 'gallon', 'imperial gallon', 'litre', 'microlitre', 'millilitre', 'pint', 'quart'}
}

short_entity = {
    'cm': 'centimetre', 'ft': 'foot', 'in': 'inch', 'm': 'metre',
    'mm': 'millimetre', 'yd': 'yard', 'gm': 'gram', 'kg': 'kilogram',
    'µg': 'microgram', 'mg': 'milligram', 'oz': 'ounce', 'lb': 'pound',
    'ton': 'ton', 'kV': 'kilovolt', 'mV': 'millivolt', 'V': 'volt',
    'KW': 'kilowatt', 'W': 'watt', 'cL': 'centilitre', 'ft³': 'cubic foot',
    'in³': 'cubic inch', 'c': 'cup', 'dL': 'decilitre', 'fl oz': 'fluid ounce',
    'gal': 'gallon', 'imp gal': 'imperial gallon', 'L': 'litre', 'µL': 'microlitre',
    'mL': 'millilitre', 'pt': 'pint', 'qt': 'quart'
}


entity_map = {
    'item_weight': findWeightEntity,
    'height': findHeightEntity,
    'width': findWidthEntity,
    'depth': findDepthEntity,
    'maximum_weight_recommendation': findMaxWeightEntity,
    'voltage': findVoltageEntity,
    'wattage': findWattageEntity,
    'item_volume': findVolumeEntity
}