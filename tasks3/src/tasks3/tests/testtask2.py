import unittest
import tempfile
from pathlib import Path


class TestDistrait(unittest.TestCase):
    def setUp(self):
        # Use temporary directory for JSON files so real data is not affected
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        import distrait
        # point module file paths to temp location
        distrait.TASKS_FILE = Path(self.tmpdir.name) / "tasks.json"
        distrait.NOTES_FILE = Path(self.tmpdir.name) / "notes.json"
        distrait.save_json(distrait.TASKS_FILE, [])
        distrait.save_json(distrait.NOTES_FILE, [])

    def test_add_and_complete_task(self):
        import distrait
        t = distrait.add_task("unit test task", priority=1)
        self.assertEqual(t['title'], "unit test task")
        distrait.complete_task(t['id'])
        tasks = distrait.load_json(distrait.TASKS_FILE)
        self.assertEqual(tasks[0]['status'], 'complete')

    def test_add_note_and_list(self):
        import distrait
        n = distrait.add_note("note1", "this is a test note", tags=['x'])
        notes = distrait.load_json(distrait.NOTES_FILE)
        self.assertEqual(notes[0]['title'], 'note1')


if __name__ == '__main__':
    unittest.main()
