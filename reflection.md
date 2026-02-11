# PawPal+ Project Reflection

## 1. System Design

Three core actions a user should be able to perform are allowing a user to add a new pet/owner combination with info about them, adding and editing tasks, and displaying the day's tasks.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My UML design has four classes: Owner, Pet, Task, and Scheduler. Owner has basic info for an owner of a pet like name, contact information, and preferences, and methods to add and remove a pet. Pet has information like name, age, type, and a list of tasks assigned to that pet, and methods to add and remove tasks. The relationship between Owner and Pet is that Owner owns a Pet. Task is a class that has a description, a duration, a priority, and a status. Pets have Tasks. The last class, Scheduler, has a list of tasks and a list of constraints, and the ability to generate schedules and explain schedules.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, I made several changes. One of the changes I made was adding a list of Pets to the Owner class as an attribute. Before, I had methods to add and remove pets, but no way to store which pets belonged to which owners. This allows Pets and Owners to be tied together. After adding this suggestion with AI, I also realized that each Pet should have an owner, so I added that line myself. This way, pets and owners are connected in both directions.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
