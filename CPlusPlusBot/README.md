1. This weekend I would like to get something functioning in the correct format

Wow so there is still a lot of work to do.

- Get the strategy manager to read its files and hold them in memeory for now.

- Get the data manager to send its own information to a strategy manager
    -- Note I think I need to update that with a single thread execution or?
    --Actually I can keep it the way I have it, but just send that off on a thread.
    --The return type doesn't matter to the excange excution manager

- get the strategy manager to send its information over to trade manager 
- Then make a trade based off of that
- Then implement the exit strategy part once all that is done.


b. I am realizing its really important that I touch this project, specifically code some lines of c++ everyday or I just lose what I learnt.

### Work in progress
still in more of design phase, but just beginning to implement.


### Note to self

Part 1.
The first iteration I want to make of this.
1. looks for 3 > sd moves on each specifc time frame (5,30,1hr, 4hr, day)
2. Does the opposite of the move
3. Searches this for forex, crypto, stocks.
4. This means I have to have my mean, map look up table calculatd at start or create the table and read it in to memory from file instead of recreating it(this really isn'
t important)
5. The looking for high sd moves, will take tinker with exchanges to figure out when they best display this.
6. Also I need to find/optimize the exit strategies, stop losses and take profit
7. Add a Markov chain like calculation to decide when to exit
8. figuring out how often to ping the server when I need to check for exit points. 


Part 2. Add in trending following strategy.


### To Run
` g++ -std=c++17 main.cpp TradeManager/OandaManager.cpp ExchangeCalls/APIcalls.cpp DataCleaner/JSONhelpers.cpp DataCleaner/json.hpp -lcurl -pthread  -o my_program;`


<img src="FLowAsOfNow.png"/>


### possible renaming, refactoring 
Thre more I work on a project, the more I have a clear understanding layout.

1. Change Trade Manager to TradeAndRiskManager.
