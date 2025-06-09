## zone perspective


4.  Zone is measured by a combination of the AO and AC.  Possibilities are sell zone(red), gray zone (do nothing) and buy zone(green).  we can say everything is going away. Momentum is in the same direction as our trade and the momentum is accelerating in our direction. Also the price is closing in our direction. This forms zone for the two possible direction, selling or buying.
Here is a summary of the technical indicators mapped to each of the 5 dimensions from the New Trading Dimension (NTD) framework from B. Williams, based on the available content:

1. The Fractal (Phase Space):
   - Pattern recognition tools like candlestick patterns, reversal/continuation patterns, trendlines, Fibonacci retracements

2. Momentum (Phase Energy):  
   - Awesome Oscillator (AO) 

3. Acceleration/Deceleration (Phase Force):
   - AC indicator (measures speed of momentum) 

4. Zone (Phase Energy/Force Combination):
   - Defined by combining signals from AO and AC  
   - Sell zone (AO and AC in downtrend), gray zone (AO and AC neutral), buy zone (AO and AC in uptrend)
   - Optimal Zone occurs when:
      - Momentum is in trade direction   
      - Momentum acceleration confirms direction
      - Price closes in trade direction

5. Balance Line (Strange Attractors):  
   - Alligator (or any triple moving average) indicator

This summarizes the technical factors quantifying each dimension based on the discussion so far. Please advise if any part of the summary could be improved or expanded on further. The goal is to develop a practical framework for applying the multidimensional NTD perspectives in technical analysis.


##  "Initiating fractal" entry signal

 "Initiating fractal" entry signal concept within Dimension 1. Capturing signals like this that integrate multiple dimensions will be key to developing a robust approach. Here are some suggestions for how we could represent this "Initiating fractal" signal:

For Dimension 1 feature engineering:
- Extract price fractals that satisfy the validation rules like being outside the red line for 5+ bars 
- Label these as candidate "Initiating fractals"

For the overall feature space:  
- Create binary feature that fires when a new fractal breaks past a opposite direction fractal, as the order entry criteria
- Include price level and direction of both fractals 
- Engineer features representing the relationship between fractals and Balance Line states

This better ties the pattern recognition of Dimension 1 to the structural tendencies sought in Dimension 5. Representing the conditions and implications of this signal will help evaluate its efficacy over time.



from : http://simp.ly/p/t8qSvQ


----
----

