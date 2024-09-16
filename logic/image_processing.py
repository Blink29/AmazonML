import pytesseract
import re
from PIL import Image
from logic.constants import short_entity, entity_name, plural_rules

def findText(image_path):
    from logic.utils import build_unit_regex, normalize_unit

    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    print('Tesseract raw text: ', text)
    text = text.replace(",", ".")
    # Replace plural forms with singular forms
    for plural, singular in plural_rules.items():
        text = text.replace(plural, singular)

    unit_pattern = build_unit_regex(entity_name, short_entity)
    pattern = re.compile(r'(\d+(?:\.\d+)?(?:\s*[-\s]+\s*\d+(?:\.\d+)?)?)\s*(%s)\b' % unit_pattern, re.IGNORECASE)

    matches = pattern.findall(text)

    print('Matches: ', matches)

    data_map = []
    for match in matches:
        number = match[0]
        
        # Replace connectors with a common delimiter
        number = re.split(r'[ \-\&to]', number)
        number = [num.strip() for num in number if num.strip()]
        
        unit = match[1].lower().strip()
        
        if len(number) > 1:
            for num in number:
                try:
                    data_map.append([unit, float(num)])
                except ValueError:
                    print(f"Failed to convert '{num}' to float")
        else:
            try:
                data_map.append([unit, float(number[0])])
            except ValueError:
                print(f"Failed to convert '{number[0]}' to float")
                
    print("Data map: ", data_map)

    return data_map
