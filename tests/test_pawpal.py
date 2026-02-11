"""
Tests for PawPal+ system
"""

from pawpal_system import Pet, Task, Priority


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
