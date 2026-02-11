#!/usr/bin/env python3
"""
Testing ground for PawPal+ system
"""

from pawpal_system import Owner, Pet, Task, Scheduler, Priority


def main():
    # Create an owner
    owner = Owner(
        name="Alex",
        contact_info="alex@email.com",
        available_time_minutes=240,  # 4 hours available today
        preferences={"preferred_time_window": "morning"}  # Prefer morning tasks
    )

    # Create two pets
    dog = Pet(
        name="Buddy",
        age=3,
        type="Dog"
    )

    cat = Pet(
        name="Whiskers",
        age=5,
        type="Cat"
    )

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create tasks for the dog
    dog_walk = Task(
        description="Morning walk",
        duration=30,
        priority=Priority.HIGH,
        frequency="daily"
    )

    dog_feeding = Task(
        description="Breakfast",
        duration=10,
        priority=Priority.HIGH,
        frequency="daily"
    )

    dog_play = Task(
        description="Playtime in backyard",
        duration=45,
        priority=Priority.MEDIUM,
        frequency="daily"
    )

    # Create tasks for the cat
    cat_feeding = Task(
        description="Breakfast",
        duration=5,
        priority=Priority.HIGH,
        frequency="daily"
    )

    cat_litter = Task(
        description="Clean litter box",
        duration=10,
        priority=Priority.MEDIUM,
        frequency="daily"
    )

    cat_grooming = Task(
        description="Brush fur",
        duration=15,
        priority=Priority.LOW,
        frequency="weekly"
    )

    # Add tasks to pets
    dog.add_task(dog_walk)
    dog.add_task(dog_feeding)
    dog.add_task(dog_play)

    cat.add_task(cat_feeding)
    cat.add_task(cat_litter)
    cat.add_task(cat_grooming)

    # Print header
    print("=" * 60)
    print("🐾 PAWPAL+ - Today's Pet Care Schedule 🐾")
    print("=" * 60)
    print(f"\nOwner: {owner.name}")
    print(f"Available Time: {owner.available_time_minutes} minutes")
    print(f"Pets: {', '.join(pet.name for pet in owner.pets)}")
    print(f"Total Pending Tasks: {len(owner.get_all_tasks())}")

    # Create scheduler and generate schedule
    scheduler = Scheduler(owner=owner)
    schedule = scheduler.generate_schedule()

    # Print the schedule
    print("\n" + "=" * 60)
    print("📅 SCHEDULED TASKS")
    print("=" * 60)

    if schedule["scheduled_tasks"]:
        for i, scheduled_task in enumerate(schedule["scheduled_tasks"], 1):
            task = scheduled_task["task"]
            pet_name = task.pet.name if task.pet else "Unknown"
            print(f"\n{i}. {task.description} ({pet_name})")
            print(f"   Time: {scheduled_task['time_range']}")
            print(f"   Reason: {scheduled_task['reason']}")
    else:
        print("\nNo tasks scheduled.")

    # Print skipped tasks
    if schedule["skipped_tasks"]:
        print("\n" + "=" * 60)
        print("⏭️  SKIPPED TASKS")
        print("=" * 60)
        for i, skipped in enumerate(schedule["skipped_tasks"], 1):
            task = skipped["task"]
            pet_name = task.pet.name if task.pet else "Unknown"
            print(f"\n{i}. {task.description} ({pet_name})")
            print(f"   Reason: {skipped['reason']}")

    # Print summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(schedule["explanation"])
    print(f"\nTime Used: {schedule['total_time_used']} / {owner.available_time_minutes} minutes")
    print(f"Scheduled: {len(schedule['scheduled_tasks'])} tasks")
    print(f"Skipped: {len(schedule['skipped_tasks'])} tasks")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
