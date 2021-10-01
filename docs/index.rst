XML Reader
-----------------------------------------

The XML file format is an intermediate solution for reading a series of images. The reader expects a valid XML file structure with a list of "image" elements. Following a simple example:

.. code:: xml

   <?xml version="1.0" ?>
   <images>
       <image file=".\test001.tif"/>
       <image file=".\test002.tif"/>
       <image file=".\test003.tif"/>
   </images>

Please note as all images must have the same dimensions. For more information/updates please refer to the following `GitHub Issue <https://github.com/napari/napari/issues/661>`_.

Given you have a conform XML file, you can simple drag-n-drop the file into Napari or open the file from within Napari via the "File/Open File(s)..." menu.
