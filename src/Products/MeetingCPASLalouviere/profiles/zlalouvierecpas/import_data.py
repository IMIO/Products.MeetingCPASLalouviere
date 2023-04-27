# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.zcpas import import_data as mc_import_data

from Products.MeetingCPASLalouviere.config import LLO_ITEM_CPAS_WF_VALIDATION_LEVELS, LLO_APPLYED_CPAS_WFA

data = deepcopy(mc_import_data.data)

# Meeting configurations -------------------------------------------------------
# College communal
bpMeeting = deepcopy(mc_import_data.bpMeeting)
bpMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_CPAS_WF_VALIDATION_LEVELS)
bpMeeting.itemAdviceStates = ['proposed_to_president', ]
bpMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']
bpMeeting.workflowAdaptations = deepcopy(LLO_APPLYED_CPAS_WFA)
bpMeeting.transitionsToConfirm = []
bpMeeting.itemBudgetInfosStates = []

# Conseil communal
casMeeting = deepcopy(mc_import_data.casMeeting)
casMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_CPAS_WF_VALIDATION_LEVELS)
casMeeting.itemAdviceStates = ['proposed_to_president', ]
casMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']
casMeeting.workflowAdaptations = deepcopy(LLO_APPLYED_CPAS_WFA)
casMeeting.transitionsToConfirm = []
casMeeting.itemBudgetInfosStates = []

data.meetingConfigs = (bpMeeting, casMeeting)
# ------------------------------------------------------------------------------
