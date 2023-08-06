import xml.etree.ElementTree as ET
from lxml import etree
from config.settings import BASE_DIR, MEDIA_URL
import os
import random
# import os

def convert_2_files_into_new_structure(old_file_path:str, new_file_path:str) -> str:
    result_file = ''
    try:
        treeMain = etree.parse(new_file_path)
        encoding = treeMain.docinfo.encoding
        element = etree.ElementTree()
        parser = element.parse(old_file_path)
        prefix = parser.prefix
        path = parser.nsmap[prefix]
        ET.register_namespace(prefix, path)

        tree2 = ET.parse(new_file_path)
        root2 = tree2.getroot()

        file_content = ET.tostring(root2,
                                encoding=encoding,
                                method='xml',
                                xml_declaration=True).decode(encoding)

        num = str(random.randint(100_000_000,999_999_999))
        result_file = os.path.join(result_file, f'ResultFile{num}.xml')
        with open(result_file, 'w+', encoding="utf-16") as new_file:
            file_content = file_content.replace('\n','') # убирает ошибку в форматировании xml файла
            new_file.write(file_content)
            print("Content file = ", new_file.read())
            print(f"Путь до результирующего файла: {result_file}")
            return result_file
    except Exception as error:
        result_file = os.path.join(result_file, 'ErrorFile.txt')
        print(f"Путь до результирующего файла: {result_file}")
        with open(result_file, 'w', encoding="utf-16") as new_file:
            new_file.write('Convertation error!')  
            return result_file

    # if os.path.exists(next_file_path):
    #     print(f"Файл существует {next_file_path}")
    # else:
    #     print(f"Файл не существует {next_file_path}")

#convert_2_files_into_new_structure('Converter/documents/Z5107.xml', 'Converter/documents/70107_8.xml', 'Converter/documents/new_CUST.xml')