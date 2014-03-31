import tempfile
import os
import unittest
from documentchain import DocumentChain
from documentchain.storage import DiskStorage

class DocumentChainTest(unittest.TestCase):
    def test_add(self):
        chain = DocumentChain()
        id1 = chain.add({'owner': 'victor'})
        id2 = chain.add({'owner': 'theodore'})
        self.assertEqual(chain.get(id1), {'owner': 'victor'})
        self.assertEqual(chain.get(id2), {'owner': 'theodore'})

    def test_verify(self):
        chain = DocumentChain()
        chain.add({'owner': 'victor'})
        self.assertTrue(chain.verify())
        chain.add({'owner': 'theodore'})
        self.assertTrue(chain.verify())

class DiskStorageTest(unittest.TestCase):
    def test_set_entry(self):
        path = tempfile.mkdtemp()
        storage = DiskStorage(path)
        storage.set_entry('abcd', 'content')
        with open(os.path.join(path, 'abcd')) as fh:
            self.assertEqual(fh.read(), 'content')

    def test_get_entry(self):
        path = tempfile.mkdtemp()
        with open(os.path.join(path, '0123'), 'w') as fh:
            fh.write('content')
        storage = DiskStorage(path)
        self.assertEqual(storage.get_entry('0123'), 'content')

    def test_set_head(self):
        path = tempfile.mkdtemp()
        storage = DiskStorage(path)
        storage.set_head('abcd')
        with open(os.path.join(path, 'HEAD')) as fh:
            self.assertEqual(fh.read(), 'abcd')

    def test_get_head(self):
        path = tempfile.mkdtemp()
        with open(os.path.join(path, 'HEAD'), 'w') as fh:
            fh.write('0123')
        storage = DiskStorage(path)
        self.assertEqual(storage.get_head(), '0123')

    def test_get_head_none(self):
        path = tempfile.mkdtemp()
        storage = DiskStorage(path)
        self.assertEqual(storage.get_head(), None)


if __name__ == '__main__':
    unittest.main()
