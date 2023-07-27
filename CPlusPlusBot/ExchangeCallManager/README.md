


1. So this must limit exchange calls on the minute and hour basis.

2. Eventually it will need to throttle the important of exchange calls. Meaning I might be in a mean reversion trade and to ping the exchange for the currency that I am in on, on a more regular basis to manage risk.

3. This must work for multiple exchanges.

4. I am noticing that, generally speaking, the exchange manager may need to send information to the the trade manager, but the trade manager may send information back to the exchange information to priortize information.


5. Each exchange manager will have 
    a. Market data calls
    b. Limit order calls
    c. Market order calls
    d. Orderbook? (This may come later)


So it seems like not a bad place for inferface here.
ALso it seems like a good place to have a manager for all the managers.

But a single manager must
1. keep track of all api calls within a time period.
2. Priotize calls.
3. Have its own logic to maintain API calling strategy.

