# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.PloneMeeting.profiles import UserDescriptor
from Products.MeetingCommunes.profiles.zcpas import import_data as mc_import_data

from Products.MeetingCPASLalouviere.config import LLO_ITEM_CPAS_WF_VALIDATION_LEVELS

data = deepcopy(mc_import_data.data)

# Meeting configurations -------------------------------------------------------
# College communal
data.bpMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_CPAS_WF_VALIDATION_LEVELS)
data.bpMeeting.itemAdviceStates = ['proposed_to_president', ]
data.bpMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']

# Conseil communal
data.casMeeting = deepcopy(mc_import_data.councilMeeting)
data.casMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_CPAS_WF_VALIDATION_LEVELS)
data.casMeeting.itemAdviceStates = ['proposed_to_president', ]
data.casMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']
# ------------------------------------------------------------------------------
