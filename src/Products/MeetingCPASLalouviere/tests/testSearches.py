# -*- coding: utf-8 -*-
#
# File: testMeetingConfig.py
#
# Copyright (c) 2015 by Imio.be
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

from Products.MeetingCPASLalouviere.tests.MeetingCPASLalouviereTestCase import MeetingCPASLalouviereTestCase
from Products.MeetingCommunes.tests.testSearches import testSearches as mcts

from Products.CMFCore.permissions import ModifyPortalContent
from imio.helpers.cache import cleanRamCacheFor


class testSearches(MeetingCPASLalouviereTestCase, mcts):
    """Test searches."""

    def _test_reviewer_groups(self, developersItem, vendorsItem, collection):
        use_cases = [
            {'transition_user_1': 'pmCreator1',
             'transition': 'goTo_returned_to_proposing_group_proposed_to_n1',
             'check_user_1': 'pmN1'},
            {'transition_user_1': 'pmN1',
             'transition': 'goTo_returned_to_proposing_group_proposed_to_n2',
             'check_user_1': 'pmN2'},
            {'transition_user_1': 'pmN2',
             'transition': 'goTo_returned_to_proposing_group_proposed_to_secretaire',
             'check_user_1': 'pmSecretaire'},
            {'transition_user_1': 'pmSecretaire',
             'transition': 'goTo_returned_to_proposing_group_proposed_to_president',
             'check_user_1': 'pmPresident'},
        ]
        for use_case in use_cases:
            self.changeUser(use_case['transition_user_1'])
            self.do(developersItem, use_case['transition'])
            # pmReviewer 1 may only edit developersItem
            self.changeUser(use_case['check_user_1'])
            self.assertTrue(self.hasPermission(ModifyPortalContent, developersItem))
            cleanRamCacheFor(
                'Products.PloneMeeting.adapters.query_itemstocorrecttovalidateofeveryreviewerlevelsandlowerlevels')
            res = collection.results()
            self.assertEqual(res.length, 1)
            self.assertEqual(res[0].UID, developersItem.UID())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSearches, prefix='test_pm_'))
    return suite
