


#






#### TODO research
1. What is an optimal betting strategy if you have a 3SD move and the next is a 3SD move?

2. If you have a 3sd move, after getting information from the next candel what should you do to exit and enter

3. What are the fractal dynamic of 1min candles after a 5min 3sd> move. How can you use that info to optimize you exit strategies?

4. Open and close VS high and low z-score

5. Probably the best thing I could do is make distrobutions based of the data I collected, the do live monteo carlo simulations during like trading time to see if that would be a high probability trade?
I actually love this idea.

6. The histograms for profit do not make any sense. A 3 sd move and profit from an event at 8am will be hugely different than a 3sd move at 7pm. I either have to normalize it or just hyper focus on a specific time zones. I think the hyper focus on specific time zones make the most sense. Also maybe look into normalizing the data based on z-score, or usualy range.

7. Using monte carlo simulation after I am in a trade, creating the simulation(because I am on long time frames) is very possible and coule lead to intresting results. Think of it this way. I could have an EV, but re-create another EV using monte carlo simulation, using a proper distrboution model (Cauchy or something more fat tailed). Also I could get decently advance and 

8. Look at the rate of change of volatility. Also add a magnitutde(volume) aspect along with it.

9. I would be curious to see what a classifier(supervised and unsupervised) would do on the fractal of a 3SD move inside a large time frame. For example say you got a 3d sd move on the 1hr on the first hour of a 4hour larger time frame. I am sure there is generally patterns there. I would be curious how many of those patterns a classifier would use and what it would do with that.