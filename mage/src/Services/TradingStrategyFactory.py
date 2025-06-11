import json
from mage.src.Strategies.DTO.TradingStrategy import TradingStrategy

class TradingStrategyFactory:

    def from_json(filepath):

        with open(filepath, 'r') as file:
            data = json.load(file)

        return TradingStrategy.from_json(data)


        
