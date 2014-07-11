import re
from StringIO import StringIO
from lxml import etree as ET
from lxml.builder import E
import sys
import os

__author__ = 'Pyle'


def get_apoc():
    return ['TOB', 'JDT', 'ESG', 'ADE', 'WIS', 'SIR', 'BAR', 'LJE', 'S3Y', 'SUS', 'BEL', '1MA', '2MA', '1ES', 'MAN',
            'PS2', '3MA', '2ES', '4MA', 'ODS', 'PSS', 'EPL', '1EN', 'JUB', 'DNT', 'DAG']


def get_books2files(source_dir):
    book2files = {}
    files = os.listdir(source_dir)
    files.sort()
    apoc = get_apoc()
    for f in files:
        if os.path.isdir(f):
            continue
        if not re.match('^[A-Z0-9]{3}[0-9]{0,3}.htm', f):
            continue
        group_name = f[:3]
        if group_name in apoc:
            continue  # skip apocryphal
        file_name, extension = f.split('.', 1)
        if group_name == 'PSA' and file_name.endswith('000') or group_name != 'PSA' and file_name.endswith('00'):
            continue  # skip intros
        if group_name not in book2files:
            book2files[group_name] = []
        full_path = os.path.join(source_dir, f)
        book2files[group_name].append(full_path)
    return book2files


def get_output_file(output_dir, file_name):
    output_file = os.path.join(output_dir, file_name + ".html")
    return output_file


def merge_multi_books(books2files, books_to_combine, output_dir, multi_book_title):
    files = []
    for book in books_to_combine:
        files += books2files[book]
    file_name = '-'.join(books_to_combine)
    output_file = get_output_file(output_dir, file_name)
    merge_files_in_order(files, multi_book_title, output_file)


def group_by_jbj_canon49(source_dir, output_dir):
    books2files = get_books2files(source_dir)
    # first handle special book combinations
    multi_books_processed = []
    multi_books = ['1SA', '2SA']
    merge_multi_books(books2files, multi_books, output_dir, 'Samuel')
    multi_books_processed += multi_books

    multi_books = ['1KI', '2KI']
    merge_multi_books(books2files, multi_books, output_dir, 'Kings')
    multi_books_processed += multi_books

    multi_books = ['JER', 'LAM']
    merge_multi_books(books2files, multi_books, output_dir, 'Jeremiah-Lamentations')
    multi_books_processed += multi_books

    multi_books = ['1CH', '2CH', 'EZR', 'NEH']
    merge_multi_books(books2files, multi_books, output_dir, 'Greater Chronicles')
    multi_books_processed += multi_books

    multi_books = ['HOS', 'JOL', 'AMO', 'OBA', 'JON', 'MIC', 'NAM', 'HAB', 'ZEP', 'HAG', 'ZEC', 'MAL']
    merge_multi_books(books2files, multi_books, output_dir, 'The Twelve')
    multi_books_processed += multi_books

    for book in books2files:
        if book in multi_books_processed:
            continue
        output_file = get_output_file(output_dir, book)
        merge_files_in_order(books2files[book], book, output_file)

def get_nav():
    return E.ul(E.li(E.a('index', {'href': 'index.html'})), {'class': 'tnav'})

def merge_files_in_order(html_files, title, output_file):
    # rel="stylesheet" href="arl.css" type="text/css">
    etree_setup = (
        E.html(
            E.head(E.title(title), E.link({'rel': 'stylesheet', 'href': '49scrolls.css', 'type': 'text/css'})),
            E.body(get_nav(),
                   E.div({'class': 'main'}),
                   get_nav())
        )
    )

    htmlparser = ET.HTMLParser()
    etree_output = ET.parse(StringIO(ET.tostring(etree_setup)), htmlparser)
    output_main = etree_output.find('./body/div')

    for html_file in html_files:
        etree_html = ET.parse(html_file, htmlparser)

        etree_main = etree_html.xpath("./body/div[@class='main']")
        if len(etree_main) == 0:
            continue
        for div in etree_main[0].findall('./div'):
            if 'footnote' in div.attrib['class'].split(' '):
                continue
            if div.attrib['class'] == 'b':
                continue
            output_main.append(div)

    etree_output.write(output_file)


if __name__ == "__main__":
    group_by_jbj_canon49(sys.argv[1], sys.argv[2])