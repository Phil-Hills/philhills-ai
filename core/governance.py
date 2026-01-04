"""
Governance Sidecar - Circuit Breakers & Resource Limits
Ensures agentic safety and cost control.
"""

class GovernanceSidecar:
    def __init__(self, agent_id, budget_limit=10.0):
        self.agent_id = agent_id
        self.budget_limit = budget_limit
        self.current_spend = 0.0
        self.recursion_depth = 0
        self.MAX_RECURSION = 5

    def check_operation(self, cost, is_recursive=False):
        """
        Validates if an operation is within safety bounds.
        """
        # Budget Check
        if self.current_spend + cost > self.budget_limit:
            raise PermissionError(f"GOVERNANCE_HALT: Budget Exceeded for {self.agent_id}")
        
        # Recursion Check
        if is_recursive:
            self.recursion_depth += 1
            if self.recursion_depth > self.MAX_RECURSION:
                 raise RecursionError(f"GOVERNANCE_HALT: Max Recursion Depth ({self.MAX_RECURSION})")

        self.current_spend += cost
        return True

    def reset_depth(self):
        self.recursion_depth = 0

if __name__ == "__main__":
    # Test Circuit Breaker
    gov = GovernanceSidecar("AGENT_TEST")
    try:
        for i in range(20):
            gov.check_operation(1.0)
            print(f"Op {i} allowed.")
    except PermissionError as e:
        print(e)
