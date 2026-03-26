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
   - **Scheduler**: the core engine. Takes an `Owner`, retrieves tasks across all pets, and exposes `generate_plan()`, which sorts tasks by priority and fits them within the time budget.

**b. Design changes**

- Did your design change during implementation?
   - Yes.

- If yes, describe at least one change and why you made it.
   - The `Task` class stores priority as a string (`"low"`, `"medium"`, `"high"`), but `generate_plan()` needs to sort tasks by priority. Since strings cannot be sorted numerically, a `PRIORITY_ORDER` mapping (`{"low": 1, "medium": 2, "high": 3}`) was added to convert it to an integer for sorting inside `generate_plan()`. The `Task` class itself stays unchanged.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
   - The scheduler considers two constraints: the owner's daily time budget (`available_minutes`) and each task's priority level (low, medium, or high). Tasks are sorted by priority first, then by duration as a tiebreaker when two tasks share the same priority.

- How did you decide which constraints mattered most?
   - Time is the hard constraint - the scheduler never exceeds `available_minutes`. Priority determines the order tasks are considered, so high-priority tasks are always evaluated before lower-priority ones. This ensures the most important tasks get scheduled first when time is limited.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
   - The scheduler uses a greedy approach: it processes tasks in priority order and skips any task that does not fit in the remaining time, even if a smaller lower-priority task could still fit. For example, if a high-priority 45-minute task cannot fit, the scheduler moves it to unscheduled and continues - it does not go back to try fitting it later after smaller tasks are added.

- Why is that tradeoff reasonable for this scenario?
   - For a daily pet care routine, simplicity and predictability matter more than perfect optimization. The greedy approach is easy to understand and explain to the user, and the tiebreaker (shortest task first within the same priority) already helps pack more tasks into the schedule.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
   - AI was used across every phase of the project. 
    - During design, it helped translate a plain-English description of the system into a UML class diagram and identify which responsibilities belonged on which class. 
    - During implementation, it generated method stubs and filled in logic like the `PRIORITY_ORDER` mapping and the `timedelta` date math in `reschedule_if_recurring()`. 
    - During testing, it proposed test cases and edge cases for each behavior, then wrote the actual test functions once the edge cases were agreed on. It also filled in the reflection prompts based on decisions made earlier in the project.

- What kinds of prompts or questions were most helpful?
   - Specific, scoped prompts worked best. Asking "write a test that verifies a daily task creates a new occurrence with due_date + 1 day" produced immediately usable code. Broad prompts like "write tests" produced generic output that needed heavy revision. Asking "what edge cases exist for this function" before writing any test code was also effective. It surfaced boundary conditions (month-end dates, midnight time slots, `once` frequency) that would not have been obvious from the happy-path implementation alone.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
   - The table header in the task list was visually cluttered. Columns were uneven and hard to read. Since the AI cannot see the rendered UI, it had no way to observe the problem directly. When asked to fix the layout, it proposed injecting roughly 50 lines of custom CSS to override Streamlit's default table styles. The suggestion looked technically valid in isolation, but running it made no visible improvement and added a large block of hard-to-maintain code for a problem that did not require it. The actual fix was adjusting the column weight numbers passed to `st.columns()` directly: `st.columns([1, 1, 1, 1.5, 1.1, 1, 1.1, 1, 1])`. One line, no CSS.

- How did you evaluate or verify what the AI suggested?
   - The AI's suggestion was evaluated by applying it and checking the rendered output in the browser. The CSS injection did not change how the header looked, which confirmed it was solving the wrong problem. The root cause was the column proportions, not the styling. Once the weights were tuned manually, the header aligned correctly. The lesson is that AI suggestions about visual layout need to be verified by actually rendering the result. The AI reasons about code structure but cannot observe what the user sees.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
   - **Task completion**: verified that `mark_complete()` flips `completion_status` from `False` to `True`. This is the most fundamental state change in the system and everything that depends on filtering completed vs. incomplete tasks relies on it being correct.
   - **Task addition**: verified that appending a task to a pet increases the task count. Important because the rest of the system (scheduling, filtering, conflict detection) reads from `pet.tasks`: a silent failure here would corrupt all downstream results.
   - **Sorting correctness**: verified that `sort_by_time()` returns tasks in chronological order across normal, already-sorted, single-item, midnight boundary, and all-identical-time inputs. Correct ordering is what makes the displayed schedule readable and predictable.
   - **Recurrence logic**: verified that `reschedule_if_recurring()` marks the original task complete and creates the next occurrence with the correct due date for daily and weekly frequencies, rolls correctly over month and year boundaries, and returns `None` without adding a task for `frequency="once"`.
   - **Conflict detection**: verified that `detect_time_conflicts()` produces one warning per conflicting time slot (not per conflicting pair), catches conflicts across different pets, correctly handles three-way conflicts, and does not exempt midnight (`00:00`). Also verified the no-conflict path returns an empty list.

- Why were these tests important?
   - Each test targets a behavior that is invisible to the Streamlit UI unless something goes wrong visibly. Without tests, a date-rollover bug or a silent conflict-detection miss could ship unnoticed. The edge cases in particular guard against assumptions that feel safe but break on boundaries, like month-end dates or midnight time slots.

**b. Confidence**

- How confident are you that your scheduler works correctly?
   - **Confidence level:  (4/5)**. The 18 passing tests cover the core behaviors reliably: sorting, recurrence date math across boundaries, and conflict detection across all meaningful cases. The fundamentals, such as task completion, task addition, are solid. 
        - The missing star reflects untested areas: the greedy packing logic in `generate_plan()` under tight time budgets, and `filter_tasks()` with combined pet-name and status filters. Those paths are exercised manually through the UI but have no automated coverage yet: a regression there would not be caught automatically.

- What edge cases would you test next if you had more time?
   - `generate_plan()` with zero available minutes (every task lands in `unscheduled`).
   - `generate_plan()` where a lower-priority short task fits but the higher-priority long task does not: verifying the greedy order still holds.
   - `filter_tasks()` with both `pet_name` and `status` filters active at the same time.
   - `reschedule_if_recurring()` called on a task that is not yet in `pet.tasks` (verifying it still appends correctly).
   - Conflict detection via the explicit `tasks=` parameter path, where the pet lookup falls back to `"Unknown"`.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
   - The separation of concerns between classes. `Task` holds data only, `Pet` owns its tasks, `Scheduler` owns all logic, and `Schedule` is a pure output container. Because each class has one clear job, adding features like conflict detection and recurrence required no changes to existing classes where new methods dropped into `Scheduler` without touching anything else. That made the codebase easy to extend and easy to test in isolation.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
   - The conflict detection model. Right now it only flags tasks that share the exact same `scheduled_time` string. A more realistic version would check whether time intervals overlap: a 30-minute task at `08:00` and a 20-minute task at `08:15` conflict in practice but pass the current check. I would store `scheduled_time` as a proper `datetime.time` object and compare `[start, start + duration)` intervals instead of raw strings.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
   - Writing tests first, or immediately after, forces you to be precise about what a function is actually supposed to do, not just what it seems to do. Several edge cases, such as month-end rollovers, midnight conflict slots, the `once` frequency returning `None`, were easy to miss during implementation but became obvious the moment a test had to assert a specific value. The act of writing the assertion is what surfaces the ambiguity.

- Which Copilot features were most effective for building your scheduler?
    - The conversational interface was the most useful feature throughout the project. It worked well for three specific tasks: translating a plain-English system description into a UML diagram, generating method stubs once the class structure was agreed on, and proposing edge cases before writing tests. Claude Code's ability to read multiple files at once and cross-reference them was especially useful.

- How did using separate chat sessions for different phases help you stay organized?
    - Keeping design, implementation, testing, and UI work in separate sessions prevented context from bleeding between phases.

- Summarize what you learned about being the "lead architect" when collaborating with powerful AI tools.
    - Claude Code does what you ask, not what you mean because often what you ask is underspecified. Being the lead architect means writing precise prompts, verifying every suggestion against the actual running system, and being willing to reject output that is technically correct but architecturally wrong.

