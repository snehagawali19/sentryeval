class SentryEvalError(Exception):
    pass


class ConfigurationError(SentryEvalError):
    pass


class DatasetIntegrityError(SentryEvalError):
    pass


class TargetError(SentryEvalError):
    pass


class BudgetExceededError(SentryEvalError):
    pass


class LiveTargetDisabledError(SentryEvalError):
    pass


class ReliabilityGateError(SentryEvalError):
    pass
