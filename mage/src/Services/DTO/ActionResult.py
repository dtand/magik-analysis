
VALID_RESULTS = ['POSITION_CLOSED', 'POSITION_OPENED', 'POSITION_ADD', 'PLACE_ORDER', 'MISC']

class ActionResult:

    def __init__(self, result=None, cost_basis=0, size=0, pnl=0):
        self.result = result
        self.cost_basis = cost_basis
        self.size = size
        self.pnl = pnl

    def from_close_position(cost_basis, size, pnl):
        return ActionResult(VALID_RESULTS[0], cost_basis, size, pnl)
    
    def from_open_position(cost_basis, size, pnl):
        return ActionResult(VALID_RESULTS[1], cost_basis, size, pnl)
    
    def from_add_position(cost_basis, size, pnl):
        return ActionResult(VALID_RESULTS[2], cost_basis, size, pnl)
    
    def from_place_order():
        return ActionResult(VALID_RESULTS[3])
    
    def from_misc():
        return ActionResult(VALID_RESULTS[4])

        