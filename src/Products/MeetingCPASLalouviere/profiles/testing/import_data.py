# -*- coding: utf-8 -*-

from copy import deepcopy
from Products.PloneMeeting.profiles import UserDescriptor
from Products.PloneMeeting.profiles.testing import import_data as pm_import_data
from Products.MeetingCommunes.profiles.testing import import_data as mc_import_data

from Products.MeetingCPASLalouviere.config import LLO_ITEM_CPAS_WF_VALIDATION_LEVELS

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

pmBudgetReviewer1 = UserDescriptor("pmBudgetReviewer1", [])
pmBudgetReviewer2 = UserDescriptor("pmBudgetReviewer2", [])

developers = data.orgs[0]
developers.budgetimpactreviewers.append(pmBudgetReviewer1)
developers.n1.append(pmN1)
developers.n2.append(pmN2)
developers.secretaire.append(pmSecretaire)
developers.n1.append(pmManager)
developers.n2.append(pmManager)

vendors = data.orgs[1]
vendors.budgetimpactreviewers.append(pmBudgetReviewer2)
vendors.n1.append(pmN1)
vendors.n2.append(pmN2)
vendors.secretaire.append(pmSecretaire)
vendors.n1.append(pmManager)
vendors.n2.append(pmManager)
# Meeting configurations -------------------------------------------------------
# College communal
bpMeeting = deepcopy(mc_import_data.collegeMeeting)
bpMeeting.id = 'meeting-config-bp'
bpMeeting.title = 'Bureau Permanent'
bpMeeting.folderTitle = 'Bureau Permanent'
bpMeeting.shortName = 'Bureau'
bpMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_CPAS_WF_VALIDATION_LEVELS)
bpMeeting.itemAdviceStates = ['proposed_to_president', ]
bpMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']

# Conseil communal
casMeeting = deepcopy(bpMeeting)
casMeeting.id = 'meeting-config-cas'
casMeeting.title = 'Conseil Action Sociale'
casMeeting.folderTitle = 'Conseil Action Sociale'
casMeeting.shortName = 'CAS'

data.meetingConfigs = (bpMeeting, casMeeting)
# data.usersOutsideGroups += [pmN1, pmN2, pmSecretaire]
# ------------------------------------------------------------------------------
