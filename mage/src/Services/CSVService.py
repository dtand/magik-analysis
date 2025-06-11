import csv
import os
import pandas as pd
from openpyxl import Workbook
from mage.src.Utils import file_utils

class CSVService:

    def __init__(self):
        self.pages = {}

    def add_page(self, name):
        self.pages[name] = []

    def add_row(self, page, row):
        self.pages[page].append(row)

    def write_to_folder(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for page in self.pages:
            with open('{}/{}.csv'.format(output_dir, page), 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.pages[page])

    def to_workbook(self, csv_folder, excel_file):
        workbook = Workbook()
        workbook.save(excel_file)

        with pd.ExcelWriter(excel_file, engine='openpyxl', mode="a") as writer:
            for filename in os.listdir(csv_folder):
                if filename.endswith('.csv'):
                    file_path = os.path.join(csv_folder, filename)
                    df = pd.read_csv(file_path)
                    sheet_name = os.path.splitext(filename)[0]
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

    def from_report(report, name):
        csv_service = CSVService()
        csv_service.add_page(name)
        has_header = False
        for row in report.rows:
            if not has_header:
                csv_service.add_row(name, report.headers)
                has_header = True
            csv_service.add_row(name, row)
        return csv_service
    
    def add_page_with_rows(self, page, columns, rows):
        self.add_page(page)
        self.add_row(page, columns)
        for row in rows:
            self.add_row(page, row)


