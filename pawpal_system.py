from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import IntEnum


class Priority(IntEnum):
    """Priority levels for tasks"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks"""
    name: Optional[str] = None
    contact_info: Optional[str] = None
    preferences: Dict = field(default_factory=dict)
    pets: List['Pet'] = field(default_factory=list)
    available_time_minutes: int = 480  # Default 8 hours per day

    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to this owner's list of pets"""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def remove_pet(self, pet: 'Pet') -> None:
        """Remove a pet from this owner's list of pets"""
        if pet in self.pets:
            self.pets.remove(pet)
            pet.owner = None

    def get_all_tasks(self, pet: Optional['Pet'] = None) -> List['Task']:
        """Get all tasks across all pets, or tasks for a specific pet if provided"""
        if pet is not None:
            # Return tasks for the specified pet only
            if pet in self.pets:
                return pet.tasks
            else:
                return []  # Pet not owned by this owner
        else:
            # Return all tasks from all pets
            all_tasks = []
            for pet in self.pets:
                all_tasks.extend(pet.tasks)
            return all_tasks


@dataclass
class Pet:
    """Stores pet details and a list of tasks"""
    name: Optional[str] = None
    age: Optional[int] = None
    type: Optional[str] = None
    owner: Optional['Owner'] = None
    tasks: List['Task'] = field(default_factory=list)

    def add_task(self, task: 'Task') -> None:
        """Add a task to this pet's task list"""
        if task not in self.tasks:
            self.tasks.append(task)
            task.pet = self

    def remove_task(self, task: 'Task') -> None:
        """Remove a task from this pet's task list"""
        if task in self.tasks:
            self.tasks.remove(task)
            task.pet = None

    def get_pending_tasks(self) -> List['Task']:
        """Get all pending tasks for this pet"""
        return [task for task in self.tasks if task.status == "pending"]


@dataclass
class Task:
    """Represents a single activity (description, time, frequency, completion status)"""
    description: Optional[str] = None
    duration: Optional[int] = None  # Duration in minutes
    priority: int = Priority.MEDIUM  # Use Priority enum
    status: str = "pending"  # pending, scheduled, completed, skipped
    frequency: str = "once"  # once, daily, weekly, multiple_daily
    pet: Optional['Pet'] = None

    def change_status(self, new_status: str) -> None:
        """Change the status of this task"""
        match new_status:
            case "completed":
                self.status = "completed"
            case "scheduled":
                self.status = "scheduled"
            case "skipped":
                self.status = "skipped"
            case "pending":
                self.status = "pending"
            case _:
                raise ValueError(f"Invalid status: {new_status}. Must be 'pending', 'scheduled', 'completed', or 'skipped'.")

    def update_task(self, description: Optional[str] = None,
                    duration: Optional[int] = None,
                    priority: Optional[int] = None,
                    frequency: Optional[str] = None) -> None:
        """Update task properties"""
        if description is not None:
            self.description = description
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority
        if frequency is not None:
            self.frequency = frequency


class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets"""

    def __init__(self, owner: Optional[Owner] = None):
        """Initialize scheduler with an owner (and their pets)"""
        self.owner = owner

    def generate_schedule(self) -> Dict:
        """
        Generate a daily schedule based on owner's pets, tasks, and constraints.

        Returns a dictionary with:
        - scheduled_tasks: List of dicts with task, start_time, end_time, reason
        - skipped_tasks: List of dicts with task and reason
        - total_time_used: Total minutes scheduled
        - explanation: Human-readable explanation of the schedule
        """
        if not self.owner:
            return {
                "scheduled_tasks": [],
                "skipped_tasks": [],
                "total_time_used": 0,
                "explanation": "No owner specified for scheduling."
            }

        # Get all pending tasks from all pets
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.get_pending_tasks())

        if not all_tasks:
            return {
                "scheduled_tasks": [],
                "skipped_tasks": [],
                "total_time_used": 0,
                "explanation": "No pending tasks to schedule."
            }

        # Sort tasks by priority (HIGH to LOW)
        sorted_tasks = self._sort_tasks_by_priority(all_tasks)

        # Schedule tasks within available time
        scheduled_tasks = []
        skipped_tasks = []
        schedule_start_time = self._get_start_time()  # Get start time from preferences
        current_time = schedule_start_time
        available_time_minutes = self._calculate_total_available_time()
        schedule_end_time = schedule_start_time + available_time_minutes  # Calculate end of available window

        for task in sorted_tasks:
            if task.duration is None or task.duration <= 0:
                skipped_tasks.append({
                    "task": task,
                    "reason": "Task has no valid duration specified"
                })
                continue

            # Check if task fits within the remaining window
            if current_time + task.duration <= schedule_end_time:
                task_start_time = current_time
                task_end_time = current_time + task.duration

                priority_label = Priority(task.priority).name
                pet_name = task.pet.name if task.pet else "unknown pet"

                scheduled_tasks.append({
                    "task": task,
                    "start_time_minutes": task_start_time,
                    "end_time_minutes": task_end_time,
                    "time_range": f"{self._format_time(task_start_time)} - {self._format_time(task_end_time)}",
                    "reason": f"Priority: {priority_label}, Duration: {task.duration}min, Pet: {pet_name}"
                })

                current_time = task_end_time
                task.change_status("scheduled")
            else:
                skipped_tasks.append({
                    "task": task,
                    "reason": f"Insufficient time remaining ({schedule_end_time - current_time}min available, {task.duration}min needed)"
                })
                task.change_status("skipped")

        # Generate explanation
        explanation = self._generate_explanation(
            scheduled_tasks, skipped_tasks, available_time_minutes, current_time - schedule_start_time
        )

        return {
            "scheduled_tasks": scheduled_tasks,
            "skipped_tasks": skipped_tasks,
            "total_time_used": current_time - schedule_start_time,
            "explanation": explanation
        }

    def _calculate_total_available_time(self) -> int:
        """Calculate total available time from owner"""
        if self.owner:
            return self.owner.available_time_minutes
        return 480  # Default 8 hours

    def _get_start_time(self) -> int:
        """Get start time based on owner preferences (morning/afternoon/evening)"""
        if not self.owner or not self.owner.preferences:
            return 0  # Default to midnight

        # Check for preferred_time_window preference
        time_window = self.owner.preferences.get("preferred_time_window", "").lower()

        # Define time windows (in minutes from midnight)
        time_windows = {
            "morning": 360,     # 6:00 AM
            "afternoon": 720,   # 12:00 PM (noon)
            "evening": 1080     # 6:00 PM
        }

        # Return the start time for the preferred window, or 0 if not found
        return time_windows.get(time_window, 0)

    def _sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority (HIGH to LOW), then by duration (shorter first)"""
        return sorted(tasks, key=lambda t: (-t.priority, t.duration if t.duration else 0))

    def _can_fit_task(self, task: Task, remaining_time: int) -> bool:
        """Check if a task can fit in the remaining available time"""
        if task.duration is None:
            return False
        return task.duration <= remaining_time

    def _format_time(self, minutes: int) -> str:
        """Convert minutes from start of day to HH:MM format"""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"

    def _generate_explanation(self, scheduled_tasks: List[Dict],
                            skipped_tasks: List[Dict],
                            available_time: int,
                            time_used: int) -> str:
        """Generate a human-readable explanation of the schedule"""
        explanation_parts = []

        # Base explanation with time preference if set
        base_explanation = f"Schedule generated for {self.owner.name if self.owner.name else 'pet owner'} "
        base_explanation += f"with {available_time}min available time"

        # Add time preference if specified
        if self.owner and self.owner.preferences:
            time_window = self.owner.preferences.get("preferred_time_window")
            if time_window:
                base_explanation += f", starting in the {time_window}"

        base_explanation += "."
        explanation_parts.append(base_explanation)

        if scheduled_tasks:
            explanation_parts.append(
                f"\nScheduled {len(scheduled_tasks)} task(s) using {time_used}min total. "
                f"Tasks were prioritized by importance (HIGH > MEDIUM > LOW) and then by duration."
            )

        if skipped_tasks:
            explanation_parts.append(
                f"\nSkipped {len(skipped_tasks)} task(s) due to time constraints or missing information."
            )

        return " ".join(explanation_parts)
