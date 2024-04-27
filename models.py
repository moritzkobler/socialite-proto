from typing import Optional
from dataclasses import dataclass, asdict, field
import json
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

    def to_dict(self):
        return asdict(self)

@dataclass
class Event:
    id: int
    date: Optional[datetime] = field(default=None) 
    title: Optional[str] = field(default="") 
    summary: Optional[str] = field(default="") 

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
    people: List[int] = field(default_factory=list)  # List to store people IDs
    events: List[int] = field(default_factory=list)   # List to store event IDs

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

