import xml.etree.ElementTree as ET
import os
import re

def validate_trades(xml_file, xslt_file, txt_output, html_output):
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return

    validation_results = []
    
    with open(txt_output, 'w') as f:
        for trade in root.findall('trade'):
            trade_id = (trade.find('trade_id').text if trade.find('trade_id') is not None else "") or ""
            
            trader_node = trade.find('trader')
            name = (trader_node.find('name').text if trader_node is not None else "") or ""
            
            inst_node = trade.find('instrument')
            instrument = (inst_node.find('name').text if inst_node is not None else "") or ""
            
            details_node = trade.find('transaction_details')
            quantity_str = (details_node.find('quantity').text if details_node is not None else "") or ""
            
            errors = []
            
            if not trade_id.isalnum():
                errors.append(f"Trade ID '{trade_id}' is not alphanumeric.")
            
            name_clean = name.strip()
            if not name_clean:
                errors.append("Trader Name is missing")
            elif not re.match(r'^[A-Za-z\s]+$', name_clean):
                errors.append(f"Trader Name '{name_clean}' contains non-alphabet characters.")
                
            instrument_clean = instrument.strip()
            if not instrument_clean:
                errors.append("Instrument Name is missing")
            elif not re.match(r'^[A-Za-z\s\.]+$', instrument_clean):
                errors.append(f"Instrument Name '{instrument_clean}' contains non-alphabet characters.")
                
            try:
                qty = float(quantity_str.strip())
                if qty > 1000:
                    errors.append(f"Quantity {qty} exceeds the maximum limit of 1000.")
            except ValueError:
                errors.append(f"Quantity '{quantity_str}' is empty or not a valid number.")
                
            status = "FAILED" if errors else "PASSED"
            validation_results.append({"id": trade_id, "status": status, "errors": errors})

            if errors:
                f.write(f"Validation errors for Trade {trade_id}:\n")
                for error in errors:
                    f.write(f"  - {error}\n")
                f.write("\n")
            else:
                f.write(f"Trade {trade_id}: Passed validation.\n\n")

        f.write("Validation process completed.\n")
    print(f"Validation report generated at: {txt_output}")

    try:
        html_content = """
        <html>
        <head><title>Trade Validation Report</title></head>
        <body>
            <h1>Trade Validation Summary</h1>
            <table border="1">
                <tr><th>Trade ID</th><th>Status</th><th>Issues</th></tr>
        """
        for res in validation_results:
            err_msg = ", ".join(res['errors']) if res['errors'] else "None"
            color = "red" if res['status'] == "FAILED" else "green"
            html_content += f"<tr><td>{res['id']}</td><td style='color:{color}'>{res['status']}</td><td>{err_msg}</td></tr>"
        
        html_content += "</table></body></html>"
        
        with open(html_output, 'w') as html_f:
            html_f.write(html_content)
        print(f"HTML report generated at: {html_output}")
    except Exception as e:
        print(f"Error generating HTML report: {e}")

if __name__ == "__main__":
    input_xml = 'source_trade.xml'
    input_xslt = 'source_trade.xslt'
    output_txt = 'output/validation.txt'
    output_html = 'output/report.html'
    
    validate_trades(input_xml, input_xslt, output_txt, output_html)