



Things I need to do for backtesting atm 
     1. Create a stats output at the end
     2. Make an iterative proccess to get optimized values
     3. The optimization for different values will come in multiple parts 
     4.  
     5. 


BackLog 
1. Make sure the times are correct, pandas/vs live vs estTime converter
2. A system to optimize went to enter a trade
3. A system to put more trades on once in on a trade
4. A system to help exit trades/limit order style
5. Make sure the indexes are the same for back testing, so I iterate on the same index
6. Rename functions, so that the function 
     keys are the same name as the function 
     except the name of the 
     strategy is at the nd
7. Use the incomplete data to your advantage
8. Make a better debug print
     A. Each function has a debug section
     B. Logs file
9. Get everything working on a pandas note book so building each component is easer
10. 


   
            # So I am just decciding to trade based on 
            # This overly simple signal
            # But I am not easily able to track the price
            # For live trading it doesn't matter because I just making market orders
            # Which will need to change because I need to make a bot that can get cheaper limit orders
            # Also I need to pass the data/like price
            # I think I want to stay away from passing around variables
            # Rather  I think I just want to pass state varibales in the inner statemaps
            # 





#Sunday
1. get optimized values
2. Run the optimized values on test to see if you can run in Monday Morning?
3. Maybe run it in google colab
4. Think about Risk manager bot?
     I think I might want to restructure everything to run on seperate threads, 
     rather than a while loop
     And they just call each other




# Short term -- This week
0. Check this works, I wrote it while really high
     a. Only do one time frame at a time because trades will cancel themselves if you get a short and negative singal at once
1. Setup the BackTests - that uses the same functions in the same way
2. Optimize parameters as a result of running mutliple  back test results
3. Develop Risk mananger
4. clean ups TODOs
     a. Remove the calls to read JSON from file, only do that once, replace the use of that data 
        When possible
        With list of Times and currencies
5. Cleverly name each folder so they come in the same alphbetical order that they are used
6. Formalize the way that I have currency pair names. 
    a. I think the way I set the currency key for the pandas dict when reading csv
       is different from API calls, which is bad 

7. Basically pass around a json/dictionary 
     from trade in, to trade out, 
     that has a time stamp of the state 
     at each stetp

4. !!!!!!!!!may 9th Tuesday 4pm first time the bot made a trade on itself
5. !!!!!!! XXXXXXXXXXXMake sure it works

# Short term -- Next week

1.  Re run this full time with backtested values
2.  Come up with an improved strategy
     A. I want a strategy that uses the DOM, but I am have no idea how to use that properly
     B. I also like the idea of using multiple exchanges and looking for all risk on events or 
     all risk off events
     C. I am sure I can improve this stratgey 
     by adding in some type of case where 
     15min.30min,1hr are all singalling green 
     which leads to a slight higher probability trade on
     X time frame trades
     D. 
3.  Re work the code so that, 
    data collections happens first, 
    then making that data fit each strategy first
     A. This might be a long and hard to think about
     B. Realize that if each strategy might use different data sources
     C. Also shit is fucked up because if I am using ONada data source,
          I should be only calling it once a minute or something
          But if run 10 strageies I could eat up all those resources to do so
          So I need to Create a data collection section
          Then pass that on to all the bots?
     D.  A shit ton of more thought needs to be involved here
          REally there needs to be timers for each data source
          Then once the timers end, they ping the strategy
          So the data source actually drives the action
          Instead of a for loop, the just goes in a circle.
          I like that a lot more.




# Mid-term TODO May 25th
1.Post code on github 
     a. Remove all BeaerTokens
     b. 
2. Add better logging, log file for living trading mode
3. Go through and spend a day or weekend working on taking care of all the TODOs
4. Update so each code section has its own log print outs



# Long term TODO before June 15th
1. 


# Long term TODO before July
1. Start adding multi assets
