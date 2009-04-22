from pubsub import pub
from pubsub.utils.topicspec import TopicTreeDefnSimple
from appcommon import topics


class TopicTree(TopicTreeDefnSimple):
    class program:
        'Events related to the program itself'
        
        class closed:
            'The program was closed'
            pages = 'The note pages open'
            _required = 'pages'
            
    class note:
        'Events related to a specific note'
        
        class opened:
            'A note was opened'
            note = 'The opened note'
            _required = 'note'

        class saved:
            'A note was saved'
            note = 'The saved note'
            _required = 'note'
            
        class closed:
            'A note was closed'
            note = 'The closed note'
            _required = 'note'
            
    class page:
        'Events related to a specific page in the GUI'
            
        class closing:
            'A page is being closed by the user'
            page = 'The page being closed'
            _required = 'page'

pub.addTopicDefnProvider(TopicTree())
