class TradingAccount:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance
        self.is_active = True

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False


class RiskManagement:
    def assess_portfolio_risk(self):
        return "Medium"

    def calculate_position_size(self, symbol, capital):
        return int(capital / 2)  # Simplified logic


class AnalyticsEngine:
    def analyze_market_trend(self, symbol):
        return {
            "symbol": symbol,
            "trend": "upward",
            "confidence": "high"
        }


class NotificationSystem:
    def __init__(self):
        self.alerts = []

    def set_price_alert(self, symbol, price, condition):
        alert = {"symbol": symbol, "price": price, "condition": condition}
        self.alerts.append(alert)
        return alert

    def get_pending_notifications(self):
        return self.alerts


class StockTrader(TradingAccount, RiskManagement, AnalyticsEngine):
    def __init__(self, account_id, name, balance):
        TradingAccount.__init__(self, account_id, balance)
        self.name = name
        self.type = "StockTrader"


class CryptoTrader(TradingAccount, RiskManagement, NotificationSystem):
    def __init__(self, account_id, name, balance):
        TradingAccount.__init__(self, account_id, balance)
        NotificationSystem.__init__(self)
        self.name = name
        self.type = "CryptoTrader"


class ProfessionalTrader(StockTrader, CryptoTrader):
    def __init__(self, account_id, name, balance):
        StockTrader.__init__(self, account_id, name, balance)
        NotificationSystem.__init__(self)
        self.name = name
        self.type = "ProfessionalTrader"

    def execute_diversified_strategy(self, strategy):
        result = {"status": "executed", "positions": []}
        for symbol, details in strategy.items():
            allocation = details.get("allocation", 0)
            capital = allocation * self.balance
            size = self.calculate_position_size(symbol, capital)
            result["positions"].append({
                "symbol": symbol,
                "allocation": allocation,
                "capital": capital,
                "size": size
            })
        return result


# Test Case 1
stock_trader = StockTrader("ST001", "John Doe", 50000.0)
crypto_trader = CryptoTrader("CT001", "Jane Smith", 25000.0)
pro_trader = ProfessionalTrader("PT001", "Mike Johnson", 100000.0)

mro_names = [cls.__name__ for cls in ProfessionalTrader.__mro__]
assert "ProfessionalTrader" in mro_names
assert "StockTrader" in mro_names
assert "CryptoTrader" in mro_names

# Test Case 2
assert stock_trader.account_id == "ST001"
assert stock_trader.balance == 50000.0

deposit_result = stock_trader.deposit(10000)
assert deposit_result == True
assert stock_trader.balance == 60000.0

withdrawal_result = stock_trader.withdraw(5000)
assert withdrawal_result == True
assert stock_trader.balance == 55000.0

# Test Case 3
risk_level = stock_trader.assess_portfolio_risk()
assert risk_level in ["Low", "Medium", "High"]

position_size = stock_trader.calculate_position_size("AAPL", 150.0)
assert isinstance(position_size, int)
assert position_size >= 0

# Test Case 4
market_data = stock_trader.analyze_market_trend("AAPL")
assert isinstance(market_data, dict)
assert "trend" in market_data
assert "confidence" in market_data

# Test Case 5
alert_set = crypto_trader.set_price_alert("BTC", 45000, "above")
assert alert_set["symbol"] == "BTC"

notifications = crypto_trader.get_pending_notifications()
assert isinstance(notifications, list)

# Test Case 6
assert hasattr(pro_trader, "assess_portfolio_risk")    # RiskManagement
assert hasattr(pro_trader, "analyze_market_trend")     # AnalyticsEngine
assert hasattr(pro_trader, "set_price_alert")          # NotificationSystem

# Test Case 7
strategy_result = pro_trader.execute_diversified_strategy({
    "AAPL": {"allocation": 0.7},
    "Crypto": {"allocation": 0.3}
})
assert strategy_result["status"] == "executed"
assert len(strategy_result["positions"]) > 0

print("✅ All tests passed!")