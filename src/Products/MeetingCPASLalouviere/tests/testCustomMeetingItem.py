# -*- coding: utf-8 -*-
#
# File: testCustomMeetingItem.py
#
# Copyright (c) 2008 by PloneGov
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

from AccessControl import Unauthorized
from DateTime import DateTime
from Products.MeetingCPASLalouviere.tests.MeetingCPASLalouviereTestCase import MeetingCPASLalouviereTestCase
from Products.MeetingCommunes.tests.testCustomMeetingItem import testCustomMeetingItem as mctcmi


class testCustomMeetingItem(MeetingCPASLalouviereTestCase, mctcmi):
    """
        Tests the Meeting adapted methods
    """

    def test_GetEchevinsForProposingGroup(self):
        """Check a meetingItem for developers group return an echevin (the Same group in our case)
           and a meetingItem for vendors return no echevin."""
        # create items
        self.changeUser('pmCreator1')
        i1 = self.create('MeetingItem')
        i1.setProposingGroup('vendors')
        # for vendor, certfiedSignatures must be empty
        res = i1.adapted().getEchevinsForProposingGroup()
        self.assertEquals(res, [])
        self.changeUser('pmCreator1')
        i2 = self.create('MeetingItem')
        i2.setProposingGroup('developers')
        # for developer, certfiedSignatures must be equal to
        res = i2.adapted().getEchevinsForProposingGroup()
        self.assertEquals(res, ['developers'])

    def test_listGrpBudgetInfosAdviser(self):
        """Check if the list of groups that can be selected on an item to modify budgetInfos field
        correspond to group with accronym start with DGF (finance and taxe))"""
        self.changeUser('admin')
        self._createFinanceGroups()
        self.changeUser('pmCreator1')
        i1 = self.create('MeetingItem')
        list_GBIA = i1.listGrpBudgetInfosAdviser()
        from Products.Archetypes.atapi import DisplayList
        res = DisplayList([('', u'--make_a_choice--'), ('finances', u'Finances'), ('taxes', u'Taxes')])
        self.assertEquals(len(list_GBIA), 3)
        self.assertEquals(list_GBIA[0], res[0])
        self.assertEquals(list_GBIA[1], res[1])
        self.assertEquals(list_GBIA[2], res[2])

    def test_onEdit(self):
        """check MeetingBudgetImpactReviewer role on an item, when a group is choosen in BudgetInfosAdviser
        and state is, at least "itemFrozen". Retrieve role for other grp_budgetimpactreviewers
        """
        self.changeUser('pmManager')
        m = self._createMeetingWithItems()
        self.do(m, 'freeze')
        item = m.getItems()[0]
        # no MeetingBudgetImpactReviewer in rôle
        self.assertEquals((u'developers_budgetimpactreviewers', (
            'Reader', 'MeetingBudgetImpactReviewer')) in item.get_local_roles(), False)
        self.assertEquals((u'vendors_budgetimpactreviewers', (
            'Reader', 'MeetingBudgetImpactReviewer')) in item.get_local_roles(), False)
        self.assertEquals((u'finances_budgetimpactreviewers', (
            'Reader', 'MeetingBudgetImpactReviewer')) in item.get_local_roles(), False)
        self.assertEquals((u'taxes_budgetimpactreviewers', (
            'Reader', 'MeetingBudgetImpactReviewer')) in item.get_local_roles(), False)
        item.setGrpBudgetInfos(('finances',))
        item.adapted().onEdit(True)
        # MeetingBudgetImpactReviewer role define for finance (only)
        self.assertEquals((u'developers_budgetimpactreviewers', (
            'Reader', 'MeetingBudgetImpactReviewer')) in item.get_local_roles(), False)
        self.assertEquals((u'vendors_budgetimpactreviewers', (
            'Reader', 'MeetingBudgetImpactReviewer')) in item.get_local_roles(), False)
        self.assertEquals((u'finances_budgetimpactreviewers', (
            'Reader', 'MeetingBudgetImpactReviewer')) in item.get_local_roles(), True)
        self.assertEquals((u'taxes_budgetimpactreviewers', (
            'Reader', 'MeetingBudgetImpactReviewer')) in item.get_local_roles(), False)

    def test_manageItemCertifiedSignatures(self):
        """
          This tests the form that manage itemCertifiedSignatures and that can apply it on item.
        """
        self.changeUser('admin')
        # make items inserted in a meeting inserted in this order
        self.meetingConfig.insertingMethodsOnAddItem = ({'insertingMethod': 'at_the_end', 'reverse': '0'}, )
        # remove recurring items if any as we are playing with item number here under
        self._removeConfigObjectsFor(self.meetingConfig)
        # a user create an item and we insert it into a meeting
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        item.setDecision('<p>A decision</p>')
        self.changeUser('pmManager')
        meeting = self._createMeetingWithItems(withItems=False, meetingDate=DateTime() + 1)
        # define an assembly on the meeting
        meeting.setAssembly('Meeting assembly')
        meeting.setSignatures('Meeting signatures')
        self.presentItem(item)
        # make the form item_assembly_default works
        self.request['PUBLISHED'].context = item
        self.changeUser('pmCreator1')
        formCertifiedSignatures = item.restrictedTraverse('@@manage_item_certified_signatures_form').form_instance
        # for now, the itemCertifiedSignatures fields are not used, so it raises Unauthorized
        self.assertRaises(Unauthorized, formCertifiedSignatures.update)
        # current user must be at least MeetingManager to use this
        self.changeUser('admin')
        formCertifiedSignatures = item.restrictedTraverse('@@manage_item_certified_signatures_form').form_instance
        formCertifiedSignatures.update()
        # by default, itemCertifiedSignatures is not define
        self.assertEquals(item.getItemCertifiedSignatures(), '')
        # now use the form to change the item itemCertifiedSignatures
        self.changeUser('pmManager')
        self.freezeMeeting(meeting)
        self.do(meeting, 'decide')
        self.do(item, 'accept')
        self.changeUser('pmCreator1')
        formCertifiedSignatures = item.restrictedTraverse('@@manage_item_certified_signatures_form').form_instance
        formCertifiedSignatures.update()
        self.request.form['form.widgets.item_certified_signatures'] = u'Item certified signatures'
        formCertifiedSignatures.handleApplyItemCertifiedSignatures(formCertifiedSignatures, None)
        self.assertEquals(item.getItemCertifiedSignatures(), 'Item certified signatures')
        # we can change this field in closed meeting
        self.changeUser('pmManager')
        self.do(meeting, 'close')
        self.changeUser('pmCreator1')
        formCertifiedSignatures = item.restrictedTraverse('@@manage_item_certified_signatures_form').form_instance
        self.request.form['form.widgets.item_certified_signatures'] = u'Item certified signatures - 2'
        formCertifiedSignatures.update()
        formCertifiedSignatures.handleApplyItemCertifiedSignatures(formCertifiedSignatures, None)
        self.assertEquals(item.getItemCertifiedSignatures(), 'Item certified signatures - 2')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCustomMeetingItem, prefix='test_pm_'))
    return suite