# -*- coding: utf-8 -*-

import logging

from Products.MeetingCommunes.migrations.migrate_to_4_0 import Migrate_To_4_0 as PMMigrate_To_4_0

from plone import api

logger = logging.getLogger('MeetingCPASLalouviere')


# The migration class ----------------------------------------------------------
class Migrate_To_4_0(PMMigrate_To_4_0):

    wfs_to_delete = []

    def _after_reinstall(self):
        """Use that hook that is called just after the profile has been reinstalled by
           PloneMeeting, this way, we may launch some steps before PloneMeeting ones.
           Here we will update used workflows before letting PM do his job."""
        logger.info('Replacing old no more existing workflows...')
        PMMigrate_To_4_0._after_reinstall(self)
        for cfg in self.tool.objectValues('MeetingConfig'):
            # MeetingItem workflow
            if cfg.getItemWorkflow() == 'meetingitembplalouviere_workflow':
                cfg.setItemWorkflow('meetingitemcpaslalouviere_workflow')
                cfg._v_oldItemWorkflow = 'meetingitembplalouviere_workflow'
                wfAdaptations = list(cfg.getWorkflowAdaptations())
                cfg.setWorkflowAdaptations(wfAdaptations)
            # Meeting workflow
            if cfg.getMeetingWorkflow() == 'meetingbplalouviere_workflow':
                cfg.setMeetingWorkflow('meetingcpaslalouviere_workflow')
                cfg._v_oldMeetingWorkflow = 'meetingbplalouviere_workflow'
            # delete old unused workflows, aka every workflows containing 'bp'
        wfTool = api.portal.get_tool('portal_workflow')
        self.wfs_to_delete = [wfId for wfId in wfTool.listWorkflows()
                              if wfId.endswith(('meetingitembplalouviere_workflow',
                                                'meetingbplalouviere_workflow',))]
        logger.info('Done.')

    def run(self, step=None):
        # change self.profile_name that is reinstalled at the beginning of the PM migration
        self.profile_name = u'profile-Products.MeetingCPASLalouviere:default'

        # call steps from Products.PloneMeeting
        PMMigrate_To_4_0.run(self, step=step)


# The migration function -------------------------------------------------------
def migrate(context):
    '''This migration function:

       1) Reinstall Products.MeetingCommunes and execute the Products.PloneMeeting migration;
       2) Clean CDLD attributes;
       3) Add an annex type for Meetings;
       4) Remove useless workflows;
       5) Migrate positive decided states.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run()
    migrator.finish()


def migrate_step1(context):
    '''This migration function:

       1) Reinstall Products.MeetingCommunes and execute the Products.PloneMeeting migration.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run(step=1)
    migrator.finish()


def migrate_step2(context):
    '''This migration function:

       1) Execute step2 of Products.PloneMeeting migration profile (imio.annex).
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run(step=2)
    migrator.finish()


def migrate_step3(context):
    '''This migration function:

       1) Execute step3 of Products.PloneMeeting migration profile.
       2) Clean CDLD attributes;
       3) Add an annex type for Meetings;
       4) Remove useless workflows;
       5) Migrate positive decided states.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run(step=3)
    migrator.finish()


def migrate_step4(context):
    '''This migration function:

       1) Add meeting assemblies DashboardPODTemplate.
    '''
    migrator = Migrate_To_4_0(context)
    migrator.run(step=4)
    migrator.finish()
