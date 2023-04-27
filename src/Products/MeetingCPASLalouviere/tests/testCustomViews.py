# -*- coding: utf-8 -*-
from datetime import datetime

from Products.MeetingCommunes.tests.testCustomViews import testCustomViews as mctcv
from Products.MeetingCPASLalouviere.browser.overrides import MLLItemDocumentGenerationHelperView
from Products.MeetingCPASLalouviere.browser.overrides import MLLMeetingDocumentGenerationHelperView
from Products.MeetingCPASLalouviere.tests.MeetingCPASLalouviereTestCase import (
    MeetingCPASLalouviereTestCase,
)


class testCustomViews(mctcv, MeetingCPASLalouviereTestCase):
    """
        Tests the custom views
    """


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomViews, prefix="test_"))
    return suite
