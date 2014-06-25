from Products.Archetypes.atapi import *


def update_group_schema(baseSchema):
    specificSchema = Schema((

        # field used to define specific signatures for a MeetingGroup
        TextField(
            name='signatures',
            widget=TextAreaWidget(
                label='Signatures',
                label_msgid='MeetingCPASLalouviere_label_signatures',
                description='Leave empty to use the signatures defined on the meeting',
                description_msgid='MeetingCPASLalouviere_descr_signatures',
                i18n_domain='PloneMeeting',
            ),
        ),
    ),)

    completeGroupSchema = baseSchema + specificSchema.copy()

    return completeGroupSchema
MeetingGroup.schema = update_group_schema(MeetingGroup.schema)


def update_item_schema(baseSchema):
    specificSchema = Schema((

    # field used to define specific assembly for a MeetingItem
    TextField(
        name='itemAssembly',
        widget=TextAreaWidget(
            condition="python: (member.has_role('MeetingManager') or member.has_role('Manager')) and here.hasMeeting() \
                      and here.getMeeting().attributeIsUsed('assembly')",
            description="ItemAssembly",
            description_msgid="MeetingCPASLalouviere_descr_assembly",
            label='Itemassembly',
            label_msgid='MeetingCPASLalouviere_label_itemAssembly',
            i18n_domain='PloneMeeting',
        ),
    ),
    ),)

    completeItemSchema = baseSchema + specificSchema.copy()
    completeSchema['budgetInfos'].write_permission = "MeetingCPASLalouviere: Write budget infos"
    completeSchema['budgetInfos'].read_permission = "MeetingCPASLalouviere: Read budget infos"
    completeSchema['optionalAdvisers'].widget.size = 10
    completeSchema['optionalAdvisers'].widget.format = "select"
    completeSchema['optionalAdvisers'].widget.description_msgid = "optional_advisers_item_descr"
    return completeItemSchema
MeetingItem.schema = update_item_schema(MeetingItem.schema)

# Classes have already been registered, but we register them again here
# because we have potentially applied some schema adaptations (see above).
# Class registering includes generation of accessors and mutators, for
# example, so this is why we need to do it again now.
from Products.PloneMeeting.config import registerClasses
registerClasses()
