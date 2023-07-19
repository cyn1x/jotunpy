import os
import xml.etree.ElementTree as ET

from core import database, util
from core.config import CONFIG


def add_item(metadata: dict, uri: str):
    metadata['link'] = uri
    node = f'channel/item[guid="{uri}"]'

    # Create timestamp and add it to the metadata dictionary
    pub_date = util.format_datetime('%a, %d %b %Y %H:%M:%S %z')
    metadata['published'] = pub_date
    metadata['link'] = metadata.get('link')

    exists_in_rss = root.find(node) is not None
    exists_in_db = database.item_exists(uri)

    match (exists_in_rss, exists_in_db):
        case (True, True):
            return
        case (True, False):  # This will only happen if the RSS feed is manually edited
            metadata['published'] = root.find(f'{node}/pubDate').text
            database.insert_blog_entry(metadata)
            return
        case (False, True):  # This will only happen if the database is manually edited
            pub_date = database.get_blog_entry(uri, 'published')[0]
            metadata['published'] = pub_date
        case (False, False):  # This is the expected case
            # Add the item to the database
            database.insert_blog_entry(metadata)

    # Get the channel element from the root
    channel = root.find('channel')

    item = ET.SubElement(channel, 'item')
    item_title = ET.SubElement(item, 'title')
    item_title.text = metadata.get('title')
    item_link = ET.SubElement(item, 'link')
    item_link.text = metadata.get('link')
    item_description = ET.SubElement(item, 'description')
    item_description.text = metadata.get('description')
    item_pub_date = ET.SubElement(item, 'pubDate')
    item_pub_date.text = pub_date
    item_guid = ET.SubElement(item, 'guid')
    item_guid.text = metadata.get('link')
    last_build_date = channel.find('lastBuildDate')
    last_build_date.text = pub_date

    ET.indent(root, space='  ')
    tree = ET.ElementTree(root)
    filepath = os.path.join(CONFIG['RSS']['FILEPATH'], CONFIG['RSS']['FILENAME'])
    tree.write(filepath, encoding='utf-8', xml_declaration=True)


def read_file():
    filepath = os.path.join(CONFIG['RSS']['FILEPATH'], CONFIG['RSS']['FILENAME'])
    if not os.path.exists(filepath):
        util.write_file('./site.rss', '<?xml version="1.0" encoding="UTF-8" ?>')

        # Create necessary metadata for RSS feed
        _root = ET.Element('rss')
        _root.set('version', '2.0')
        channel = ET.SubElement(_root, 'channel')
        title = ET.SubElement(channel, 'title')
        title.text = CONFIG['RSS']['AUTHOR']
        link = ET.SubElement(channel, 'link')
        link.text = CONFIG['RSS']['LINK']
        description = ET.SubElement(channel, 'description')
        description.text = CONFIG['RSS']['DESCRIPTION']
        language = ET.SubElement(channel, 'language')
        language.text = CONFIG['RSS']['LANGUAGE']
        channel_last_build_date = ET.SubElement(channel, 'lastBuildDate')
        channel_last_build_date.text = util.format_datetime('%a, %d %b %Y %H:%M:%S %z')

        # Indent the XML and write to file
        ET.indent(_root, space='  ')
        tree = ET.ElementTree(_root)
        tree.write(filepath, encoding='utf-8', xml_declaration=True)

    tree = ET.parse(filepath)
    _root = tree.getroot()

    return _root


# Get the root element from the RSS feed
root = read_file()
