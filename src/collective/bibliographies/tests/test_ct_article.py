# -*- coding: utf-8 -*-
from collective.bibliographies.content.article import IArticle  # NOQA E501
from collective.bibliographies.testing import COLLECTIVE_BIBLIOGRAPHIES_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class ArticleIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_BIBLIOGRAPHIES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_article_schema(self):
        fti = queryUtility(IDexterityFTI, name='Article')
        schema = fti.lookupSchema()
        self.assertEqual(IArticle, schema)

    def test_ct_article_fti(self):
        fti = queryUtility(IDexterityFTI, name='Article')
        self.assertTrue(fti)

    def test_ct_article_factory(self):
        fti = queryUtility(IDexterityFTI, name='Article')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IArticle.providedBy(obj),
            u'IArticle not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_article_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Article',
            id='article',
        )

        self.assertTrue(
            IArticle.providedBy(obj),
            u'IArticle not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_article_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Article')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
