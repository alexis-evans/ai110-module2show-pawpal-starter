"""
Tests for PawPal+ system
"""

from pawpal_system import Owner, Pet, Task, Scheduler, Priority


def test_task_completion():
    """Verify that calling change_status() actually changes the task's status"""
    # Create a task
    task = Task(
        description="Walk the dog",
        duration=30,
        priority=Priority.HIGH
    )

    # Initial status should be pending
    assert task.status == "pending"

    # Change status to completed
    task.change_status("completed")

    # Verify the status changed
    assert task.status == "completed"

    # Test other status changes
    task.change_status("scheduled")
    assert task.status == "scheduled"

    task.change_status("skipped")
    assert task.status == "skipped"


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count"""
    # Create a pet
    pet = Pet(
        name="Buddy",
        age=3,
        type="Dog"
    )

    # Initially, pet should have no tasks
    assert len(pet.tasks) == 0

    # Create and add first task
    task1 = Task(
        description="Morning walk",
        duration=30,
        priority=Priority.HIGH
    )
    pet.add_task(task1)

    # Verify task count increased
    assert len(pet.tasks) == 1

    # Create and add second task
    task2 = Task(
        description="Feed breakfast",
        duration=10,
        priority=Priority.HIGH
    )
    pet.add_task(task2)

    # Verify task count increased again
    assert len(pet.tasks) == 2

    # Verify the tasks are in the pet's task list
    assert task1 in pet.tasks
    assert task2 in pet.tasks

    # Verify the tasks are linked to the pet
    assert task1.pet == pet
    assert task2.pet == pet


def test_generate_schedule_honors_explicit_task_time():
    """Tasks with explicit HH:MM time should be scheduled at that exact time."""
    owner = Owner(
        name="Alex",
        available_time_minutes=600,  # 6:00 -> 16:00 when morning preference is set
        preferences={"preferred_time_window": "morning"}
    )
    pet = Pet(name="Buddy", age=4, type="Dog")
    owner.add_pet(pet)

    fixed_task = Task(
        description="Morning walk",
        duration=30,
        priority=Priority.HIGH,
        time="08:00"
    )
    flexible_task = Task(
        description="Brush coat",
        duration=20,
        priority=Priority.MEDIUM
    )
    pet.add_task(fixed_task)
    pet.add_task(flexible_task)

    scheduler = Scheduler(owner=owner)
    schedule = scheduler.generate_schedule()

    fixed_entry = next(item for item in schedule["scheduled_tasks"] if item["task"] is fixed_task)
    assert fixed_entry["start_time_minutes"] == 8 * 60
    assert fixed_entry["time_range"].startswith("08:00")


def test_generate_schedule_keeps_fixed_task_outside_preferred_window():
    """Fixed-time tasks outside preferred window should still be scheduled."""
    owner = Owner(
        name="Alex",
        available_time_minutes=120,
        preferences={"preferred_time_window": "morning"}
    )
    pet = Pet(name="Whiskers", age=2, type="Cat")
    owner.add_pet(pet)

    outside_task = Task(
        description="Late-night feed",
        duration=15,
        priority=Priority.HIGH,
        time="22:00"
    )
    pet.add_task(outside_task)

    scheduler = Scheduler(owner=owner)
    schedule = scheduler.generate_schedule()

    assert outside_task in [item["task"] for item in schedule["scheduled_tasks"]]
    assert outside_task not in [item["task"] for item in schedule["skipped_tasks"]]
