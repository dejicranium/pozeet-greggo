class NotificationManager: 
    
    def __init__(self, request, user_id, sender_id, activity_type, act_source, act_object):
        self.user_id = user_id 
        self.request = request
        self.source = act_source
        self.source_id = self.source.id
        self.object = act_object
        self.object_id = self.object.id
        self.sender_id = sender_id


        if activity_type == 'poll':
            self.action_type = 'created'
        elif activity_type == 'opinion':
            self.action_type = 'posted'
        
        elif activity_type == 'like':
            self.action_type = 'liked'
        
        elif activity_type == 'vote':
            self.action_type = 'voted'
        
        elif activity_type == 'comment':
            self.action_type = 'commented'
        
        elif activity_type == 'reply':
            self.action_type = 'replied'

        elif activity_type == 'agree':
            self.action_type = 'agreed'
        
        elif activity_type == 'share':
            self.action_type = 'shared'

        
    def create_new_notification(self):
        notification =  Notification()
        notification.user_id = self.user_id
        notification.action_type = self.action_type
        notification.sender_id = self.sender_id
        notification.source = self.source
        notification.source_id = self.source_id
        notification.object_id = self.object_id

        if isinstance(self.object, Poll):
            notification.object = 'poll'
        elif isinstance(self.object, Comment):
            notification.object = 'comment'
        elif isinstance(self.object, Share):
            notification.object = 'share'
        elif isinstance(self.object, Like):
            notification.object = 'like'
        elif isinstance(self.object, Agree):
            notification.object = 'agree'
        
        self.request.dbsession.add(notification)