import math
from Acquisition import aq_inner
from five import grok

from zope.component import getMultiAdapter

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable


class IGalleryFolder(form.Schema, IImageScaleTraversable):
    """
    A dedicated image gallery folder
    """


class GalleryFolder(Container):
    grok.implements(IGalleryFolder)


class View(grok.View):
    """ Thumbnail view """

    grok.context(IGalleryFolder)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_galleries = len(self.contained_galleries()) > 0
        self.has_images = len(self.contained_images()) > 0

    def gallery_matrix(self):
        items = self.contained_galleries()
        return self.build_matrix(items)

    def image_matrix(self):
        items = self.image_list()
        return self.build_matrix(items)

    def contained_galleries(self):
        context = aq_inner(self.context)
        items = context.restrictedTraverse('@@folderListing')(
            portal_type='newport.sitecontent.galleryfolder')
        return items

    def contained_images(self):
        context = aq_inner(self.context)
        items = context.restrictedTraverse('@@folderListing')(
            portal_type='Image')
        return items

    def build_matrix(self, data):
        items = data
        count = len(items)
        rowcount = count / 4.0
        rows = math.ceil(rowcount)
        matrix = []
        for i in range(int(rows)):
            row = []
            for j in range(4):
                index = 4 * i + j
                if index <= int(count - 1):
                    cell = {}
                    cell['item'] = items[index]
                    row.append(cell)
            matrix.append(row)
        return matrix

    def image_list(self):
        images = self.contained_images()
        data = []
        for item in images:
            info = {}
            info['title'] = item.Title
            info['desc'] = item.Description
            thumb = self.getImageTag(item, scalename='thumb')
            info['thumb_url'] = thumb['url']
            info['thumb_width'] = thumb['width']
            info['thumb_height'] = thumb['height']
            original = self.getImageTag(item, scalename='original')
            info['original_url'] = original['url']
            info['original_width'] = original['width']
            info['original_height'] = original['height']
            data.append(info)
        return data

    def getImageTag(self, item, scalename):
        obj = item.getObject()
        scales = getMultiAdapter((obj, self.request), name='images')
        if scalename == 'thumb':
            scale = scales.scale('image', width=200, height=200)
        else:
            scale = scales.scale('image', width=768, height=768)
        item = {}
        if scale is not None:
            item['url'] = scale.url
            item['width'] = scale.width
            item['height'] = scale.height
        return item
