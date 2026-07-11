# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial design centered on four classes: Task, Pet, Owner, and Scheduler. Task holds the details of a single activity — description, due time, due date, frequency (once/daily/weekly), and completion status. Pet stores identifying info (name, species) and owns a list of its own Task objects, with methods to add and count tasks. Owner manages a list of Pet objects and can look up a pet by name or pull every task across all pets. Scheduler doesn't hold data itself — it takes an Owner and is responsible for the "smart" behavior: sorting tasks by time, filtering them, detecting conflicts, and handling recurrence when a task is completed.

**b. Design changes**

One change I made was moving recurrence logic onto Task.mark_complete() instead of putting it entirely in Scheduler. My first instinct was to have Scheduler regenerate recurring tasks by checking frequency itself, but that meant the Scheduler needed to know too much about how a Task's own recurrence math worked. Instead, I had Task.mark_complete() return a new Task for the next occurrence (or None if it doesn't recur), and let Scheduler.mark_task_complete() just handle adding that new task back to the right pet. That kept the "does this task repeat, and when's next" logic inside Task, where it belongs, and kept Scheduler focused on cross-pet coordination.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler's main constraint is time — specifically, each task's due date and due time. Tasks are organized purely by when they're due, since that's the most immediately actionable piece of information for a pet owner glancing at their day. I didn't build in a separate "priority" field, since for pet care tasks, urgency is usually implied by time (a scheduled feeding at 8am matters "now" regardless of how important it is relative to other tasks). Time was the constraint that mattered most because it's the one a pet owner actually needs to act on moment-to-moment.

**b. Tradeoffs**

One tradeoff my scheduler makes is that conflict detection only checks for exact matching times (same date and same HH:MM), rather than detecting overlapping durations. For example, if one task runs 08:00–08:30 and another starts at 08:15, my system won't flag that as a conflict since the start times don't match exactly. This is a reasonable simplification for this scenario because tasks here are treated as instantaneous events (a walk, a feeding) rather than tasks with a duration, so exact-time matching catches the most common real-world conflict: two things scheduled for the identical moment.

---

## 3. AI Collaboration

**a. How you used AI**

I used my AI coding assistant throughout — for brainstorming the initial class structure from the UML, generating the class skeletons, fleshing out full method implementations, and debugging issues as they came up (including a tricky file-sync issue between my editor and terminal that took a while to track down). The most helpful prompts were specific and scoped to one method at a time, like asking how Scheduler should retrieve tasks from Owner, or how to use timedelta for recurrence — narrow questions got me clean, usable answers faster than broad "build my whole app" requests.

**b. Judgment and verification**

One moment I didn't just accept AI output as-is was around recurrence logic. My first instinct (and an early AI suggestion) was to have Scheduler handle regenerating recurring tasks by checking Task.frequency itself. I pushed back on that because it meant Scheduler needed to know internal details about how Task recurrence math worked, which felt like the wrong class owning that responsibility. I changed it so Task.mark_complete() handles its own recurrence and just returns the next Task (or None), and Scheduler only handles slotting that new task back into the right pet. I verified this was working correctly by writing an actual test (test_recurrence_creates_next_day_task) rather than just trusting that it looked right.

---

## 4. Testing and Verification

**a. What you tested**

I tested five core behaviors: that mark_complete() correctly flips a task's status, that adding a task increases a pet's task count, that tasks are returned in correct chronological order regardless of the order they were added, that completing a recurring task generates a correctly-dated next occurrence, and that two tasks scheduled at the same date/time are correctly flagged as a conflict. These mattered because they cover both the basic data operations (add/complete) and the "smart" algorithmic behavior (sort/recur/conflict) that makes the app more than just a glorified list.

**b. Confidence**

I'd rate my confidence at 4/5. All five tests pass consistently, and I manually verified the CLI output matches expected behavior (sorted schedule, correct conflict warning, correct next-occurrence date). If I had more time, I'd test edge cases like: a pet with zero tasks, tasks with overlapping but non-identical times (since my conflict detection only catches exact time matches), and marking an already-completed task complete again.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with how the Scheduler class turned out — keeping it focused purely on cross-pet coordination (sorting, filtering, conflicts) while pushing task-specific logic like recurrence down into Task itself made the code easier to reason about and test in isolation.

**b. What you would improve**

If I did another iteration, I'd improve conflict detection to check for overlapping time ranges rather than exact time matches, since real pet-care tasks (like a 30-minute walk) can conflict with each other even if they don't start at the identical minute.

**c. Key takeaway**

The biggest thing I learned is that AI is much more useful as a collaborator on well-scoped questions than as an author of my whole system. I got the best results when I already had an opinion about how something should be structured and used AI to fill in or challenge that opinion, rather than asking it to design everything from scratch.