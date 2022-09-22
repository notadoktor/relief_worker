from enum import Enum, auto


class StrEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    def __str__(self) -> str:
        return self.value


class ShiftAction(StrEnum):
    APPROVE = auto()
    ASSIGN = auto()
    CANCEL = auto()
    CREATE = auto()
    DENY = auto()
    RELEASE = auto()
    REQUEST = auto()


class EmployeeStatus(StrEnum):
    PERMANENT = auto()
    CONTRACT = auto()


class WorkerRole(StrEnum):
    DOCTOR = auto()
    NURSE = auto()
    ADMINISTRATION = auto()


class ShiftStatus(StrEnum):
    OPEN = auto()
    CLOSED = auto()
    CANCELLED = auto()


class ShiftType(StrEnum):
    REGULAR = auto()
    OVERTIME = auto()
    HOLIDAY = auto()


class ShiftTime(StrEnum):
    MORNING = auto()
    AFTERNOON = auto()
    NIGHT = auto()


class ShiftDay(int, Enum):
    def __str__(self) -> str:
        return self.name.lower()

    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()


class WeekDay(int, Enum):
    def __str__(self) -> str:
        return self.name.lower()

    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()
