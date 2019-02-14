#an 'id' is useful because it is how we represent an activity

VERBS = {
    "ADDED":{'id': 1, 'action': 'added'},
    "COMMENTED": {'id': 2, 'action': 'commented on'},
    "SHARED": {'id': 3, 'action': 'shared'},
    "AGREED": {'id': 4, 'action': 'agreed with'},
    "VOTED": {'id': 5, 'action': 'voted'},
    "FOLLOWED": {'id': 7, 'action': 'followed'},
}


def get_verb_action(verb):
    verb = verb.upper()
    action = VERBS[verb]['action']
    return action


def get_action_from_verb_id(id):
    action = [VERBS[a]['action'] for a in VERBS.keys()
                if VERBS[a]['id'] == id]
    return "".join(action)


def get_verb_from_id(id):
    verb = [a for a in VERBS.keys() if VERBS[a]['id'] == id]
    return ''.join(verb)
