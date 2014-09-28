#!/usr/bin/env python

from __future__ import print_function
import hashlib
import Image
import pyPdf
import sys


class PDFDumper(object):
    """Dump resources from a pdf.

    Currently, only images are supported.
    """

    _image_colorspaces = {
        '/DeviceRGB': 'RGB',
        '/DeviceGray': 'L',
        }

    def __init__(self, fp):
        self.fp = fp
        self.reader = pyPdf.PdfFileReader(fp)

    def get_resources(self):
        extracted = set()
        for page in self.reader.pages:
            try:
                resources = page['/Resources']
            except KeyError:
                continue
            try:
                xobject = resources['/XObject']
            except KeyError:
                # Are there types other than XObject?
                continue
            for res in xobject.itervalues():
                # In case it's indirect
                res = res.getObject()
                try:
                    name = self.resource_name(res)
                except (NotImplementedError, AssertionError) as ex:
                    print('Warning: {}'.format(ex))
                    continue
                if name in extracted:
                    continue
                extracted.add(name)
                yield res

    def get_image(self, resource):
        dimensions = (resource['/Width'], resource['/Height'])
        colorspace = resource['/ColorSpace']
        if isinstance(colorspace, basestring):
            # Basic image
            colorspace = self._image_colorspaces[colorspace]
            im = Image.new(colorspace, dimensions)
            im.frombytes(resource.getData())
            return im
        # Paletteized image
        if colorspace[0] != '/Indexed':
            print('Not implemented, image type: {}{}'.format(
                colorspace[0], colorspace[1]))
            return None
        palette = colorspace[3].getObject().getData()
        im = Image.new('P', dimensions)
        im.putpalette(palette)
        im.frombytes(resource.getData())
        return im

    @staticmethod
    def resource_name(resource):
        return hashlib.sha1(resource.getData()).hexdigest()

    def save_resources(self):
        for res in self.get_resources():
            if res['/Type'] == '/XObject' and res['/Subtype'] == '/Image':
                im = self.get_image(res)
                im.save('{}.png'.format(self.resource_name(res)))
                continue
            print('Unknown Resource: {}/{}'.format(
                res['/Type'], res['/Subtype']))


if __name__ == '__main__':
    try:
        fp = open(sys.argv[1])
    except IndexError:
        print('Usage: pdf_dumper <filename>')
        sys.exit(1)
    dumper = PDFDumper(fp)
    dumper.save_resources()
