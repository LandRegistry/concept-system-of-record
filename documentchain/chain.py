import json
import requests
from .entry import Entry
from .storage import MemoryStorage

class DocumentChain(object):
    def __init__(self, storage=None, webhooks=None):
        self.storage =  storage or MemoryStorage()
        self.webhooks = webhooks or []

    def add(self, content):
        entry = Entry(
            content=content,
            previous_id=self.storage.get_head(),
        )
        id = entry.get_id()
        self.storage.set_entry(id, entry.to_json())
        self.storage.set_head(id)
        for url in self.webhooks:
            res = requests.post(
                url,
                data=entry.to_json(),
                headers={'content-type': 'application/json'}
            )
            res.raise_for_status()
        return id

    def get(self, id):
        return Entry.from_json(self.storage.get_entry(id))

    def all(self):
        """
        Returns an iterator of all entries.
        """
        id = self.storage.get_head()
        while id:
            entry = Entry.from_json(self.storage.get_entry(id))
            yield entry
            id = entry.previous_id

    def verify(self):
        id = self.storage.get_head()
        while id:
            entry = Entry.from_json(self.storage.get_entry(id))
            if entry.get_id() != id:
                return False
            id = entry.previous_id
        return True

    def get_head(self):
        id = self.storage.get_head()
        return Entry.from_json(self.storage.get_entry(id))
