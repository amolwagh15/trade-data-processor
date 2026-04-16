# trade-data-processor
Validate the trade data before uploading to the trade lifecycle database.

Project Overview
This pipeline automates the validation of XML trade data files. It ensures that critical fields like Trade IDs and Quantities meet business requirements before data ingestion.

Design Choices

Python (lxml): Used for its high performance and native support for XSLT transformations.


GitHub Actions: Acts as the orchestrator to automatically verify data integrity on every code change or data update.

Prerequisites

Git (for version control).

How to Run
Clone the Repo: git clone https://github.com/amolwagh15/trade-data-processor.git

View Results: Open the output/ directory for validation.txt and report.html.

Assumptions & Limitations

Empty Names: In source_trade.xml, Trade T12345 has an empty <name/>. The script flags this as a warning but checks formatting only if a name exists.

Scaling: For massive XML files (GBs), we would shift from etree.parse to etree.iterparse to save memory.