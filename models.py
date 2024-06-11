from typing import Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Person:
    id: int
    first_name: Optional[str] = field(default="") 
    last_name: Optional[str] = field(default="") 
    profession: Optional[str] = field(default="") 
    summary: Optional[str] = field(default="") 
    image_url: Optional[str] = field(default="./assets/img/placeholder.webp") 

    entries: List['Entry'] = field(default_factory=list)  # Forward declaration
    events: List['Event'] = field(default_factory=list)  # Forward declaration

    def to_dict(self):
        return asdict(self)

@dataclass
class Event:
    id: int
    date: Optional[datetime] = field(default=None) 
    title: Optional[str] = field(default="") 
    summary: Optional[str] = field(default="") 

    entries: List['Entry'] = field(default_factory=list)  # Forward declaration
    people: List['Person'] = field(default_factory=list)  # Forward declaration

    def to_dict(self):
        # Special handling for datetime to serialize properly
        result = asdict(self)
        result['date'] = self.date.strftime('%Y-%m-%d') if self.date else None # Formatting date as a string
        return result

@dataclass
class Entry:
    id: int
    published_date: datetime
    edited_date: datetime
    title: Optional[str] = field(default="") 
    body: Optional[str] = field(default="") 
    people: List[Person] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "published_date": self.published_date.strftime('%Y-%m-%d') if self.published_date else None,
            "edited_date": self.edited_date.strftime('%Y-%m-%d') if self.edited_date else None,
            "title": self.title,
            "body": self.body,
            "people": self.people,
            "events": self.events
        }
        
def get_entries_for_person(person_id, entries):
    """Return entries that mention the given person."""
    return [entry for entry in entries if person_id in entry.people]

def get_entries_for_event(event_id, entries):
    """Return entries that mention the given event."""
    return [entry for entry in entries if event_id in entry.events]

def get_events_for_person(person_id, entries, all_events):
    """Return unique events connected to the given person via entries."""
    event_ids = set()
    for entry in entries:
        if person_id in entry.people:
            event_ids.update(entry.events)
    return [event for event in all_events if event.id in event_ids]

def get_people_for_event(event_id, entries, all_people):
    """Return unique people connected to the given event via entries."""
    people_ids = set()
    for entry in entries:
        if event_id in entry.events:
            people_ids.update(entry.people)
    return [person for person in all_people if person.id in people_ids]


