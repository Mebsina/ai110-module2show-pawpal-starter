"""Phase 1: System Design with UML + AI Support

All five core classes are defined here with attribute declarations and
method signatures only. No scheduling logic is implemented yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

PRIORITY_ORDER: dict[str, int] = {
    "low": 1,
    "medium": 2,
    "high": 3,
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Task:
    """Represents a single care task assigned to a pet.

    Attributes
    ----------
    title:
        Human-readable name for the task.
    duration_minutes:
        How long the task takes to complete.
    priority:
        One of "low", "medium", or "high" (see PRIORITY_ORDER).
    category:
        Broad grouping such as "walk", "feeding", "meds",
        "grooming", or "enrichment".
    frequency:
        How often the task recurs, e.g. "daily", "weekly", "once".
    completion_status:
        Whether the task has been completed today.
    notes:
        Optional free-text notes about the task.
    """

    title: str
    duration_minutes: int
    priority: str
    category: str
    frequency: str
    completion_status: bool = False
    notes: str = ""


@dataclass
class Pet:
    """Represents a pet and its associated care tasks.

    Attributes
    ----------
    name:
        The pet's name.
    species:
        The pet's species (e.g. "dog", "cat").
    age:
        The pet's age in years.
    special_needs:
        List of special needs or conditions (e.g. ["diabetic", "senior"]).
    tasks:
        List of care tasks assigned to this pet.
    """

    name: str
    species: str
    age: int
    special_needs: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)


@dataclass
class Owner:
    """Represents the pet owner and their daily time budget.

    Attributes
    ----------
    name:
        The owner's name.
    available_minutes:
        Total minutes per day available for pet care.
    preferences:
        Optional key/value preferences (e.g. {"morning_tasks": ["walk"]}).
    pets:
        List of pets the owner manages.
    """

    name: str
    available_minutes: int
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)


@dataclass
class Schedule:
    """The result produced by Scheduler.generate_plan().

    Attributes
    ----------
    tasks:
        Ordered list of tasks that fit within the owner's time budget.
    total_duration:
        Sum of duration_minutes for all scheduled tasks.
    unscheduled:
        Tasks that could not fit within the available time.
    """

    tasks: list[Task] = field(default_factory=list)
    total_duration: int = 0
    unscheduled: list[Task] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------


@dataclass
class Scheduler:
    """Generates a daily care schedule across all of an owner's pets.

    Retrieves tasks from every pet in owner.pets, sorts them by priority
    (with duration as a tiebreaker), and fits them within the owner's
    available_minutes budget.
    """

    owner: Owner

    def generate_plan(self) -> Schedule:
        """Retrieve all tasks from owner's pets and build a schedule.

        Returns
        -------
        Schedule
            A Schedule whose .tasks list contains every task that fit,
            and whose .unscheduled list contains every task that did not.
        """
        pass

    def explain_plan(self, schedule: Schedule) -> str:
        """Return an explanation of the generated plan.

        Parameters
        ----------
        schedule:
            A Schedule previously returned by generate_plan().

        Returns
        -------
        str
            Explanation of why each task was scheduled or skipped.
        """
        pass
