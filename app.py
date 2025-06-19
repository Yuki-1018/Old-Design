from flask import Flask, Response
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/table', methods=['GET'])
def get_table():
    url = 'https://www.jorudan.co.jp/unk/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', class_='unktable')
    if table is None:
        return Response("<error>Table not found</error>", status=404, mimetype='application/xml')

    # Create XML structure
    root = ET.Element("table")
    
    headers = [header.text for header in table.find_all('th')]
    rows = table.find_all('tr')
    
    # Add headers
    header_elem = ET.SubElement(root, "headers")
    for header in headers:
        header_tag = ET.SubElement(header_elem, "header")
        header_tag.text = header

    # Add rows
    for row in rows:
        cells = row.find_all('td')
        if cells:
            row_elem = ET.SubElement(root, "row")
            for cell in cells:
                cell_elem = ET.SubElement(row_elem, "cell")
                cell_elem.text = cell.text

    # Convert XML to string
    xml_str = ET.tostring(root, encoding='unicode')
    
    return Response(xml_str, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True)
