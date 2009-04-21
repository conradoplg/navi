from pubsub import pub
from pubsub.utils.topicspec import TopicTreeDefnSimple


class CommonTopicTree(TopicTreeDefnSimple):
    class commands:
        'Events related to all commands'
        
        class created:
            'The commands were created'
            command_tree = 'The command tree'
            _required = 'command_tree'
        
        class changed:
            """The commands were changed.
            
            The change could be the name, description or shortcut
            in any oh them"""
            command_tree = 'The command tree'
            accel_table = 'The new accelerator table'
            _required = 'command_tree', 'accel_table'
            
    class command:
        'Events related to a single command'
        
        class execute:
            'Execute the command specified by the ID'
            ide = 'ID of the command'
            _required = 'ide'
            
    class language:
        'Events related to the program locale'
        
        class changed:
            'The language was changed'
        
    class settings:
        'Events related to the settings'
        
        class changed:
            'Some or all of the settings were changed'
            settings = 'The settings'
            _required = 'settings'
            
    class setting:
        'Events related to a specific setting'
        
        class changed:
            'A setting was changed'
            settings = 'The settings'
            section = 'The section of the setting'
            option = 'The option which was changed'
            value = 'The new value'
            _required = 'settings', 'section', 'option', 'value'


pub.addTopicDefnProvider(CommonTopicTree())
