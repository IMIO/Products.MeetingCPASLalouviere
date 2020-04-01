# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.PloneMeeting.profiles import UserDescriptor
from Products.PloneMeeting.profiles.testing import import_data as pm_import_data
from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data

data = deepcopy(mc_import_data.data)

# Inherited users
pmReviewer1 = deepcopy(pm_import_data.pmReviewer1)
pmReviewer2 = deepcopy(pm_import_data.pmReviewer2)
pmReviewerLevel1 = deepcopy(pm_import_data.pmReviewerLevel1)
pmReviewerLevel2 = deepcopy(pm_import_data.pmReviewerLevel2)
pmManager = deepcopy(pm_import_data.pmManager)
# xxx specific to CPAS La louvière
pmN1 = UserDescriptor('pmN1', [])
pmN2 = UserDescriptor('pmN2', [])
pmSecretaire = UserDescriptor('pmSecretaire', [])

developers = data.orgs[0]
developers.n1.append(pmN1)
developers.n2.append(pmN2)
developers.secretaire.append(pmSecretaire)
developers.n1.append(pmManager)
developers.n2.append(pmManager)

data = deepcopy(mc_import_data.data)
# Meeting configurations -------------------------------------------------------
# College communal
collegeMeeting = deepcopy(mc_import_data.collegeMeeting)
collegeMeeting.itemWorkflow = 'meetingitemcpaslalouviere_workflow'
collegeMeeting.meetingWorkflow = 'meetingcpaslalouviere_workflow'
collegeMeeting.itemConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowActions'
collegeMeeting.transitionsForPresentingAnItem = ['proposeToN1', 'proposeToN2', 'proposeToSecretaire',
                                                 'proposeToPresident', 'validate', 'present']
collegeMeeting.onMeetingTransitionItemTransitionToTrigger = ({'meeting_transition': 'freeze',
                                                              'item_transition': 'itemfreeze'},

                                                             {'meeting_transition': 'decide',
                                                              'item_transition': 'itemfreeze'},

                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'itemfreeze'},
                                                             {'meeting_transition': 'close',
                                                              'item_transition': 'accept'},

                                                             {'meeting_transition': 'backToCreated',
                                                              'item_transition': 'backToPresented'},)
collegeMeeting.itemAdviceStates = ['proposed_to_president', ]
collegeMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']
collegeMeeting.workflowAdaptations = []

# Conseil communal
councilMeeting = deepcopy(mc_import_data.councilMeeting)
councilMeeting.itemWorkflow = 'meetingitemcpaslalouviere_workflow'
councilMeeting.meetingWorkflow = 'meetingcpaslalouviere_workflow'
councilMeeting.itemConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowConditions'
councilMeeting.itemActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowActions'
councilMeeting.meetingConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowConditions'
councilMeeting.meetingActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowActions'
councilMeeting.transitionsForPresentingAnItem = ['proposeToN1', 'proposeToN2', 'proposeToSecretaire',
                                                 'proposeToPresident', 'validate', 'present']

councilMeeting.itemAdviceStates = ['proposed_to_president', ]
councilMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']
councilMeeting.workflowAdaptations = []
councilMeeting.itemCopyGroupsStates = []

data.meetingConfigs = (collegeMeeting, councilMeeting)
# ------------------------------------------------------------------------------
