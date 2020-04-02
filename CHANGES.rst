Products.MeetingCPASLalouviere Changelog
========================================

4.1 (unreleased)
----------------
- Compatible for PloneMeeting 4.1

4.0 (2018-08-14)
----------------
- Now MeetingCPASLalouviere using MeetingCommunes who using PloneMeeting

3.3 (2015-02-27)
----------------
- Updated regarding changes in PloneMeeting
- Removed profile 'examples' that loaded examples in english
- Removed dependencies already defined in PloneMeeting's setup.py
- Added parameter MeetingConfig.initItemDecisionIfEmptyOnDecide that let enable/disable
  items decision field initialization when meeting 'decide' transition is triggered
- Added MeetingConfig 'CoDir'
- Added MeetingConfig 'CA'
- Field 'MeetingGroup.signatures' was moved to PloneMeeting

3.2.0.1 (2014-03-06)
--------------------
- Updated regarding changes in PloneMeeting
- Moved some translations from the plone domain to the PloneMeeting domain

3.2.0 (2014-02-12)
------------------
- Updated regarding changes in PloneMeeting
- Use getToolByName where necessary

3.1.0 (2013-11-04)
------------------
- Simplified overrides now that PloneMeeting manage this correctly
- Moved 'add_published_state' to PloneMeeting and renamed to 'hide_decisions_when_under_writing'
- Moved 'searchitemstovalidate' topic to PloneMeeting now that PloneMeeting also manage a 'searchitemstoprevalidate' search

3.0.3dev (unreleased)
---------------------
- Adapted all tests to call PloneMeeting ones
- Added specific search for user gdecoster (http://trac.imio.be/trac/ticket/6354)

2.1.2 (2012-09-19)
------------------
- Original release