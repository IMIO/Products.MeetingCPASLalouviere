# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
# File: adapters.py
#
# Copyright (c) 2014 by Imio.be
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# ------------------------------------------------------------------------------
from appy.gen import No
from AccessControl import getSecurityManager, ClassSecurityInfo
from Globals import InitializeClass
from zope.interface import implements
from Products.CMFCore.permissions import ReviewPortalContent, ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from Products.PloneMeeting.MeetingItem import MeetingItem, \
    MeetingItemWorkflowConditions, MeetingItemWorkflowActions
from Products.PloneMeeting.utils import checkPermission, prepareSearchValue
from Products.PloneMeeting.Meeting import MeetingWorkflowActions, \
    MeetingWorkflowConditions, Meeting
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.interfaces import IMeetingCustom, IMeetingItemCustom, \
    IMeetingConfigCustom
from Products.MeetingCPASLalouviere.interfaces import \
    IMeetingItemPBLalouviereWorkflowConditions, IMeetingItemPBLalouviereWorkflowActions,\
    IMeetingPBLalouviereWorkflowConditions, IMeetingPBLalouviereWorkflowActions
from Products.PloneMeeting.model import adaptations

# Names of available workflow adaptations.
customWfAdaptations = ('return_to_proposing_group', )
MeetingConfig.wfAdaptations = customWfAdaptations
# configure parameters for the returned_to_proposing_group wfAdaptation
# we keep also 'itemfrozen' and 'itempublished' in case this should be activated for meeting-config-college...
RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = ('presented', 'itemfrozen', )
adaptations.RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES = RETURN_TO_PROPOSING_GROUP_FROM_ITEM_STATES
RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = {
    # view permissions
    'Access contents information':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'View':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read decision':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read optional advisers':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read decision annex':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    'PloneMeeting: Read item observations':
    ('Manager', 'MeetingManager', 'MeetingMember', 'MeetingN1', 'MeetingN2',
     'MeetingSecretaire', 'MeetingReviewer', 'MeetingObserverLocal', 'Reader', ),
    # edit permissions
    'Modify portal content':
    ('Manager', 'MeetingMember', 'MeetingN2', 'MeetingManager', ),
    'PloneMeeting: Write decision':
    ('Manager', 'MeetingMember', 'MeetingN2', 'MeetingManager', ),
    'Review portal content':
    ('Manager', 'MeetingMember', 'MeetingN2', 'MeetingManager', ),
    'Add portal content':
    ('Manager', 'MeetingMember', 'MeetingN2', 'MeetingManager', ),
    'PloneMeeting: Add annex':
    ('Manager', 'MeetingMember', 'MeetingN2', 'MeetingManager', ),
    'PloneMeeting: Add MeetingFile':
    ('Manager', 'MeetingMember', 'MeetingN2', 'MeetingManager', ),
    'PloneMeeting: Write decision annex':
    ('Manager', 'MeetingMember', 'MeetingN2', 'MeetingManager', ),
    'PloneMeeting: Write optional advisers':
    ('Manager', 'MeetingMember', 'MeetingN2', 'MeetingManager', ),
    'PloneMeeting: Write optional advisers':
    ('Manager', 'MeetingMember', 'MeetingN2', 'MeetingManager', ),
    # MeetingManagers edit permissions
    'Delete objects':
    ('Manager', 'MeetingMember', 'MeetingN2', 'MeetingManager', ),
    'PloneMeeting: Write item observations':
    ('Manager', 'MeetingMember', 'MeetingN2', 'MeetingManager', ),
}

adaptations.RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS = RETURN_TO_PROPOSING_GROUP_CUSTOM_PERMISSIONS


# ------------------------------------------------------------------------------


class CustomMeeting(Meeting):
    '''Adapter that adapts a meeting implementing IMeeting to the
       interface IMeetingCustom.'''

    implements(IMeetingCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    # Implements here methods that will be used by templates
    security.declarePublic('getPrintableItems')
    def getPrintableItems(self, itemUids, late=False, ignore_review_states=[],
                          privacy='*', oralQuestion='both', categories=[],
                          excludedCategories=[], firstNumber=1, renumber=False):
        '''Returns a list of items.
           An extra list of review states to ignore can be defined.
           A privacy can also be given, and the fact that the item is an
           oralQuestion or not (or both).
           Some specific categories can be given or some categories to exchude.
           These 2 parameters are exclusive.  If renumber is True, a list of tuple
           will be return with first element the number and second element, the item.
           In this case, the firstNumber value can be used.'''
        # We just filter ignore_review_states here and privacy and call
        # getItemsInOrder(uids), passing the correct uids and removing empty
        # uids.
        # privacy can be '*' or 'public' or 'secret'
        # oralQuestion can be 'both' or False or True
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)
        #no filtering, return the items ordered
        if not categories and not ignore_review_states and privacy == '*' and oralQuestion == 'both':
            return self.context.getItemsInOrder(late=late, uids=itemUids)
        # Either, we will have to filter the state here and check privacy
        filteredItemUids = []
        uid_catalog = self.context.uid_catalog
        for itemUid in itemUids:
            obj = uid_catalog(UID=itemUid)[0].getObject()
            if obj.queryState() in ignore_review_states:
                continue
            elif not (privacy == '*' or obj.getPrivacy() == privacy):
                continue
            elif not (oralQuestion == 'both' or obj.getOralQuestion() == oralQuestion):
                continue
            elif categories and not obj.getCategory() in categories:
                continue
            elif excludedCategories and obj.getCategory() in excludedCategories:
                continue
            filteredItemUids.append(itemUid)
        #in case we do not have anything, we return an empty list
        if not filteredItemUids:
            return []
        else:
            items = self.context.getItemsInOrder(late=late, uids=filteredItemUids)
            if renumber:
                #return a list of tuple with first element the number and second
                #element the item itself
                i = firstNumber
                res = []
                for item in items:
                    res.append((i, item))
                    i = i + 1
                items = res
            return items

    def _getGroupIndex(self, group, groups, groupPrefixes):
        '''Is p_group among the list of p_groups? If p_group is not among
           p_groups but another group having the same prefix as p_group
           (the list of prefixes is given by p_groupPrefixes), we must conclude
           that p_group is among p_groups. res is -1 if p_group is not
           among p_group; else, the method returns the index of p_group in
           p_groups.'''
        prefix = self._getAcronymPrefix(group, groupPrefixes)
        if not prefix:
            if group not in groups:
                return -1
            else:
                return groups.index(group)
        else:
            for gp in groups:
                if gp.getAcronym().startswith(prefix):
                    return groups.index(gp)
            return -1

    def _insertGroupInCategory(self, categoryList, meetingGroup, groupPrefixes, groups, item=None):
        '''Inserts a group list corresponding to p_meetingGroup in the given
           p_categoryList, following meeting group order as defined in the
           main configuration (groups from the config are in p_groups).
           If p_item is specified, the item is appended to the group list.'''
        usedGroups = [g[0] for g in categoryList[1:]]
        groupIndex = self._getGroupIndex(meetingGroup, usedGroups, groupPrefixes)
        if groupIndex == -1:
            # Insert the group among used groups at the right place.
            groupInserted = False
            i = -1
            for usedGroup in usedGroups:
                i += 1
                if groups.index(meetingGroup) < groups.index(usedGroup):
                    if item:
                        categoryList.insert(i+1, [meetingGroup, item])
                    else:
                        categoryList.insert(i+1, [meetingGroup])
                    groupInserted = True
                    break
            if not groupInserted:
                if item:
                    categoryList.append([meetingGroup, item])
                else:
                    categoryList.append([meetingGroup])
        else:
            # Insert the item into the existing group.
            if item:
                categoryList[groupIndex+1].append(item)

    def _insertItemInCategory(self, categoryList, item, byProposingGroup, groupPrefixes, groups):
        '''This method is used by the next one for inserting an item into the
           list of all items of a given category. if p_byProposingGroup is True,
           we must add it in a sub-list containing items of a given proposing
           group. Else, we simply append it to p_category.'''
        if not byProposingGroup:
            categoryList.append(item)
        else:
            group = item.getProposingGroup(True)
            self._insertGroupInCategory(categoryList, group, groupPrefixes,
                                        groups, item)

    def getPrintableItemsByCategory(self, itemUids=[], late=False,
                                    ignore_review_states=[], by_proposing_group=False, group_prefixes={},
                                    includeEmptyCategories=False, includeEmptyGroups=False):
        '''Returns a list of (late-)items (depending on p_late) ordered by
           category. Items being in a state whose name is in
           p_ignore_review_state will not be included in the result.
           If p_by_proposing_group is True, items are grouped by proposing group
           within every category. In this case, specifying p_group_prefixes will
           allow to consider all groups whose acronym starts with a prefix from
           this param prefix as a unique group. p_group_prefixes is a dict whose
           keys are prefixes and whose values are names of the logical big
           groups. If p_includeEmptyCategories is True, categories for which no
           item is defined are included nevertheless. If p_includeEmptyGroups
           is True, proposing groups for which no item is defined are included
           nevertheless.'''
        # The result is a list of lists, where every inner list contains:
        # - at position 0: the category object (MeetingCategory or MeetingGroup)
        # - at position 1 to n: the items in this category
        # If by_proposing_group is True, the structure is more complex.
        # Every inner list contains:
        # - at position 0: the category object
        # - at positions 1 to n: inner lists that contain:
        #   * at position 0: the proposing group object
        #   * at positions 1 to n: the items belonging to this group.
        res = []
        items = []
        previousCatId = None
        # Retrieve the list of items
        for elt in itemUids:
            if elt == '':
                itemUids.remove(elt)
        items = self.context.getItemsInOrder(late=late, uids=itemUids)
        if by_proposing_group:
            groups = self.context.portal_plonemeeting.getActiveGroups()
        else:
            groups = None
        if items:
            for item in items:
                # Check if the review_state has to be taken into account
                if item.queryState() in ignore_review_states:
                    continue
                currentCat = item.getCategory(theObject=True)
                currentCatId = currentCat.getId()
                if currentCatId != previousCatId:
                    # Add the item to a new category, excepted if the
                    # category already exists.
                    catExists = False
                    for catList in res:
                        if catList[0] == currentCat:
                            catExists = True
                            break
                    if catExists:
                        self._insertItemInCategory(catList, item, by_proposing_group, group_prefixes, groups)
                    else:
                        res.append([currentCat])
                        self._insertItemInCategory(res[-1], item, by_proposing_group, group_prefixes, groups)
                    previousCatId = currentCatId
                else:
                    # Append the item to the same category
                    self._insertItemInCategory(res[-1], item, by_proposing_group, group_prefixes, groups)
        if includeEmptyCategories:
            meetingConfig = self.context.portal_plonemeeting.getMeetingConfig(
                self.context)
            allCategories = meetingConfig.getCategories()
            usedCategories = [elem[0] for elem in res]
            for cat in allCategories:
                if cat not in usedCategories:
                    # Insert the category among used categories at the right
                    # place.
                    categoryInserted = False
                    for i in range(len(usedCategories)):
                        if allCategories.index(cat) < \
                           allCategories.index(usedCategories[i]):
                            usedCategories.insert(i, cat)
                            res.insert(i, [cat])
                            categoryInserted = True
                            break
                    if not categoryInserted:
                        usedCategories.append(cat)
                        res.append([cat])
        if by_proposing_group and includeEmptyGroups:
            # Include, in every category list, not already used groups.
            # But first, compute "macro-groups": we will put one group for
            # every existing macro-group.
            macroGroups = []  # Contains only 1 group of every "macro-group"
            consumedPrefixes = []
            for group in groups:
                prefix = self._getAcronymPrefix(group, group_prefixes)
                if not prefix:
                    group._v_printableName = group.Title()
                    macroGroups.append(group)
                else:
                    if prefix not in consumedPrefixes:
                        consumedPrefixes.append(prefix)
                        group._v_printableName = group_prefixes[prefix]
                        macroGroups.append(group)
            # Every category must have one group from every macro-group
            for catInfo in res:
                for group in macroGroups:
                    self._insertGroupInCategory(catInfo, group, group_prefixes,
                                                groups)
                    # The method does nothing if the group (or another from the
                    # same macro-group) is already there.
        return res

    security.declarePublic('showAllItemsAtOnce')
    def showAllItemsAtOnce(self):
        """
          Monkeypatch for hiding the allItemsAtOnce field
        """
        return False
    Meeting.showAllItemsAtOnce = showAllItemsAtOnce


# ------------------------------------------------------------------------------
class CustomMeetingItem(MeetingItem):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCustom.'''
    implements(IMeetingItemCustom)
    security = ClassSecurityInfo()

    customItemTransitionsForPresentingIt = ('proposeToN1', 'proposeToN2', 'proposeToSecretaire', 'proposeToPresident',
                                            'validate', 'present', )
    MeetingItem.itemTransitionsForPresentingIt = customItemTransitionsForPresentingIt

    customMeetingAlreadyFrozenStates = ('frozen', 'decided', )
    MeetingItem.meetingAlreadyFrozenStates = customMeetingAlreadyFrozenStates

    def __init__(self, item):
        self.context = item

    security.declarePublic('getMeetingsAcceptingItems')
    def getMeetingsAcceptingItems(self):
        '''Overrides the default method so we only display meetings that are
           in the 'created' or 'frozen' state.'''
        pmtool = getToolByName(self.context, "portal_plonemeeting")
        catalogtool = getToolByName(self.context, "portal_catalog")
        meetingPortalType = pmtool.getMeetingConfig(self.context).getMeetingTypeName()
        # If the current user is a meetingManager (or a Manager),
        # he is able to add a meetingitem to a 'decided' meeting.
        review_state = ['created', 'frozen', ]
        member = self.context.portal_membership.getAuthenticatedMember()
        if member.has_role('MeetingManager') or member.has_role('Manager'):
            review_state.extend(('decided', 'in_committee', 'in_council', ))
        res = catalogtool.unrestrictedSearchResults(
            portal_type=meetingPortalType,
            review_state=review_state,
            sort_on='getDate')
        # Frozen meetings may still accept "late" items.
        return res


# ------------------------------------------------------------------------------
class CustomMeetingConfig(MeetingConfig):
    '''Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom.'''

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    #we need to be able to give an advice in the initial_state for Council...
    from Products.PloneMeeting.MeetingConfig import MeetingConfig
    MeetingConfig.listItemStatesInitExcepted = MeetingConfig.listItemStates

    security.declarePublic('searchReviewableItems')
    def searchReviewableItems(self, sortKey, sortOrder, filterKey, filterValue, **kwargs):
        '''Returns a list of items that the user could review.'''
        member = self.portal_membership.getAuthenticatedMember()
        groups = self.portal_groups.getGroupsForPrincipal(member)
        #the logic is :
        #a user is reviewer for his level of hierarchy and every levels below in a group
        #so find the different groups (a user could be divisionhead in groupA and director in groupB)
        #and find the different states we have to search for this group (proposingGroup of the item)
        reviewSuffixes = ('_reviewers', '_secretaire', '_n1', '_n2', )
        statesMapping = {
            '_reviewers': ('proposed_to_n1', 'proposed_to_n2', 'proposed_to_secretaire',
            'proposed_to_president'),
            '_secretaire': ('proposed_to_n1', 'proposed_to_n2', 'proposed_to_secretaire'),
            '_n2': ('proposed_to_n1', 'proposed_to_n2'),
            '_n1': 'proposed_to_servicehead', }
        foundGroups = {}
        #check that we have a real PM group, not "echevins", or "Administrators"
        for group in groups:
            realPMGroup = False
            for reviewSuffix in reviewSuffixes:
                if group.endswith(reviewSuffix):
                    realPMGroup = True
                    break
            if not realPMGroup:
                continue
            #remove the suffix
            groupPrefix = '_'.join(group.split('_')[:-1])
            if not groupPrefix in foundGroups:
                foundGroups[groupPrefix] = ''
        #now we have the differents services (equal to the MeetingGroup id) the user is in
        strgroups = str(groups)
        for foundGroup in foundGroups:
            for reviewSuffix in reviewSuffixes:
                if "%s%s" % (foundGroup, reviewSuffix) in strgroups:
                    foundGroups[foundGroup] = reviewSuffix
                    break
        #now we have in the dict foundGroups the group the user is in in the key and the highest level in the value
        res = []
        for foundGroup in foundGroups:
            params = {'Type': unicode(self.getItemTypeName(), 'utf-8'),
                      'getProposingGroup': foundGroup,
                      'review_state': statesMapping[foundGroups[foundGroup]],
                      'sort_on': sortKey,
                      'sort_order': sortOrder}
            # Manage filter
            if filterKey:
                params[filterKey] = prepareSearchValue(filterValue)
            # update params with kwargs
            params.update(kwargs)
            # Perform the query in portal_catalog
            brains = self.portal_catalog(**params)
            res.extend(brains)
        return res
    MeetingConfig.searchReviewableItems = searchReviewableItems


# ------------------------------------------------------------------------------
class MeetingPBLalouviereWorkflowActions(MeetingWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCollegeWorkflowActions'''

    implements(IMeetingPBLalouviereWorkflowActions)
    security = ClassSecurityInfo()

    def _adaptEveryItemsOnMeetingClosure(self):
        """Helper method for accepting every items."""
        # Every item that is not decided will be automatically set to "accepted"
        for item in self.context.getAllItems():
            if item.queryState() == 'presented':
                self.context.portal_workflow.doActionFor(item, 'itemfreeze')
            if item.queryState() in ['itemfrozen', 'pre_accepted', ]:
                self.context.portal_workflow.doActionFor(item, 'accept')

    security.declarePrivate('doDecide')
    def doDecide(self, stateChange):
        '''We pass every item that is 'presented' in the 'itemfrozen'
           state.  It is the case for late items.'''
        for item in self.context.getAllItems(ordered=False):
            if item.queryState() == 'presented':
                self.context.portal_workflow.doActionFor(item, 'itemfreeze')

    security.declarePrivate('doFreeze')
    def doFreeze(self, stateChange):
        '''When freezing the meeting, every items must be automatically set to
           "itemfrozen".'''
        for item in self.context.getAllItems(ordered=True):
            if item.queryState() == 'presented':
                self.context.portal_workflow.doActionFor(item, 'itemfreeze')

    security.declarePrivate('doBackToCreated')
    def doBackToCreated(self, stateChange):
        '''When a meeting go back to the "created" state, for example the
           meeting manager wants to add an item, we do not do anything.'''
        pass


# ------------------------------------------------------------------------------
class MeetingPBLalouviereWorkflowConditions(MeetingWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingCollegeWorkflowConditions'''

    implements(IMeetingPBLalouviereWorkflowConditions)
    security = ClassSecurityInfo()

    security.declarePublic('mayFreeze')
    def mayFreeze(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            res = True  # At least at present
            if not self.context.getRawItems():
                res = No(self.context.utranslate('item_required_to_publish'))
        return res

    security.declarePublic('mayClose')
    def mayClose(self):
        res = False
        # The user just needs the "Review portal content" permission on the
        # object to close it.
        if checkPermission(ReviewPortalContent, self.context):
            res = True
        return res

    security.declarePublic('mayDecide')
    def mayDecide(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context) and \
           (not self._allItemsAreDelayed()):
            res = True
        return res

    security.declarePublic('mayChangeItemsOrder')
    def mayChangeItemsOrder(self):
        '''We can change the order if the meeting is not closed'''
        res = False
        if checkPermission(ModifyPortalContent, self.context) and \
           self.context.queryState() not in ('closed'):
            res = True
        return res

    def mayCorrect(self):
        '''Take the default behaviour except if the meeting is frozen
           we still have the permission to correct it.'''
        from Products.PloneMeeting.Meeting import MeetingWorkflowConditions
        res = MeetingWorkflowConditions.mayCorrect(self)
        currentState = self.context.queryState()
        if not res is True and currentState == "frozen":
            # Change the behaviour for being able to correct a frozen meeting
            # back to created.
            if checkPermission(ReviewPortalContent, self.context):
                return True
        return res


# ------------------------------------------------------------------------------
class MeetingItemPBLalouviereWorkflowActions(MeetingItemWorkflowActions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemPBWorkflowActions'''

    implements(IMeetingItemPBLalouviereWorkflowActions)
    security = ClassSecurityInfo()

    security.declarePrivate('doAccept_but_modify')
    def doAccept_but_modify(self, stateChange):
        pass

    security.declarePrivate('doPreAccept')
    def doPreAccept(self, stateChange):
        pass

    security.declarePrivate('doRemove')
    def doRemove(self, stateChange):
        pass

    security.declarePrivate('doProposeToN1')
    def doProposeToN1(self, stateChange):
        pass

    security.declarePrivate('doWaitAdvices')
    def doWaitAdvices(self, stateChange):
        pass

    security.declarePrivate('doProposeToSecretaire')
    def doProposeToSecretaire(self, stateChange):
        pass

    security.declarePrivate('doProposeToN2')
    def doProposeToN2(self, stateChange):
        pass

    security.declarePrivate('doProposeToPresident')
    def doProposeToPresident(self, stateChange):
        pass

    security.declarePrivate('doValidateByBudgetImpactReviewer')
    def doValidateByBudgetImpactReviewer(self, stateChange):
        pass

    security.declarePrivate('doProposeToBudgetImpactReviewer')
    def doProposeToBudgetImpactReviewer(self, stateChange):
        pass

    security.declarePrivate('doAsk_advices_by_itemcreator')
    def doAsk_advices_by_itemcreator(self, stateChange):
        pass


# ------------------------------------------------------------------------------
class MeetingItemPBLalouviereWorkflowConditions(MeetingItemWorkflowConditions):
    '''Adapter that adapts a meeting item implementing IMeetingItem to the
       interface IMeetingItemCollegeWorkflowConditions'''

    implements(IMeetingItemPBLalouviereWorkflowConditions)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item  # Implements IMeetingItem
        self.sm = getSecurityManager()
        self.useHardcodedTransitionsForPresentingAnItem = True
        self.transitionsForPresentingAnItem = ('proposeToN1',
                                               'proposeToN2',
                                               'proposeToSecretaire',
                                               'proposeToPresident',
                                               'validate',
                                               'present')

    security.declarePublic('mayDecide')
    def mayDecide(self):
        '''We may decide an item if the linked meeting is in the 'decided'
           state.'''
        res = False
        meeting = self.context.getMeeting()
        if checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['decided', 'closed']):
            res = True
        return res

    security.declarePublic('mayValidate')
    def mayValidate(self):
        """
          Either the alderman or the MeetingManager can validate
          The MeetingManager can bypass the validation process and validate an item
          that is in the state 'itemcreated'
        """
        res = False
        #first of all, the use must have the 'Review portal content permission'
        if checkPermission(ReviewPortalContent, self.context):
            res = True
            #if the current item state is 'itemcreated', only the MeetingManager can validate
            member = self.context.portal_membership.getAuthenticatedMember()
            if self.context.queryState() in ('itemcreated',) and not \
               (member.has_role('MeetingManager') or member.has_role('Manager')):
                res = False
        return res

    security.declarePublic('mayFreeze')
    def mayFreeze(self):
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            if self.context.hasMeeting() and \
               (self.context.getMeeting().queryState() in ('frozen', 'decided', 'closed')):
                res = True
        return res

    security.declarePublic('mayCorrect')
    def mayCorrect(self):
        # Check with the default PloneMeeting method and our test if res is
        # False. The diffence here is when we correct an item from itemfrozen to
        # presented, we have to check if the Meeting is in the "created" state
        # and not "published".
        res = MeetingItemWorkflowConditions.mayCorrect(self)
        # Manage our own behaviour now when the item is linked to a meeting,
        # a MeetingManager can correct anything except if the meeting is closed
        if not res is True:
            if checkPermission(ReviewPortalContent, self.context):
                # Get the meeting
                meeting = self.context.getMeeting()
                if meeting:
                    # Meeting can be None if there was a wf problem leading
                    # an item to be in a "presented" state with no linked
                    # meeting.
                    meetingState = meeting.queryState()
                    # A user having ReviewPortalContent permission can correct
                    # an item in any case except if the meeting is closed.
                    if meetingState != 'closed':
                        res = True
                else:
                    res = True
        return res

    security.declarePublic('mayWaitAdvices')
    def mayWaitAdvices(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToN1')
    def mayProposeToN1(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToN2')
    def mayProposeToN2(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToSecretaire')
    def mayProposeToSecretaire(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToPresident')
    def mayProposeToPresident(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
            res = True
            #if the current item state is 'itemcreated', only the MeetingManager can validate
            member = self.context.portal_membership.getAuthenticatedMember()
            if self.context.queryState() in ('proposed_to_n1',) and not \
               (member.has_role('MeetingReviewer') or member.has_role('Manager')):
                res = False
        return res

    security.declarePublic('mayRemove')
    def mayRemove(self):
        """
          We may remove an item if the linked meeting is in the 'decided'
          state.  For now, this is the same behaviour as 'mayDecide'
        """
        res = False
        meeting = self.context.getMeeting()
        if checkPermission(ReviewPortalContent, self.context) and \
           meeting and (meeting.queryState() in ['decided', 'closed']):
            res = True
        return res

    security.declarePublic('mayValidateByBudgetImpactReviewer')
    def mayValidateByBudgetImpactReviewer(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

    security.declarePublic('mayProposeToBudgetImpactReviewer')
    def mayProposeToBudgetImpactReviewer(self):
        """
          Check that the user has the 'Review portal content'
        """
        res = False
        if checkPermission(ReviewPortalContent, self.context):
                res = True
        return res

# ------------------------------------------------------------------------------
InitializeClass(CustomMeetingItem)
InitializeClass(CustomMeeting)
InitializeClass(CustomMeetingConfig)
InitializeClass(MeetingPBLalouviereWorkflowActions)
InitializeClass(MeetingPBLalouviereWorkflowConditions)
InitializeClass(MeetingItemPBLalouviereWorkflowActions)
InitializeClass(MeetingItemPBLalouviereWorkflowConditions)
# ------------------------------------------------------------------------------
