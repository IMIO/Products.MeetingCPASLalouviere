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
from copy import deepcopy
from Products.MeetingCommunes.adapters import CustomToolPloneMeeting, CustomMeetingConfig
from Products.PloneMeeting.interfaces import IToolPloneMeetingCustom, IMeetingConfigCustom
from Products.PloneMeeting.model import adaptations
from Products.PloneMeeting.MeetingConfig import MeetingConfig
from Products.PloneMeeting.model.adaptations import _addIsolatedState


from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from Products.Archetypes.utils import OrderedDict
from collective.contact.plonegroup.utils import get_all_suffixes
from zope.interface import implements
from zope.i18n import translate


customWfAdaptations = list(deepcopy(MeetingConfig.wfAdaptations))
customWfAdaptations.append('propose_to_budget_reviewer')
MeetingConfig.wfAdaptations = tuple(customWfAdaptations)

class LLMeetingConfig(CustomMeetingConfig):
    """Adapter that adapts a meetingConfig implementing IMeetingConfig to the
       interface IMeetingConfigCustom."""

    implements(IMeetingConfigCustom)
    security = ClassSecurityInfo()

    def _extraSearchesInfo(self, infos):
        """Add some specific searches."""
        super(LLMeetingConfig, self)._extraSearchesInfo(infos)
        cfg = self.getSelf()
        itemType = cfg.getItemTypeName()
        proposed_to_director = (
            "searchproposedtodirector",
            {
                "subFolderId": "searches_items",
                "active": True,
                "query": [
                    {
                        "i": "portal_type",
                        "o": "plone.app.querystring.operation.selection.is",
                        "v": [itemType, ],
                    },
                    {
                        "i": "review_state",
                        "o": "plone.app.querystring.operation.selection.is",
                        "v": ["proposed_to_director"],
                    },
                ],
                "sort_on": u"modified",
                "sort_reversed": True,
                "showNumberOfItems": True,
                "tal_condition": "python:tool.userIsAmong(['directors'])",
                "roles_bypassing_talcondition": ["Manager", ],
            },
        )
        extra_infos = []
        if 'council' in cfg.getId():
            extra_infos = [
                proposed_to_director,
            ]
        elif 'college' in cfg.getId():
            extra_infos = [
                (
                    "searchproposedtobudgetreviewer",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_budget_reviewer"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                (
                    "searchproposedtoservicehead",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_servicehead"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition":
                            "python:tool.userIsAmong(['serviceheads', 'officemanagers', 'divisionheads', 'directors'])",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                (
                    "searchproposedtoofficemanager",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_officemanager"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition": "python:tool.userIsAmong(['officemanagers', 'divisionheads', 'directors'])",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                (
                    "searchproposedtodivisionhead",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_divisionhead"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition": "python:tool.userIsAmong(['divisionheads', 'directors'])",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                proposed_to_director,
                # Items in state 'proposed_to_dg'
                (
                    "searchproposedtodg",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_dg"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition": "python: tool.isManager(cfg)",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                # Items in state 'proposed_to_alderman'
                (
                    "searchproposedtoalderman",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["proposed_to_alderman"],
                            },
                        ],
                        "sort_on": u"modified",
                        "sort_reversed": True,
                        "showNumberOfItems": True,
                        "tal_condition": "python:tool.userIsAmong(['alderman'])",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                (
                    "searchItemsTofollow_up_yes",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [
                                    "accepted",
                                    "refused",
                                    "delayed",
                                    "accepted_but_modified",
                                ],
                            },
                            {
                                "i": "getFollowUp",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["follow_up_yes", ],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                # Items to follow provider but not to print in Dashboard'
                (
                    "searchItemsProvidedFollowUpButNotToPrint",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [
                                    "accepted",
                                    "refused",
                                    "delayed",
                                    "accepted_but_modified",
                                ],
                            },
                            {
                                "i": "getFollowUp",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["follow_up_provided_not_printed", ],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
                # Items to follow provider and to print
                (
                    "searchItemsProvidedFollowUp",
                    {
                        "subFolderId": "searches_items",
                        "active": True,
                        "query": [
                            {
                                "i": "portal_type",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [itemType, ],
                            },
                            {
                                "i": "review_state",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": [
                                    "accepted",
                                    "refused",
                                    "delayed",
                                    "accepted_but_modified",
                                ],
                            },
                            {
                                "i": "getFollowUp",
                                "o": "plone.app.querystring.operation.selection.is",
                                "v": ["follow_up_provided", ],
                            },
                        ],
                        "sort_on": u"created",
                        "sort_reversed": True,
                        "showNumberOfItems": False,
                        "tal_condition": "",
                        "roles_bypassing_talcondition": ["Manager", ],
                    },
                ),
            ]
        infos.update(OrderedDict(extra_infos))
        return infos

    def _custom_reviewersFor(self):
        '''Manage reviewersFor Bourgmestre because as some 'creators' suffixes are
           used after reviewers levels, this break the _highestReviewerLevel and other
           related hierarchic level functionalities.'''
        reviewers = [
            ('president', ['proposed_to_president', ]),
            ('secretaire',
             ['proposed_to_secretaire',
              'proposed_to_n2',
              'proposed_to_n1',]),
            ('n2',
             ['proposed_to_n2',
              'proposed_to_n1',]),
            ('n1',
             ['proposed_to_n1',]),
        ]
        return OrderedDict(reviewers)

    def get_item_custom_suffix_roles(self, item, item_state):
        '''See doc in interfaces.py.'''
        suffix_roles = {}
        if item_state == 'proposed_to_budget_reviewer':
            for suffix in get_all_suffixes(item.getProposingGroup()):
                suffix_roles[suffix] = ['Reader']
                if suffix == 'budgetimpactreviewers':
                    suffix_roles[suffix] += ['Contributor', 'Editor', 'Reviewer']

        return True, suffix_roles


class MLLCustomToolPloneMeeting(CustomToolPloneMeeting):
    '''Adapter that adapts portal_plonemeeting.'''

    implements(IToolPloneMeetingCustom)
    security = ClassSecurityInfo()

    def performCustomWFAdaptations(
            self, meetingConfig, wfAdaptation, logger, itemWorkflow, meetingWorkflow):
        ''' '''
        if wfAdaptation == 'propose_to_budget_reviewer':
            _addIsolatedState(
                new_state_id='proposed_to_budget_reviewer',
                origin_state_id='itemcreated',
                origin_transition_id='proposeToBudgetImpactReviewer',
                origin_transition_title=translate("proposeToBudgetImpactReviewer", "plone"),
                # origin_transition_icon=None,
                origin_transition_guard_expr_name='mayCorrect()',
                back_transition_guard_expr_name="mayCorrect()",
                back_transition_id='backTo_itemcreated_from_proposed_to_budget_reviewer',
                back_transition_title=translate("validateByBudgetImpactReviewer", "plone"),
                # back_transition_icon=None
                itemWorkflow=itemWorkflow)
            return True
        return False


InitializeClass(MLLCustomToolPloneMeeting)
InitializeClass(LLMeetingConfig)

LLO_WAITING_ADVICES_FROM_STATES = {
    '*':
    (
        {'from_states': ('itemcreated', ),
         'back_states': ('itemcreated', ),
         'perm_cloned_state': 'itemcreated',
         'use_custom_icon': False,
         # default to "validated", this avoid using the backToValidated title that
         # is translated to "Remove from meeting"
         'use_custom_back_transition_title_for': ("validated", ),
         # we can define some back transition id for some back_to_state
         # if not, a generated transition is used, here we could have for example
         # 'defined_back_transition_ids': {"validated": "validate"}
         'defined_back_transition_ids': {},
         # if () given, a custom transition icon is used for every back transitions
         'only_use_custom_back_transition_icon_for': ("validated", ),
         'use_custom_state_title': False,
         'use_custom_transition_title_for': {},
         'remove_modify_access': True,
         'adviser_may_validate': True,
         # must end with _waiting_advices
         'new_state_id': None,
         },
        {'from_states': ('proposed_to_president', ),
         'back_states': ('proposed_to_president', ),
         'perm_cloned_state': 'validated',
         'use_custom_icon': False,
         # default to "validated", this avoid using the backToValidated title that
         # is translated to "Remove from meeting"
         'use_custom_back_transition_title_for': ("validated", ),
         # we can define some back transition id for some back_to_state
         # if not, a generated transition is used, here we could have for example
         # 'defined_back_transition_ids': {"validated": "validate"}
         'defined_back_transition_ids': {},
         # if () given, a custom transition icon is used for every back transitions
         'only_use_custom_back_transition_icon_for': ("validated", ),
         'use_custom_state_title': True,
         'use_custom_transition_title_for': {},
         'remove_modify_access': True,
         'adviser_may_validate': False,
         # must end with _waiting_advices
         'new_state_id': None,
         },
    ),
}
adaptations.WAITING_ADVICES_FROM_STATES.update(LLO_WAITING_ADVICES_FROM_STATES)