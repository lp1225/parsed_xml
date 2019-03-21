from lxml import etree
import os
import xmltodict
import json
# import pandas as pd


class XMLConnector:

    def __init__(self, filepath):
        self.tree = etree.parse(filepath)

    @property
    def parsed_data(self):
        elem_str = etree.tostring(self.tree)
        # str 转 dict
        elem_dict = xmltodict.parse(elem_str)
        return elem_dict

    @property
    def convert_json(self):
        elem_json = json.dumps(self.parsed_data)
        return elem_json

    @property
    def convert_csv(self):
        orderdict = self.parsed_data
        header = orderdict.keys()
        rows = pd.DataFrame(orderdict).to_dict('records')

        with open('outtest.csv', 'w') as f:
            f.write(','.join(header))
            f.write('\n')
            for data in rows:
                f.write(",".join(str(data[h]) for h in header))
                f.write('\n')
        return None


if __name__ == '__main__':
    # 需要pip lxml, xmltodict
    filepath = os.path.abspath(os.path.dirname(__file__))
    print(filepath)
    # 路径
    final_path = os.path.join(filepath, 'style1.xml')
    print(final_path)

    # 解析为json
    conn = XMLConnector(final_path)
    res = conn.convert_json
    print('res', res)
    # conn.convert_csv

