from five import grok
from Acquisition import aq_inner
from zope.interface import Interface
from plone.app.layout.viewlets.interfaces import IPortalHeader
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import ISiteRoot


class SpecialsViewlet(grok.Viewlet):
    grok.name('newport.sitecontent.SpecialsViewlet')
    grok.context(Interface)
    grok.require('zope2.View')
    grok.viewletmanager(IPortalHeader)

    def update(self):
        context = aq_inner(self.context)
        self.context_url = context.absolute_url()
