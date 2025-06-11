CONTRACT_SIZES = {
    '6B.FUT': 6250
}

def find_size_for_contract(contract):
    if contract not in CONTRACT_SIZES:
        return 1
    return CONTRACT_SIZES[contract]