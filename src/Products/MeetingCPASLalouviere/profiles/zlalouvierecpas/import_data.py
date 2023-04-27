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
pmN11 = UserDescriptor('pmN11', [])
pmN12 = UserDescriptor('pmN12', [])
pmN21 = UserDescriptor('pmN21', [])
pmN22 = UserDescriptor('pmN22', [])
pmSecretaire = UserDescriptor('pmSecretaire', [])

developers = data.orgs[0]
developers.n1.append(pmN11)
developers.n1.append(pmReviewerLevel1)
developers.n1.append(pmManager)
developers.n2.append(pmN21)
developers.n2.append(pmReviewerLevel2)
developers.n2.append(pmManager)
developers.secretaire.append(pmSecretaire)
developers.secretaire.append(pmManager)
developers.president.append(pmReviewer1)
developers.president.append(pmManager)

vendors = data.orgs[1]
vendors.n1.append(pmN12)
vendors.n1.append(pmReviewerLevel1)
vendors.n1.append(pmManager)
vendors.n2.append(pmN22)
vendors.n2.append(pmReviewerLevel2)
vendors.n2.append(pmManager)
vendors.secretaire.append(pmSecretaire)
vendors.secretaire.append(pmManager)
vendors.president.append(pmReviewer2)
vendors.president.append(pmManager)

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
casMeeting = deepcopy(mc_import_data.councilMeeting)
casMeeting.id = 'meeting-config-cas'
casMeeting.title = 'Conseil Action Sociale'
casMeeting.folderTitle = 'Conseil Action Sociale'
casMeeting.shortName = 'CAS'
casMeeting.itemWFValidationLevels = deepcopy(LLO_ITEM_CPAS_WF_VALIDATION_LEVELS)
casMeeting.itemAdviceStates = ['proposed_to_president', ]
casMeeting.itemAdviceEditStates = ['proposed_to_president', 'validated']

data.meetingConfigs = (bpMeeting, casMeeting)
# data.usersOutsideGroups += [pmN1, pmN2, pmSecretaire]
# ------------------------------------------------------------------------------
