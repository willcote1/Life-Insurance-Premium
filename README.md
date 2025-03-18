# Life-Insurance-Premium

to use: https://life-insurance-premium-9.onrender.com/ (note: free domain makes the load time ~50 seconds sometimes)

This is a calculator for life insurance premiums based on user demographics.

**Project Overview:**

The code leverages actuarial and survival analysis techniques to personalize life insurance pricing.

1. **Data Integration:**  
   The code uses real-world data—demographic, health, and lifestyle information (stored in a JSON file and imported into an SQLite database).

2. **Predictive Modeling with Survival Analysis:**  
   I implemented a Weibull Accelerated Failure Time (AFT) model to predict an individual’s age of death. This survival model considers multiple risk factors such as weight, blood pressure, cholesterol, medication use, and lifestyle indicators, providing an estimate of life expectancy.

3. **Premium Calculation:**  
   The predicted age of death is then used to determine the remaining lifetime (i.e., the years left from current age until expected death). Using this information, it calculates a base premium that reflects the cost of insuring an individual over that period. For term life policies, the user specifies a desired coverage term, and the premium is adjusted accordingly. For whole life policies, a fixed multiplier is applied.
