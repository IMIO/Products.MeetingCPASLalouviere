# -*- coding: utf-8 -*-

from collections import OrderedDict
from Products.PloneMeeting import config as PMconfig


PROJECTNAME = "MeetingCPASLalouviere"

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

CPASLALOUVIEREROLES = {}
CPASLALOUVIEREROLES['budgetimpactreviewers'] = 'MeetingBudgetImpactReviewer'
CPASLALOUVIEREROLES['n1'] = 'MeetingN1'
CPASLALOUVIEREROLES['n2'] = 'MeetingN2'
CPASLALOUVIEREROLES['secretaire'] = 'MeetingSecretaire'
PMconfig.MEETINGROLES.update(CPASLALOUVIEREROLES)

PMconfig.MEETING_GROUP_SUFFIXES = PMconfig.MEETINGROLES.keys()
#the president will use the default 'MeetingReviewer' role

STYLESHEETS = [{'id': 'meetingcpaslalouviere.css',
                'title': "MeetingCPASLalouvière CSS styles"}]

CPASLALOUVIEREMEETINGREVIEWERS = OrderedDict([('reviewers', 'proposed_to_president'),
                                            ('secretaire', 'proposed_to_secretaire'),
                                            ('n2', 'proposed_to_n2'),
                                            ('n1', 'proposed_to_n1'), ])
PMconfig.MEETINGREVIEWERS = CPASLALOUVIEREMEETINGREVIEWERS
