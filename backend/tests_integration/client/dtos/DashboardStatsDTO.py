from typing import Dict


class DashboardStatsDTO:
    def __init__(self, agreement_types: Dict[str, int], jurisdictions: Dict[str, int]):
        self.agreement_types = agreement_types
        self.jurisdictions = jurisdictions


