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
            except AttributeError:
                continue
            try:
                xobject = resources['/XObject']
            except AttributeError:
                # Are there types other than XObject?
                continue
            for res in xobject.itervalues():
                # In case it's indirect
                res = res.getObject()
                name = self.resource_name(res)
                if name in extracted:
                    continue
                extracted.add(name)
                yield res

    def get_image(self, resource):
        dimensions = (resource['/Width'], resource['/Height'])
        im = Image.new(
            self._image_colorspaces[resource['/ColorSpace']],
            dimensions)
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
            print('Resource: {}/{}'.format(res['/Type'], res['/Subtype']))


if __name__ == '__main__':
    try:
        fp = open(sys.argv[1])
    except IndexError:
        print('Usage: pdf_dumper <filename>')
        sys.exit(1)
    dumper = PDFDumper(fp)
    dumper.save_resources()
