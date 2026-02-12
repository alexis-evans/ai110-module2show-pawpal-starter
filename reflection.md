# PawPal+ Project Reflection

## 1. System Design

Three core actions a user should be able to perform are allowing a user to add a new pet/owner combination with info about them, adding and editing tasks, and displaying the day's tasks.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My UML design has four classes: Owner, Pet, Task, and Scheduler. Owner has basic info for an owner of a pet like name, hours available in a day for pet-related tasks, and preferences, and methods to add and remove a pet. Pet has information like name, age, type, and a list of tasks assigned to that pet, and methods to add and remove tasks. The relationship between Owner and Pet is that Owner owns a Pet and a Pet is owned by an Owner. Task is a class that has a description, a duration, a priority, and a status. Pets have Tasks and each Task belongs to one Pet. The last class, Scheduler, has a list of tasks and a list of constraints, and the ability to generate schedules and explain schedules.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, I made several changes. One of the changes I made was adding a list of Pets to the Owner class as an attribute. Before, I had methods to add and remove pets, but no way to store which pets belonged to which owners. This allows Pets and Owners to be tied together. After adding this suggestion with AI, I also realized that each Pet should have an owner, so I added that line myself. This way, pets and owners are connected in both directions.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers task priority (high > medium > low), task duration, total owner availability (time budget for day), preferred time window (morning, afternoon, or evening) as a preference -- but not end all be all, explicit task times as hard constraints (HH:MM), and task status (it only schedules pending tasks).

I prioritize explicit times first because the user inputted them manually at that time, then priority, then fit with available total time. The preferred time window does not override explicit user-set times.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that it allows scheduling conflicts instead of skipping them, but it flags them as overlapping so the user is aware. The tradeoff is reasonable because sometimes you can do two things at once, like feed two cats at the same time. Other times, it doesn't make sense to do two things at once, like feeding an animal at home and being on a walk with a pet at the same time. This way, the user is made aware of any scheduling conflicts and can set other times if it doesn't make sense to do them both at the same time or have them overlap. It also allows the user to keep as many of the tasks that they scheduled at once without dropping them.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used it for brainstorming, coming up with a UML diagram, debugging, refactoring, test writing, and implementation. The prompts that were most helpful were bug reports that I experienced when running the app myself, and behavior focused requests like "I want to add this feature" or "This should not happen anymore" even if they weren't necessarily *bugs*.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When I was working on the explicit time tasks, I noticed that if you set a preference for a time, but scheduled a task for a specific time outside of that window, that the scheduler would just skip the task because it didn't fit the user preference. This didn't make sense to me because a user knows that the time they chose for the task may fall outside of that preferred window, but maybe that task just has to happen at that time and the user still wants it on the schedule. The way I evaluated what the AI suggested as a fix was creating and running test cases that passed, seeing if the app compiled, and then testing out the edge case myself. If all three worked, I figured the code was working as expected.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested task status transitions, task additions to pets, explicit-time scheduling, and fixed-time task behavior around preferred windows. These tests were important because they represented key functionalities of the scheduler, and also edge cases that the scheduler previously did not work as intented.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm fairly confident that the scheduler works as expected. Some edge cases that I would test if I had more time would be: conflict heavy schedules with a lot of tasks that overlap but have fixed times. Editing tasks and making sure the task object doesn't have weird side effects to changing some of its values, recurring tasks completion in terms of how it repopulates recurring tasks in the current task view and the new schedules, and more testing around streamlit states and keeping what needs to be kept and discarding what's safe to get rid of.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the owner, pet, and task creation fields. I feel like it makes sense for what I would expect a user to want to input about a task or an animal or themselves and their preferences, and I think the scheduler really does a good job accommodating those things well.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would redesign the scheduler UI because right now it's just a list, and I would like it to be a time-blocked calendar view, or have multiple views that you can toggle between. I think that would make it more user-friendly, but I don't know how to do that in Streamlit yet...

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that AI can handle really complex tasks, and it's a lot better than where it was just a few years ago. However, it's still not perfect, and it misses a lot, but if you give it direction, it can execute very, very well.
