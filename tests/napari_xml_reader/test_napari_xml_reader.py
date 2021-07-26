"""
Unittests for napri_xml_reader.napari_xml_reader module.
"""
from unittest.mock import MagicMock
import sys

# mock imports which are not available in the test environment
sys.modules['napari'] = MagicMock()
sys.modules['napari.plugins'] = MagicMock()
sys.modules['napari.plugins.io'] = MagicMock()

from napari_xml_reader.napari_xml_reader import xml_reader


class MockXMLDoc():
    def __init__(self, data_dict):
        self.data_dict = data_dict
    def getElementsByTagName(self, key):
        return self.data_dict[key]

class MockXMLElement():
    def __init__(self, attr_dict):
        self.attributes = attr_dict

class MockXMLAttribut():
    def __init__(self, value):
        self.value = value


def test_xml_reader_for_images(mocker):
    """
    Test for the napari_xml_reader.xml_reader() function with image data.
    """
    mocker.patch(
        'xml.dom.minidom.parse',
        return_value=MockXMLDoc({
            'images': [
                MockXMLElement({'type': MockXMLAttribut('invalid')}),
            ],
            'image': [
                MockXMLElement({'file': MockXMLAttribut('path1')}),
                MockXMLElement({'file': MockXMLAttribut('path2')}),
            ]
        })
    )
    mocker.patch(
        'napari_xml_reader.napari_xml_reader.read_data_with_plugins',
        lambda path: [(None, path),]
    )

    layer_data_list = xml_reader("test.xml")
    assert len(layer_data_list) == 1
    data, meta, layer_type = layer_data_list[0]
    assert layer_type == "image"
    assert meta == ['path1', 'path2']

def test_xml_reader_for_labels(mocker):
    """
    Test for the napari_xml_reader.xml_reader() function with label data.
    """
    mocker.patch(
        'xml.dom.minidom.parse',
        return_value=MockXMLDoc({
            'images': [
                MockXMLElement({'type': MockXMLAttribut('labels')}),
            ],
            'image': [
                MockXMLElement({'file': MockXMLAttribut('path1')}),
                MockXMLElement({'file': MockXMLAttribut('path2')}),
            ]
        })
    )
    mocker.patch(
        'napari_xml_reader.napari_xml_reader.read_data_with_plugins',
        lambda path: [(None, path),]
    )

    layer_data_list = xml_reader("test.xml")
    assert len(layer_data_list) == 1
    data, meta, layer_type = layer_data_list[0]
    assert layer_type == "labels"
    assert meta == ['path1', 'path2']
