import json


def load_report_schema(schema_filename):
        with open(f'src/reports_schema/{schema_filename}', 'r') as file:
            schema = json.load(file)
        return schema