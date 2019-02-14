from .verbs import VERBS

#the type of activity is going to be stored in the datastore as integers,
#so this mapping is meant to easily check the ativity that an activity entails
#
ACTIVITY_SCORES= {
'VOTED': 1,
'AGREED': 2,
'SHARED': 3,
'COMMENTED': 4,
'ADDED': 5
}

class BaseActivity:
    """Class for creating an activity

        An activity is made up of an actor, object, verb and source.

        As its name implies, an 'actor' refers to the user or entity who
        triggered the activity.

        An 'object' is the entity on which an action by an actor is carred out
        The 'verb' is the name of the action carried out
        A 'source', as its name implies, signifies the source of the object

        For example::

        In "Deji Atoyebi commented on Iyabo Atoyebi's poll":

        Actor: Deji Atoyebi
        Verb: Commented on
        Object: Poll
        Source: A poll by Iyabo Atoyebi in the list of polls

        In this class, the ids of the actor and source, rather than the actual
        objects, are needed.
        """

    #the class which we query to get our actor. Needs to be changed
    actor_class = None

    def __init__(self, id, actor_id, verb, object, source_id):
        self.id
        self.actor_id = actor_id
        self.verb = verb if verb in VERBS.keys() else None
        self.object = object
        self.source_id = source_id

    def set_actor_id(self, id):
        pass

    def set_verb(self, verb):
        pass

    def get_actor_id(self):
            return self.actor_id

    def get_actor(self, request):
            actor = self.get_entity_from_class(request, actor_class, actor_id)
            return actor

    def get_source_id(self):
            return self.source_id

    def get_verb(self):
            return self.verb

    def get_object(self):
            return self.object

    def get_entity_from_class(self, request, clss, entity_id):
        entity = request.dbsession.query(clss).filter(clss.id==entity_id).first()
        return entity

    @property
    def serialization_id(self):
        pass


    class ShareActivity(BaseActivity):
        # -*- coding: utf-8 -*-
        def __init__(self, id, actor_id, verb=VERBS["SHARED"]['ID'], object, source_id):
            super().__init__(id, actor_id, verb, object, source_id)


    class CommentActivity(BaseActivity):
        def __init__(self, id, actor_id, verb=VERBS[''], object, source_id):
            super()._init__(id, actor_id, verb, object, source_id)
            self.comment = None

        def set_comment(self, comment):
            self.comment = comment

        def get_comment(self):
            return comment
