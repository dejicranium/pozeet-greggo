import unittest
from greggo.activity import Activity, BaseActivity

class TestActivityClass(unittest.TestCase):
    def test_class_creation(self):
        activity = Activity('deji', 'LIKE', 'comment', 'comments')
        self.assertIsInstance(activity, BaseActivity)

    def test_get_actor_id_method(self):
        activity = Activity('deji', 'LIKE', 'comment', 'comments')
        self.assertEqual(activity.get_actor_id(), "deji")

    def test_get_source_id_method(self):
        activity = Activity('deji', 'LIKE', 'comment', 'comments')
        self.assertEqual(activity.get_source_id(), 'comments')

    def test_get_verb_method(self):
        activity = Activity('deji', 'LIKE', 'comment', 'comments')
        self.assertEqual(activity.get_verb(), 'LIKE')

    def test_verb_defaults_to_none(self):
        activity = Activity('deji', 'BELIEVE', 'comment', 'comments')
        self.assertIsNone(activity.get_verb())

    def test_get_object_method(self):
        activity = Activity('deji', 'LIKE', 'comment', 'comments')
        self.assertEqual(activity.get_object(), 'comment')

    def test_actor_class_is_none(self):
        self.assertIsNone(Activity.actor_class)

    def test_actor_class_is_not_none(self):
        activity = Activity
        activity.actor_class = "Something"
        self.assertIsNotNone(Activity.actor_class)


if __name__ == '__main__':
    unittest.main()
