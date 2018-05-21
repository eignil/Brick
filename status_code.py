import enum

@enum.unique
class StatusCode(enum.Enum):
    SUCCESS = 0
    FAIL    = -1
    WRITE_FAIL = 2
    READ_FAIL = 3
    RW_NOT_MATCH = 4