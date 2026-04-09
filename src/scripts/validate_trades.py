from lxml import etree
import os
import re

def validate_trades(xml_file, xslt_file, txt_output, html_output):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(txt_output), exist_ok=True)
    
    tree = etree.parse(xml_file)
    root = tree.getroot()
    
    with open(txt_output, 'w') as f:
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
            if not name_clean:
                errors.append("Trader Name is missing")
            elif not re.match(r'^[A-Za-z\s]+$', name_clean):
                errors.append(f"Trader Name '{name_clean}' contains non-alphabet characters.")
                
            # Validate Instrument should be alphabetic, spaces and dots allowed
            instrument_clean = instrument.strip()
            if not instrument_clean:
                errors.append("Instrument Name is missing")
            elif not re.match(r'^[A-Za-z\s\.]+$', instrument_clean):
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
    print(f"Validation report generated at: {txt_output}")
            
    # XSLT TRANSFORMATION LOGIC
    try:
        xslt_tree = etree.parse(xslt_file)
        transform = etree.XSLT(xslt_tree)
        # Apply transformation to the XML tree
        result_tree = transform(tree)
        
        # Save HTML report
        with open(html_output, 'wb') as html_f:
            html_f.write(etree.tostring(result_tree, pretty_print=True, method="html"))
        print(f"HTML report generated at: {html_output}")
    except Exception as e:
        print(f"Error during XSLT transformation: {e}")

if __name__ == "__main__":
    input_xml = 'source_trade.xml'
    input_xslt = 'source_trade.xslt'
    output_txt = 'output/validation.txt'
    output_html = 'output/report.html'
    
    validate_trades(input_xml, input_xslt, output_txt, output_html)