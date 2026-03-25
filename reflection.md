# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
   - The design models a pet care scheduling system using five classes. An `Owner` manages multiple `Pet` objects, each pet owns its own list of `Task` objects, and a `Scheduler` retrieves all tasks across the owner's pets, fits them within the time budget, and returns a `Schedule`.

- What classes did you include, and what responsibilities did you assign to each?
   - **Owner**: holds the owner's name, daily time budget (`available_minutes`), optional preferences, and a list of pets. It is the primary constraint that drives scheduling.
   - **Pet**: stores the pet's name, species, age, special needs, and owns its list of care tasks.
   - **Task**: represents a single care activity with a title, duration, priority (low, medium, or high), category, frequency, completion status, and optional notes.
   - **Schedule**: the output of planning. Holds two lists: tasks that fit within the time budget, and tasks that did not. A pure data container with no logic.
   - **Scheduler**: the core engine. Takes an `Owner`, retrieves tasks across all pets, and exposes `generate_plan()`, which sorts tasks by priority and fits them within the time budget, and `explain_plan()`, which narrates why each task was included or excluded.

**b. Design changes**

- Did your design change during implementation?
   - Yes.

- If yes, describe at least one change and why you made it.
   - The `Task` class stores priority as a string (`"low"`, `"medium"`, `"high"`), but `generate_plan()` needs to sort tasks by priority. Since strings cannot be sorted numerically, a `PRIORITY_ORDER` mapping (`{"low": 1, "medium": 2, "high": 3}`) was added to convert it to an integer for sorting inside `generate_plan()`. The `Task` class itself stays unchanged.

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
