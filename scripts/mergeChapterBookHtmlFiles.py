import re
from StringIO import StringIO
from lxml import etree as ET
from lxml.builder import E
import sys
import os

__author__ = 'Pyle'


def get_book_order():
    return ['GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', '1SA-2SA', 'PSA', 'JOB', 'PRO', 'SNG', 'ECC',
            'ISA', '1KI-2KI', 'JER-LAM', 'EZK', 'DAN', 'EST', 'HOS-JOL-AMO-OBA-JON-MIC-NAM-HAB-ZEP-HAG-ZEC-MAL',
            '1CH-2CH-EZR-NEH', 'MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM',
            '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE',
            '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV']


def get_books2titles():
    return {'GEN': 'Genesis', 'EXO': 'Exodus',
            'LEV': 'Leviticus', 'NUM': 'Numbers', 'DEU': 'Deuteronomy', 'JOS': 'Joshua', 'JDG': 'Judges',
            'RUT': 'Ruth', '1SA-2SA': 'Samuel', 'PSA': 'Psalms', 'JOB': 'Job', 'PRO': 'Proverbs',
            'SNG': 'Song of Songs', 'ECC': 'Ecclesiastes', 'ISA': 'Isaiah', '1KI-2KI': 'Kings',
            'JER-LAM': 'Jeremiah-Lamentations', 'EZK': 'Ezekiel',
            'DAN': 'Daniel', 'EST': 'Esther', 'HOS-JOL-AMO-OBA-JON-MIC-NAM-HAB-ZEP-HAG-ZEC-MAL': 'The Twelve',
            '1CH-2CH-EZR-NEH': 'Greater Chronicles', 'MAT': 'Matthew', 'MRK': 'Mark', 'LUK': 'Luke',
            'JHN': 'John', 'ACT': 'Acts', 'ROM': 'Romans',
            '1CO': '1 Corinthians', '2CO': '2 Corinthians', 'GAL': 'Galatians', 'EPH': 'Ephesians',
            'PHP': 'Philippians', 'COL': 'Colossians', '1TH': '1 Thessalonians', '2TH': '2 Thessalonians',
            '1TI': '1 Timothy', '2TI': '2 Timothy', 'TIT': 'Titus', 'PHM': 'Philemon', 'HEB': 'Hebrews',
            'JAS': 'James', '1PE': '1 Peter',
            '2PE': '2 Peter', '1JN': '1 John', '2JN': '2 John', '3JN': '3 John', 'JUD': 'Jude',
            'REV': 'Revelation'}


def get_surrounding_books(book_code):
    book_before = None
    book_after = None
    all_books = get_book_order()
    idx_book = all_books.index(book_code)
    idx_book_before = idx_book - 1
    idx_book_after = idx_book + 1
    if idx_book_before >= 0:
        book_before = all_books[idx_book_before]
    if idx_book_after <= (len(all_books) - 1):
        book_after = all_books[idx_book + 1]
    return book_before, book_after


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
        if group_name in ['GLO', 'FRT']:
            continue
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

    books2titles = get_books2titles()
    for book in books2files:
        if book in multi_books_processed:
            continue
        output_file = get_output_file(output_dir, book)
        merge_files_in_order(books2files[book], books2titles[book], output_file)


def get_list_item_nav(text, file_name, anchor):
    if not file_name:
        return ''
    return E.li(E.a(text, {'href': '{}{}'.format(file_name, anchor)}))


def get_nav(book_code, group_anchor, book_anchor):
    book_title = ''
    book_link = ''
    if book_code is not None:
        books2titles = get_books2titles()
        book_title = books2titles[book_code]
        book_link = '{}.html'.format(book_code)
    return E.ul(get_list_item_nav(group_anchor, 'index.html', '#' + group_anchor),
                get_list_item_nav(book_title, book_link, anchor='#' + book_anchor), {'class': 'tnav'})


def get_book_group(book_code):
    all_books = get_book_order()
    if not book_code in all_books:
        return ''
    i_book = all_books.index(book_code)
    i_lion = all_books.index('JDG')
    i_eagle = all_books.index('ISA')
    i_man = all_books.index('MAT')
    if i_book >= i_man:
        return 'Man'
    if i_book >= i_eagle:
        return 'Eagle'
    if i_book >= i_lion:
        return 'Lion'
    if i_book >= 0:
        return 'Ox'
    return ''


def add_nav_divs(output_file, etree_main):
    book_file_name = os.path.basename(output_file)
    book_code, _ = book_file_name.split('.', 1)
    book_group = get_book_group(book_code)
    previous_book_code, next_book_code = get_surrounding_books(book_code)
    top_nav = get_nav(book_code=previous_book_code, group_anchor=book_group, book_anchor='bottom')
    etree_main.addprevious(top_nav)
    bottom_nav = get_nav(book_code=next_book_code, group_anchor=book_group, book_anchor='')
    etree_main.addnext(bottom_nav)


def merge_files_in_order(html_files, title, output_file):
    # rel="stylesheet" href="arl.css" type="text/css">
    etree_setup = (
        E.html(
            E.head(E.title(title), E.link({'rel': 'stylesheet', 'href': '49scrolls.css', 'type': 'text/css'})),
            E.body(E.div({'class': 'main'}))
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
    output_main.append(ET.XML('<a id="bottom"/>'))
    add_nav_divs(output_file, output_main)
    etree_output.write(output_file)


if __name__ == "__main__":
    group_by_jbj_canon49(sys.argv[1], sys.argv[2])