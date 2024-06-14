# Determining price of asset based on orderbook

-   We need 3 things

1. bids
2. asks
3. history of trades

## Steps to determine price of asset

1. Determine bid ask spread

```python
bid_ask_spread = min(asks) - max(bids)
```

2. Determine mid-price

```python
mid_price = (max(bid)+min(ask))/2
```

3. market price (prototyping) is determined by the most recent transaction's agreed price
4. Weighted average price (VWAP)

```py
def calculate_vwap(tradehistory):
    numerator = 0
    denominator = 0
    for trades in tradehistory:
        numerator += trades.price * trades.volume
        denominator += trades.volume
    return numerator/denominator
```

4. Order matching

-   execution is based on the best available marching order in the order book
-   market buy orders are executed at the lowest ask price
-   market sell orders are executed at the the highest bid price.
