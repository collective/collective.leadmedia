# -*- coding: utf-8 -*-
# Viewlets
from plone.app.layout.viewlets import ViewletBase
from plone.dexterity.interfaces import IDexterityContainer
from plone.app.contenttypes.interfaces import IDocument
from Products.CMFCore.utils import getToolByName
from ..behaviors.slideshow import ISlideshow
from Products.CMFPlone.browser.syndication.adapters import FolderFeed
from zope.component import queryMultiAdapter
from Products.CMFPlone.interfaces import ISocialMediaSchema
from Products.CMFPlone.interfaces.syndication import IFeedItem
from plone.app.layout.viewlets.common import TitleViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.component.hooks import getSite
from plone.app.uuid.utils import uuidToCatalogBrain, uuidToObject

class LeadMediaViewlet(ViewletBase):
    """ A simple viewlet which renders leadimage """

    def update(self):
        # get item brain
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.queryCatalog({"UID": self.context.UID()})
        item = brains[0]

        self.available = False

        if not ISlideshow.providedBy(self.context):
            if hasattr(item, 'hasMedia'):
                if item.hasMedia:
                    self.available = True
                    media_brains = catalog.queryCatalog({"UID": item.leadMedia})
                    media = media_brains[0]
                    self.context.image = media.getObject()
                else:
                    self.available = False

class SocialTagsViewletCustom(TitleViewlet):
    index = ViewPageTemplateFile('templates/social_tags.pt')

    def update(self):
        super(SocialTagsViewletCustom, self).update()
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISocialMediaSchema, prefix="plone",
                                         check=False)

        if not settings.share_social_data:
            self.tags = []
            return

        self.tags = [
            dict(name="twitter:card", content="summary"),
            dict(name="twitter:title", content=self.page_title),
            dict(property="og:title", content=self.page_title),
            dict(property="og:type", content="website"),
            dict(property="og:site_name", content=self.site_title),
        ]
        if settings.twitter_username:
            self.tags.append(dict(name="twitter:site",
                                  content="@" + settings.twitter_username))
        if settings.facebook_app_id:
            self.tags.append(dict(property="fb:app_id",
                                  content=settings.facebook_app_id))
        if settings.facebook_username:
            self.tags.append(
                dict(property="og:article:publisher",
                     content="https://www.facebook.com/" + settings.facebook_username))

        # reuse syndication since that packages the data
        # the way we'd prefer likely
        item = queryMultiAdapter((self.context, FolderFeed(getSite())),
                                 IFeedItem, default=None)
        if item is None:
            # this should not happen but we can be careful
            return

<<<<<<< HEAD
        self.tags.extend([
            dict(name="twitter:description", content=item.description),
            dict(property="og:description", content=item.description),
=======
        social_description = item.description
        if not item.description:
            social_description = self.page_title

        self.tags.extend([
            dict(name="twitter:description", content=social_description),
            dict(property="og:description", content=social_description),
>>>>>>> plone5
            dict(name="twitter:url", content=item.link),
            dict(property="og:url", content=item.link),
        ])

        context_uid = self.context.UID()
        has_media = False
        brain = uuidToCatalogBrain(context_uid)
<<<<<<< HEAD
        if brain.leadMedia:
=======
        if getattr(brain, 'leadMedia', None):
>>>>>>> plone5
            has_media = True
            media = uuidToCatalogBrain(brain.leadMedia)

        if item.has_enclosure and item.file_length > 0:
            if item.file_type.startswith('image'):
                self.tags.extend([
                    dict(name="twitter:image", content=item.file_url),
                    dict(property="og:image", content=item.file_url),
                    dict(property="og:image:type", content=item.file_type)
                ])
            elif (item.file_type.startswith('video')
                    or item.file_type == "application/x-shockwave-flash"):
                self.tags.extend([
                    dict(property="og:video", content=item.file_url),
                    dict(property="og:video:type", content=item.file_type)
                ])
            elif item.file_type.startswith('audio'):
                self.tags.extend([
                    dict(property="og:audio", content=item.file_url),
                    dict(property="og:audio:type", content=item.file_type)
                ])
        elif has_media:
            if media != None:
                file_url = media.getURL()
<<<<<<< HEAD
                image = media.getObject()
=======
                file_type = "image/jpeg"
                """image = media.getObject()
>>>>>>> plone5
                image_file = getattr(image, 'image', None)
                if image_file:
                    file_type = getattr(image, 'contentType', None)
                    if not file_type:
                        file_type = "image/jpeg"
<<<<<<< HEAD
                
                    self.tags.extend([
                        dict(name="twitter:image", content=file_url),
                        dict(property="og:image", content=file_url),
                        dict(property="og:image:type", content=file_type)
                    ])
=======
                """
                self.tags.extend([
                    dict(name="twitter:image", content=file_url),
                    dict(property="og:image", content=file_url),
                    dict(property="og:image:type", content=file_type)
                ])
>>>>>>> plone5



