# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2015 by IMIO
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Andre NUYENS <andre.nuyens@imio.be>"""
__docformat__ = 'plaintext'

import os
import logging
logger = logging.getLogger('MeetingCPASLalouviere: setuphandlers')
from plone import api
from Products.PloneMeeting.exportimport.content import ToolInitializer
from Products.MeetingCPASLalouviere.config import PROJECTNAME


def isNotMeetingCPASLalouviereProfile(context):
    return context.readDataFile("MeetingCPASLalouviere_marker.txt") is None


def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotMeetingCPASLalouviereProfile(context):
        return
    wft = api.portal.get_tool('portal_workflow')
    wft.updateRoleMappings()


def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotMeetingCPASLalouviereProfile(context):
        return
    site = context.getSite()
    #need to reinstall PloneMeeting after reinstalling MC workflows to re-apply wfAdaptations
    reinstallPloneMeeting(context, site)
    showHomeTab(context, site)
    reorderSkinsLayers(context, site)


def logStep(method, context):
    logger.info("Applying '%s' in profile '%s'" %
                (method, '/'.join(context._profile_path.split(os.sep)[-3:])))


def isMeetingCPASllConfigureProfile(context):
    return context.readDataFile("MeetingCPASll_examples_fr_marker.txt") or \
           context.readDataFile("MeetingCPASLL_tests_marker.txt")


def installMeetingCPASLalouviere(context):
    """ Run the default profile"""
    if not isMeetingCPASllConfigureProfile(context):
        return
    logStep("installMeetingCPASLalouviere", context)
    portal = context.getSite()
    portal.portal_setup.runAllImportStepsFromProfile('profile-Products.MeetingCPASLalouviere:default')


def initializeTool(context):
    '''Initialises the PloneMeeting tool based on information from the current
       profile.'''
    if not isMeetingCPASllConfigureProfile(context):
        return

    logStep("initializeTool", context)
    _installPloneMeeting(context)
    return ToolInitializer(context, PROJECTNAME).run()


def reinstallPloneMeeting(context, site):
    '''Reinstall PloneMeeting so after install methods are called and applied,
       like performWorkflowAdaptations for example.'''

    if isNotMeetingCPASLalouviereProfile(context):
        return

    logStep("reinstallPloneMeeting", context)
    _installPloneMeeting(context)
    # launch skins step for MeetingNamur so MeetingNamur skin layers are before PM ones
    site.portal_setup.runImportStepFromProfile('profile-Products.MeetingCPASLalouviere:default', 'skins')

def _installPloneMeeting(context):
    site = context.getSite()
    profileId = u'profile-Products.PloneMeeting:default'
    site.portal_setup.runAllImportStepsFromProfile(profileId)


def showHomeTab(context, site):
    """
       Make sure the 'home' tab is shown...
    """
    if isNotMeetingCPASLalouviereProfile(context):
        return

    logStep("showHomeTab", context)

    index_html = getattr(site.portal_actions.portal_tabs, 'index_html', None)
    if index_html:
        index_html.visible = True
    else:
        logger.info("The 'Home' tab does not exist !!!")


def reorderSkinsLayers(context, site):
    """
       Re-apply MeetingCPASLalouviere skins.xml step
       as the reinstallation of MeetingCPASLalouviere and PloneMeeting changes the portal_skins layers order
    """
    if isNotMeetingCPASLalouviereProfile(context) and not isMeetingCPASllConfigureProfile(context):
        return

    logStep("reorderSkinsLayers", context)
    site.portal_setup.runImportStepFromProfile(u'profile-Products.MeetingCPASLalouviere:default', 'skins')


def finalizeInstance(context):
    """
      Called at the very end of the installation process (after PloneMeeting).
    """
    if isNotMeetingCPASLalouviereProfile(context) and not isMeetingCPASllConfigureProfile(context):
        return

    reorderSkinsLayers(context, context.getSite())
    reorderCss(context)


def reorderCss(context):
    """
       Make sure CSS are correctly reordered in portal_css so things
       work as expected...
    """
    site = context.getSite()
    logStep("reorderCss", context)
    portal_css = site.portal_css
    css = ['imio.dashboard.css',
           'plonemeeting.css',
           'meetingcpaslalouviere.css',
           'imioapps.css',
           'plonemeetingskin.css',
           'imioapps_IEFixes.css',
           'ploneCustom.css']
    for resource in css:
        portal_css.moveResourceToBottom(resource)
