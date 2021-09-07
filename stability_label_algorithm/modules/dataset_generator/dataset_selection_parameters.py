class DatasetSelectionParameters:
    def __init__(self,
                 allow_support_cycle: bool = True,
                 allow_irrelevance_issues: bool = True,
                 allow_inconsistency_issues: bool = True):
        self.allow_support_cycle = allow_support_cycle
        self.allow_irrelevance_issues = allow_irrelevance_issues
        self.allow_inconsistently_issues = allow_inconsistency_issues
