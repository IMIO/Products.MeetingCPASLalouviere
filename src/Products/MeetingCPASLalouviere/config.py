# -*- coding: utf-8 -*-
#
# File: MeetingCPASLalouviere.py
#
# Copyright (c) 2014 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andre Nuyens <andre@imio.be>"""
__docformat__ = 'plaintext'


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
##code-section config-head #fill in your manual code here
import os
##/code-section config-head


PROJECTNAME = "MeetingCPASLalouviere"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
from Products.PloneMeeting import config as PMconfig
CPASLALOUVIEREROLES = {}
CPASLALOUVIEREROLES['budgetimpactreviewers'] = 'MeetingBudgetImpactReviewer'
CPASLALOUVIEREROLES['n1'] = 'MeetingN1'
CPASLALOUVIEREROLES['n2'] = 'MeetingN2'
CPASLALOUVIEREROLES['secretaire'] = 'MeetingSecretaire'
PMconfig.MEETINGROLES.update(CPASLALOUVIEREROLES)

PMconfig.MEETING_GROUP_SUFFIXES = PMconfig.MEETINGROLES.keys()
#the president will use the default 'MeetingReviewer' role

##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from Products.MeetingCPASLalouviere.AppConfig import *
except ImportError:
    pass