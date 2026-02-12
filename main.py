#!/usr/bin/env python3
"""
PawPal+ Demo: Algorithmic Features
This script demonstrates sorting, filtering, recurring tasks, and conflict detection.
"""

from pawpal_system import Owner, Pet, Task, Scheduler, Priority
from datetime import datetime

def print_separator(title=""):
    """Print a visual separator"""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    print()

def print_task_list(tasks, title="Tasks"):
    """Print a formatted list of tasks"""
    print(f"\n{title}:")
    print("-" * 70)
    if not tasks:
        print("  (No tasks)")
    for i, task in enumerate(tasks, 1):
        pet_name = task.pet.name if task.pet else "No pet"
        time_str = f" at {task.time}" if task.time else ""
        print(f"  {i}. {task.description} ({pet_name}){time_str} - "
              f"{task.duration}min - {Priority(task.priority).name} - {task.status}")
    print()

def main():
    print_separator("🐾 PawPal+ Algorithmic Features Demo 🐾")

    # ========================================================================
    # Setup: Create owner and pets
    # ========================================================================
    print("Setting up owner and pets...")
    owner = Owner(
        name="Alex",
        available_time_minutes=360,  # 6 hours
        preferences={"preferred_time_window": "morning"}
    )

    # Create pets
    dog = Pet(name="Buddy", age=5, type="Dog")
    cat = Pet(name="Whiskers", age=3, type="Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    print(f"✓ Owner: {owner.name}")
    print(f"✓ Pets: {dog.name} (Dog), {cat.name} (Cat)")

    # ========================================================================
    # Feature 1: Add tasks with specific times (out of order)
    # ========================================================================
    print_separator("Feature 1: Adding Tasks (Out of Order)")

    # Add tasks with times - intentionally out of order
    task1 = Task(
        description="Morning walk",
        duration=30,
        priority=Priority.HIGH,
        time="08:00",
        frequency="daily",
        due_date=datetime.now()
    )
    dog.add_task(task1)

    task2 = Task(
        description="Feed breakfast",
        duration=15,
        priority=Priority.HIGH,
        time="07:00"  # Earlier than walk
    )
    dog.add_task(task2)

    task3 = Task(
        description="Play fetch",
        duration=20,
        priority=Priority.MEDIUM,
        time="10:00"
    )
    dog.add_task(task3)

    task4 = Task(
        description="Feed cat",
        duration=10,
        priority=Priority.HIGH,
        time="07:00"  # Same time as dog breakfast - CONFLICT!
    )
    cat.add_task(task4)

    task5 = Task(
        description="Clean litter box",
        duration=15,
        priority=Priority.MEDIUM,
        time="09:00",
        frequency="daily",
        due_date=datetime.now()
    )
    cat.add_task(task5)

    # Add a task without a specific time
    task6 = Task(
        description="Groom Buddy",
        duration=45,
        priority=Priority.LOW
    )
    dog.add_task(task6)

    all_tasks = owner.get_all_tasks()
    print_task_list(all_tasks, "All Tasks (Added Out of Order)")

    # ========================================================================
    # Feature 2: Sorting by Time
    # ========================================================================
    print_separator("Feature 2: Sort Tasks by Time")

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time(all_tasks)

    print_task_list(sorted_tasks, "Tasks Sorted by Time")
    print("Note: Tasks without a time appear at the end.")

    # ========================================================================
    # Feature 3: Filtering Tasks
    # ========================================================================
    print_separator("Feature 3: Filter Tasks")

    # Filter by pet
    dog_tasks = scheduler.filter_tasks(all_tasks, pet_name="Buddy")
    print_task_list(dog_tasks, f"Tasks for {dog.name}")

    cat_tasks = scheduler.filter_tasks(all_tasks, pet_name="Whiskers")
    print_task_list(cat_tasks, f"Tasks for {cat.name}")

    # Filter by status
    pending_tasks = scheduler.filter_tasks(all_tasks, status="pending")
    print_task_list(pending_tasks, "Pending Tasks")

    # Filter by both pet and status
    dog_pending = scheduler.filter_tasks(all_tasks, pet_name="Buddy", status="pending")
    print_task_list(dog_pending, f"Pending Tasks for {dog.name}")

    # ========================================================================
    # Feature 4: Conflict Detection
    # ========================================================================
    print_separator("Feature 4: Detect Scheduling Conflicts")

    conflicts = scheduler.detect_conflicts(all_tasks)

    if conflicts:
        print(f"Found {len(conflicts)} conflict(s):\n")
        for conflict in conflicts:
            print(f"  {conflict['message']}\n")
    else:
        print("✓ No scheduling conflicts detected!")

    # ========================================================================
    # Feature 5: Recurring Tasks Automation
    # ========================================================================
    print_separator("Feature 5: Recurring Tasks Automation")

    print("Before completing recurring tasks:")
    print(f"  Total tasks for {dog.name}: {len(dog.tasks)}")
    print(f"  Total tasks for {cat.name}: {len(cat.tasks)}")

    # Mark recurring tasks as complete
    print("\nMarking daily tasks as complete...")
    new_task1 = task1.mark_complete()  # Morning walk (daily)
    new_task2 = task5.mark_complete()  # Clean litter box (daily)

    if new_task1:
        print(f"  ✓ Created new task: '{new_task1.description}' for {new_task1.due_date.strftime('%Y-%m-%d')}")
    if new_task2:
        print(f"  ✓ Created new task: '{new_task2.description}' for {new_task2.due_date.strftime('%Y-%m-%d')}")

    print("\nAfter completing recurring tasks:")
    print(f"  Total tasks for {dog.name}: {len(dog.tasks)} (should be same - old task replaced by new)")
    print(f"  Total tasks for {cat.name}: {len(cat.tasks)} (should be same - old task replaced by new)")

    # Show status of original tasks
    print("\nOriginal task statuses:")
    print(f"  Morning walk: {task1.status}")
    print(f"  Clean litter box: {task5.status}")

    # Show new tasks
    dog_pending_after = scheduler.filter_tasks(dog.tasks, status="pending")
    cat_pending_after = scheduler.filter_tasks(cat.tasks, status="pending")
    print_task_list(dog_pending_after, f"New Pending Tasks for {dog.name}")
    print_task_list(cat_pending_after, f"New Pending Tasks for {cat.name}")

    # ========================================================================
    # Feature 6: Combined Demo - Sort, Filter, and Check Conflicts
    # ========================================================================
    print_separator("Feature 6: Combined Demo")

    print("Workflow: Get pending tasks → Sort by time → Check conflicts")
    print()

    # Get all pending tasks
    all_current_tasks = owner.get_all_tasks()
    pending = scheduler.filter_tasks(all_current_tasks, status="pending")
    print(f"Step 1: Found {len(pending)} pending tasks")

    # Sort them by time
    sorted_pending = scheduler.sort_by_time(pending)
    print(f"Step 2: Sorted {len(sorted_pending)} tasks by time")
    print_task_list(sorted_pending, "Sorted Pending Tasks")

    # Check for conflicts
    conflicts_check = scheduler.detect_conflicts(sorted_pending)
    print(f"Step 3: Conflict check - {len(conflicts_check)} conflict(s) found")
    if conflicts_check:
        for conflict in conflicts_check:
            print(f"  {conflict['message']}")

    print_separator("✨ Demo Complete! ✨")
    print("Key Takeaways:")
    print("  ✓ Sorting: Tasks can be ordered by time using lambda functions")
    print("  ✓ Filtering: Tasks can be filtered by pet name and/or status")
    print("  ✓ Recurring: Daily/weekly tasks auto-create new instances when completed")
    print("  ✓ Conflicts: System detects when tasks have overlapping time windows")
    print()

if __name__ == "__main__":
    main()
