# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 by Imio.be
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

from DateTime import DateTime
from Products.MeetingCommunes.tests.helpers import MeetingCommunesTestingHelpers


class MeetingCPASLalouviereTestingHelpers(MeetingCommunesTestingHelpers):
    '''Override some values of PloneMeetingTestingHelpers.'''

    TRANSITIONS_FOR_PROPOSING_ITEM_1 = ('proposeToN1',
                                        'proposeToN2',
                                        'proposeToSecretaire',
                                        'proposeToPresident', )
    TRANSITIONS_FOR_PROPOSING_ITEM_2 = ('proposeToN1',
                                        'proposeToPresident', )
    TRANSITIONS_FOR_VALIDATING_ITEM_1 = ('proposeToN1',
                                         'proposeToN2',
                                         'proposeToSecretaire',
                                         'proposeToPresident',
                                         'validate', )
    TRANSITIONS_FOR_VALIDATING_ITEM_2 = ('validate', )
    TRANSITIONS_FOR_PRESENTING_ITEM_1 = ('proposeToN1',
                                         'proposeToN2',
                                         'proposeToSecretaire',
                                         'proposeToPresident',
                                         'validate',
                                         'present', )
    TRANSITIONS_FOR_PRESENTING_ITEM_2 = ('validate', 'present', )
    TRANSITIONS_FOR_FREEZING_MEETING_1 = TRANSITIONS_FOR_FREEZING_MEETING_2 = ('freeze', )
    TRANSITIONS_FOR_PUBLISHING_MEETING_1 = TRANSITIONS_FOR_PUBLISHING_MEETING_2 = ('freeze', )
    TRANSITIONS_FOR_ACCEPTING_ITEMS_1 = ('freeze', 'decide', )
    TRANSITIONS_FOR_ACCEPTING_ITEMS_2 = ('freeze', 'decide', )

    TRANSITIONS_FOR_DECIDING_MEETING_1 = ('freeze', 'decide', )
    TRANSITIONS_FOR_DECIDING_MEETING_2 = ('freeze', 'decide', )
    TRANSITIONS_FOR_CLOSING_MEETING_1 = ('freeze', 'decide', 'close', )
    TRANSITIONS_FOR_CLOSING_MEETING_2 = ('freeze', 'decide', 'close', )
    BACK_TO_WF_PATH_1 = {
        # Meeting
        'created': ('backToPublished',
                    'backToFrozen',
                    'backToCreated',),
        # MeetingItem
        'itemcreated': ('backToItemFrozen',
                        'backToPresented',
                        'backToValidated',
                        'backToProposedToPresident',
                        'backToProposedToSecretaire',
                        'backToProposedToN2',
                        'backToProposedToN1',
                        'backToItemCreated'),
        'proposed_to_n1': ('backToItemFrozen',
                           'backToPresented',
                           'backToValidated',
                           'backToProposedToPresident',
                           'backToProposedToSecretaire',
                           'backToProposedToN2',
                           'backToProposedToN1'),
        'proposed_to_n2': ('backToItemFrozen',
                           'backToPresented',
                           'backToValidated',
                           'backToProposedToPresident',
                           'backToProposedToSecretaire',
                           'backToProposedToN2'),
        'proposed_to_secretaire': ('backToItemFrozen',
                                   'backToPresented',
                                   'backToValidated',
                                   'backToProposedToPresident',
                                   'backToProposedToSecretaire'),
        'proposed_to_president': ('backToItemFrozen',
                                  'backToPresented',
                                  'backToValidated',
                                  'backToProposedToPresident', ),
        'validated': ('backToItemFrozen',
                      'backToPresented',
                      'backToValidated', )}
    BACK_TO_WF_PATH_2 = {
        # Meeting
        'created': ('backToPublished',
                    'backToFrozen',
                    'backToCreated',),
        'itemcreated': ('backToItemFrozen',
                        'backToPresented',
                        'backToValidated',
                        'backToProposedToPresident',
                        'backToProposedToSecretaire',
                        'backToProposedToN2',
                        'backToProposedToN1',
                        'backToItemCreated'),
        'proposed_to_n1': ('backToItemFrozen',
                           'backToPresented',
                           'backToValidated',
                           'backToProposedToPresident',
                           'backToProposedToSecretaire',
                           'backToProposedToN2',
                           'backToProposedToN1'),
        'proposed_to_n2': ('backToItemFrozen',
                           'backToPresented',
                           'backToValidated',
                           'backToProposedToPresident',
                           'backToProposedToSecretaire',
                           'backToProposedToN2'),
        'proposed_to_secretaire': ('backToItemFrozen',
                                   'backToPresented',
                                   'backToValidated',
                                   'backToProposedToPresident',
                                   'backToProposedToSecretaire'),
        'proposed_to_president': ('backToItemFrozen',
                                  'backToPresented',
                                  'backToValidated',
                                  'backToProposedToPresident', ),
        'validated': ('backToItemFrozen',
                      'backToPresented',
                      'backToValidated', )}
    WF_STATE_NAME_MAPPINGS = {'itemcreated': 'itemcreated',
                              'proposed_to_president': 'proposed_to_president',
                              'proposed': 'proposed_to_president',
                              'validated': 'validated',
                              'presented': 'presented'}

    def _createMeetingWithItems(self, withItems=True, meetingDate=DateTime()):
        '''Create a meeting with a bunch of items.
           Overrided to do it as 'Manager' to be able
           to add recurring items.'''
        from plone.app.testing.helpers import setRoles
        currentMember = self.portal.portal_membership.getAuthenticatedMember()
        currentMemberRoles = currentMember.getRoles()
        setRoles(self.portal, currentMember.getId(), currentMemberRoles + ['Manager', ])
        meeting = MeetingCommunesTestingHelpers._createMeetingWithItems(self,
                                                                        withItems=withItems,
                                                                        meetingDate=meetingDate)
        setRoles(self.portal, currentMember.getId(), currentMemberRoles)
        return meeting
