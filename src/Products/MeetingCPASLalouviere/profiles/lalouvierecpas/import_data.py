# -*- coding: utf-8 -*-
from Products.PloneMeeting.profiles import *
from Products.MeetingCPASLalouviere.config import *

# File types -------------------------------------------------------------------
annexe = MeetingFileTypeDescriptor('annexe', 'Annexe', 'attach.png', '')
annexeBudget = MeetingFileTypeDescriptor('annexeBudget', 'Article Budgétaire', 'budget.png', '')
annexeCahier = MeetingFileTypeDescriptor('annexeCahier', 'Cahier des Charges', 'cahier.gif', '')
annexeDecision = MeetingFileTypeDescriptor('annexeDecision', 'Annexe à la décision', 'attach.png', '', True)
# Categories -------------------------------------------------------------------
recurring = CategoryDescriptor('recurrents', 'Récurrents')
categories = [recurring,
              CategoryDescriptor('travaux', 'Travaux'),
              CategoryDescriptor('urbanisme', 'Urbanisme'),
              CategoryDescriptor('comptabilite', 'Comptabilité/Recettes'),
              CategoryDescriptor('personnel', 'Personnel'),
              CategoryDescriptor('population', 'Population/Etat-civil'),
              CategoryDescriptor('locations', 'Locations'),
              CategoryDescriptor('divers', 'Divers'),
             ]

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('agenda', 'Ordre du jour')
agendaTemplate.podTemplate = 'Agenda.odt'
agendaTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                              'here.portal_membership.' \
                              'getAuthenticatedMember().has_role("' \
                              'MeetingManager")'

agendaTemplatePDF = PodTemplateDescriptor('agendapdf', 'Ordre du jour')
agendaTemplatePDF.podTemplate = 'Agenda.odt'
agendaTemplatePDF.podFormat = 'pdf'
agendaTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                  'here.portal_membership.' \
                                  'getAuthenticatedMember().has_role("' \
                                  'MeetingManager")'

decisionsTemplate = PodTemplateDescriptor('decisions', 'Procès-verbal')
decisionsTemplate.podTemplate = 'Decisions.odt'
decisionsTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_membership.' \
                                 'getAuthenticatedMember().has_role("' \
                                 'MeetingManager")'

decisionsTemplatePDF = PodTemplateDescriptor('decisionspdf', 'Procès-verbal')
decisionsTemplatePDF.podTemplate = 'Decisions.odt'
decisionsTemplatePDF.podFormat = 'pdf'
decisionsTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                    'here.portal_membership.' \
                                    'getAuthenticatedMember().has_role("' \
                                    'MeetingManager")'
decisionsByCatTemplate = PodTemplateDescriptor('decisionsbycat', 'PV avec catégories')
decisionsByCatTemplate.podTemplate = 'DecisionsWithItemsByCategory.odt'
decisionsByCatTemplate.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                 'here.portal_membership.' \
                                 'getAuthenticatedMember().has_role("' \
                                 'MeetingManager")'

decisionsByCatTemplatePDF = PodTemplateDescriptor('decisionsbycatpdf', 'PV avec catégories')
decisionsByCatTemplatePDF.podTemplate = 'DecisionsWithItemsByCategory.odt'
decisionsByCatTemplatePDF.podFormat = 'pdf'
decisionsByCatTemplatePDF.podCondition = 'python:(here.meta_type=="Meeting") and ' \
                                    'here.portal_membership.' \
                                    'getAuthenticatedMember().has_role("' \
                                    'MeetingManager")'

itemTemplate = PodTemplateDescriptor('item', 'Délibération')
itemTemplate.podTemplate = 'MeetingItem.odt'
itemTemplate.podCondition = 'python:here.meta_type=="MeetingItem"'

itemTemplatePDF = PodTemplateDescriptor('itempdf', 'Délibération')
itemTemplatePDF.podTemplate = 'MeetingItem.odt'
itemTemplatePDF.podFormat = 'pdf'
itemTemplatePDF.podCondition = 'python:here.meta_type=="MeetingItem"'

allTemplates = [agendaTemplate, agendaTemplatePDF,
                decisionsTemplate, decisionsTemplatePDF,
                decisionsByCatTemplate, decisionsByCatTemplatePDF,
                itemTemplate, itemTemplatePDF]

# Users and groups -------------------------------------------------------------
secretaire = UserDescriptor('secretaire', ['MeetingManager'], email="test@test.be")
agentInfo = UserDescriptor('agentInfo', [], email="test@test.be")
agentCompta = UserDescriptor('agentCompta', [], email="test@test.be")
agentPers = UserDescriptor('agentPers', [], email="test@test.be")
agentTrav = UserDescriptor('agentTrav', [], email="test@test.be")
chefPers = UserDescriptor('chefPers', [], email="test@test.be")
chefCompta = UserDescriptor('chefCompta', [], email="test@test.be")
echevinPers = UserDescriptor('echevinPers', [], email="test@test.be")
emetteuravisPers = UserDescriptor('emetteuravisPers', [], email="test@test.be")
groups = [
           GroupDescriptor('secretariat', 'Secretariat communal', 'Secr'),
           GroupDescriptor('informatique', 'Service informatique', 'Info'),
           GroupDescriptor('personnel', 'Service du personnel', 'Pers'),
           GroupDescriptor('comptabilite', 'Service comptabilité', 'Compt', givesMandatoryAdviceOn='python:True'),
           GroupDescriptor('travaux', 'Service travaux', 'Trav'),
         ]
#add new rôles
for groupDescr in groups:
    for groupSuffix in MEETINGROLES.iterkeys():
        if not getattr(groupDescr, groupSuffix, None):
            setattr(groupDescr, groupSuffix, [])

# MeetingManager
groups[0].creators.append(secretaire)
groups[0].reviewers.append(secretaire)
groups[0].observers.append(secretaire)
groups[0].advisers.append(secretaire)

groups[1].creators.append(agentInfo)
groups[1].creators.append(secretaire)
groups[1].reviewers.append(agentInfo)
groups[1].reviewers.append(secretaire)
groups[1].observers.append(agentInfo)
groups[1].advisers.append(agentInfo)

groups[2].creators.append(agentPers)
groups[2].observers.append(agentPers)
groups[2].creators.append(secretaire)
groups[2].reviewers.append(secretaire)
groups[2].creators.append(chefPers)
groups[2].reviewers.append(chefPers)
groups[2].observers.append(chefPers)
groups[2].observers.append(echevinPers)
groups[2].advisers.append(emetteuravisPers)

groups[3].creators.append(agentCompta)
groups[3].creators.append(chefCompta)
groups[3].creators.append(secretaire)
groups[3].reviewers.append(chefCompta)
groups[3].reviewers.append(secretaire)
groups[3].observers.append(agentCompta)
groups[3].advisers.append(chefCompta)

groups[4].creators.append(agentTrav)
groups[4].creators.append(secretaire)
groups[4].reviewers.append(agentTrav)
groups[4].reviewers.append(secretaire)
groups[4].observers.append(agentTrav)
groups[4].advisers.append(agentTrav)
# Meeting configurations -------------------------------------------------------
# college
collegeMeeting = MeetingConfigDescriptor(
    'meeting-config-bp', 'Bureau permanent',
    'Bureau permanent', isDefault=True)
collegeMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                           'Charles Exemple - 1er Echevin,\n' \
                           'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                           'Jacqueline Exemple, Responsable du CPAS'
collegeMeeting.signatures = 'Pierre Dupont, Bourgmestre - Charles Exemple, 1er Echevin'
collegeMeeting.categories = categories
collegeMeeting.shortName = 'Pb'
collegeMeeting.meetingFileTypes = [annexe, annexeBudget, annexeCahier, annexeDecision]
collegeMeeting.itemWorkflow = 'meetingitembplalouviere_workflow'
collegeMeeting.meetingWorkflow = 'meetingbplalouviere_workflow'
collegeMeeting.itemConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingItemPBLalouviereWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingCPASLalouviere.interfaces.IMeetingPBLalouviereWorkflowActions'
collegeMeeting.itemTopicStates = ('itemcreated', 'proposedToN1', 'proposedToN2', 'proposedToPresident', 'proposedToSecretaire', 'validated', 'presented', 'itemfrozen', 'accepted', 'refused', 'delayed', 'pre_accepted', 'removed',)
collegeMeeting.meetingTopicStates = ('created', 'frozen')
collegeMeeting.decisionTopicStates = ('decided', 'closed')
collegeMeeting.itemAdviceStates = ('validated',)
collegeMeeting.recordItemHistoryStates = ['',]
collegeMeeting.maxShownMeetings = 5
collegeMeeting.maxDaysDecisions = 60
collegeMeeting.meetingAppDefaultView = 'topic_searchmyitems'
collegeMeeting.itemDocFormats = ('odt', 'pdf')
collegeMeeting.meetingDocFormats = ('odt', 'pdf')
collegeMeeting.useAdvices = True
collegeMeeting.useCopies = True
collegeMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'), groups[1].getIdSuffixed('reviewers'), groups[2].getIdSuffixed('reviewers'), groups[4].getIdSuffixed('reviewers')]
collegeMeeting.podTemplates = allTemplates
collegeMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance antérieure',
        description='Approuve le procès-verbal de la séance antérieure',
        category='recurrents',
        proposingGroup='secretariat',
        decision='Procès-verbal approuvé'),
    RecurringItemDescriptor(
        id='recurringofficialreport1',
        title='Autorise et signe les bons de commande de la semaine',
        description='Autorise et signe les bons de commande de la semaine',
        category='recurrents',
        proposingGroup='secretariat',
        decision='Bons de commande signés'),
    RecurringItemDescriptor(
        id='recurringofficialreport2',
        title='Ordonnance et signe les mandats de paiement de la semaine',
        description='Ordonnance et signe les mandats de paiement de la semaine',
        category='recurrents',
        proposingGroup='secretariat',
        decision='Mandats de paiement de la semaine approuvés'),
    ]
data = PloneMeetingConfiguration(
           meetingFolderTitle='Mes séances',
           meetingConfigs=(collegeMeeting,),
           groups=groups)
data.unoEnabledPython='/usr/bin/python'
# ------------------------------------------------------------------------------
