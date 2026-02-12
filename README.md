# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

---
---

## Smarter Scheduling

PawPal+ now includes smarter planning behavior to better match real user intent:

- **Explicit times are honored**: tasks with a set time (like `08:00`) are scheduled at that exact time.
- **Preference-aware scheduling**: tasks without a set time are placed starting from your preferred window (morning/afternoon/evening), with a default start around **8:00 AM** if no preference is chosen.
- **Conflict visibility**: overlapping timed tasks are allowed, but clearly flagged with caution indicators.
- **Recurring task automation**: completing daily/weekly tasks can automatically create the next occurrence.
- **Task editing improvements**: tasks can be edited after creation, including moving a task to a different pet.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

Test coverage includes core domain and scheduling behavior: owner/pet/task management, status transitions, task updates, recurrence logic (daily/weekly), fixed-time scheduling, chronological sorting, priority ordering, filter/sort helpers, conflict detection, boundary conditions, and skipped-task edge cases.

Confidence Level: ⭐️⭐️⭐️⭐️
4/5 stars based on current automated test results. Feel pretty confident, but you can always miss something.

## Features

- **Chronological schedule output**: final scheduled tasks are sorted by start time for a clear day plan.
- **Fixed-time task honoring**: tasks with explicit `HH:MM` times are scheduled at those exact times.
- **Priority-based scheduling**: flexible tasks are ordered by priority (HIGH to LOW), then shorter duration first.
- **Preference-aware start windows**: flexible tasks start from preferred windows (`morning`, `afternoon`, `evening`) with fallback search if needed.
- **Time-budget constraints**: scheduling respects total available minutes and skips tasks that cannot fit.
- **Gap-based slot finding**: flexible tasks are placed in the earliest available non-overlapping slot.
- **Conflict warnings**: overlapping timed tasks are detected and reported as conflict alerts.
- **Task status workflow**: tasks move through `pending`, `scheduled`, `completed`, and `skipped`.
- **Daily/weekly recurrence**: completing recurring tasks automatically creates the next occurrence.
- **Task filtering and time sorting utilities**: helper methods support filtering by pet/status and sorting by task time.

## Demo 📸

![PawPal+ Demonstration Screenshot](PawPal_Final.png)

