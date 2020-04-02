# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.MeetingCommunes.profiles.zcpas import import_data as mc_import_data

data = deepcopy(mc_import_data.data)

# Remove persons -------------------------------------------------
data.persons = []

# No Users and groups -----------------------------------------------

# Meeting configurations -------------------------------------------------------
# Bureau Permanent
bpMeeting = deepcopy(mc_import_data.bpMeeting)
bpMeeting.id = 'meeting-config-bp'
bpMeeting.title = 'Bureau Permanent'
bpMeeting.folderTitle = 'Bureau Permanent'
bpMeeting.shortName = 'Bureau'
bpMeeting.itemWorkflow = 'meetingitemcpaslalouviere_workflow'
bpMeeting.meetingWorkflow = 'meetingcpaslalouviere_workflow'
bpMeeting.itemConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowConditions'
bpMeeting.itemActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowActions'
bpMeeting.meetingConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowConditions'
bpMeeting.meetingActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowActions'
bpMeeting.transitionsForPresentingAnItem = ['proposeToN1', 'proposeToN2', 'proposeToSecretaire',
                                                 'proposeToPresident', 'validate', 'present']
bpMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
                                                              'item_transition': 'itemfreeze'},

                                                             {'meeting_transition': 'decide',
                                                              'item_transition': 'itemfreeze'},

                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'itemfreeze'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'accept'},

                                                             {'meeting_transition': 'backToCreated',
                                                              'item_transition': 'backToPresented'},)
bpMeeting.itemAdviceStates = ['proposed_to_president', ]
bpMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']
bpMeeting.workflowAdaptations = []
bpMeeting.transitionsToConfirm = []
bpMeeting.itemBudgetInfosStates = []
bpMeeting.podTemplates = []

# Conseil de l'Action Sociale
casMeeting = deepcopy(mc_import_data.casMeeting)
casMeeting.id = 'meeting-config-cas'
casMeeting.title = 'Conseil Action Soiale'
casMeeting.folderTitle = 'Conseil Action Soiale'
casMeeting.shortName = 'CAS'
casMeeting.itemWorkflow = 'meetingitemcpaslalouviere_workflow'
casMeeting.meetingWorkflow = 'meetingcpaslalouviere_workflow'
casMeeting.itemConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowConditions'
casMeeting.itemActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowActions'
casMeeting.meetingConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowConditions'
casMeeting.meetingActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowActions'
casMeeting.transitionsForPresentingAnItem = ['proposeToN1', 'proposeToN2', 'proposeToSecretaire',
                                                 'proposeToPresident', 'validate', 'present']

casMeeting.itemAdviceStates = ['proposed_to_president', ]
casMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']
casMeeting.workflowAdaptations = []
casMeeting.itemCopyGroupsStates = []
casMeeting.transitionsToConfirm = []
casMeeting.itemBudgetInfosStates = []
casMeeting.podTemplates = []

data.meetingConfigs = (bpMeeting, casMeeting)
data.usersOutsideGroups += []
# ------------------------------------------------------------------------------
