import xml.etree.ElementTree as ET
import os
import re

def validate_trades(xml_file, output_file):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    with open(output_file, 'w') as f:
        for trade in root.findall('trade'):
            # Check if any field is empty and handle it gracefully
            trade_id = trade.find('trade_id').text or ""
            name = trade.find('trader/name').text or ""
            instrument = trade.find('instrument/name').text or ""
            quantity_str = trade.find('transaction_details/quantity').text or ""
            
            errors = []
            
            # Validate Trade ID if its alphanumeric 
            if not trade_id.isalnum():
                errors.append(f"Trade ID '{trade_id}' is not alphanumeric.")
            
            # Validate Name should be alphabetic and spaces allowed 
            name_clean = name.strip()
            if not re.match(r'^[A-Za-z\s]+$', name_clean):
                errors.append(f"Trader Name '{name_clean}' contains non-alphabet characters.")
                
            # Validate Instrument should be alphabetic, spaces and dots allowed
            instrument_clean = instrument.strip()
            if not re.match(r'^[A-Za-z\s\.]+$', instrument_clean):
                errors.append(f"Instrument Name '{instrument_clean}' contains non-alphabet characters.")
                
            # Validate Quantity (<= 1000)
            try:
                qty = float(quantity_str.strip())
                if qty > 1000:
                    errors.append(f"Quantity {qty} exceeds the maximum limit of 1000.")
            except ValueError:
                errors.append(f"Quantity '{quantity_str}' is empty or not a valid number.")
                
            # Log results
            if errors:
                f.write(f"Validation errors for Trade {trade_id}:\n")
                for error in errors:
                    f.write(f"  - {error}\n")
                f.write("\n")
            else:
                f.write(f"Trade {trade_id}: Passed validation.\n\n")
                
        f.write("Validation process completed.\n")

if __name__ == "__main__":
    validate_trades('source_trade.xml', 'output/validation.txt')