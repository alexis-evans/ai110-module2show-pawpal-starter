from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Owner:
    name: Optional[str] = None
    contact_info: Optional[str] = None
    preferences: Dict = field(default_factory=dict)
    
    def add_pet(self):
        pass
    
    def remove_pet(self):
        pass


@dataclass
class Pet:
    name: Optional[str] = None
    age: Optional[int] = None
    type: Optional[str] = None
    tasks: List = field(default_factory=list)
    
    def add_task(self):
        pass
    
    def remove_task(self):
        pass


@dataclass
class Task:
    description: Optional[str] = None
    duration: Optional[int] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    
    def mark_complete(self):
        pass
    
    def update_task(self):
        pass


class Scheduler:
    def __init__(self):
        self.tasks = []
        self.constraints = []
    
    def generate_schedule(self):
        pass
    
    def explain_schedule(self):
        pass