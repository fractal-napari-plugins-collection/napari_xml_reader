"""
Main module containing the method to read xml files.
"""
import os
from xml.dom import minidom
from napari.plugins.io import read_data_with_plugins
from napari_plugin_engine import napari_hook_implementation


def xml_reader(path):
    """
    Function which reads images from an XML file.

    :param path: The path of the .xml file
    :return: List of LayerData tuples
    """
    xmldoc = minidom.parse(path)
    images_element = xmldoc.getElementsByTagName('images')[0]
    image_elements = xmldoc.getElementsByTagName('image')
    layer_data_list = read_data_with_plugins(
        [
            os.path.join(os.path.dirname(path), image_element.attributes["file"].value)
            for image_element in image_elements
        ]
    )
    layer_type = "image"
    try:
        if images_element.attributes["type"].value in ["image", "labels"]:
            layer_type = images_element.attributes["type"].value
    except KeyError:
        pass

    return [
        (
            layer_data[0],  # data
            layer_data[1] if len(layer_data) >= 2 else {},  # meta
            layer_type
        )
        for layer_data in layer_data_list
    ]


@napari_hook_implementation
def napari_get_reader(path):
    """
    Napari plugin that returns a reader for .xml files.

    .. note::
       This hook does not support a list of paths

    :param path:  The path of the .xml file
    :return: The xml_reader function or None
    """
    if isinstance(path, str) and path.endswith(".xml"):
        return xml_reader
    return None
