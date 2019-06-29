# How much is this car worth?
-	Price prediction of used car using data base scrapped from Craigslist.
-	Investigate the important features that determines the car price.
-	Providing a guide line of used car price for car buyers and sellers in California.

**Personal motivation:** When I came to the United States, I had to buy a car. I could not buy used car because there were so many things (independent variables affecting the price) to consider. Now, I am planning to build my own criteria for buying used cars and share with others.
**Personal Goal:** Comparing linear regression and gradient boosting.

# Why do we want to predict used car price?
When you are planning to buy a new car, first thing you do is web searching. Gather the information and ‘estimates’ the car price you are willing to buy. Probably your estimated market price of the car is near the mean value of information you collected. In statistical term, you just set your expected value as a mean value from your sample data set. This is a good starting point, but you still need something to improve your estimation. 

Modeling is about improving your method to reach better prediction from the original estimation. Incorporating the modeling in your decision, you might able to save or earn few hundreds to thousand dollars by knowing correctly estimated car values.

# DATA
29 California Craigslist sites: https://geo.craigslist.org/iso/us/ca

**117,047 x 22** (Last Update: 2019-06-27)

Web scrapped by modifying source code used for Kaggle data:
https://www.kaggle.com/austinreese/craigslist-carstrucks-data#craigslistVehiclesFull.csv

List of 29 cities and locations in California:
- bakersfield
- chico
- fresno / madera
- gold country
- hanford-corcoran
- humboldt county
- imperial county
- inland empire - riverside and san bernardino counties
- los angeles
- mendocino county
- merced
- modesto
- monterey bay
- orange county
- palm springs
- redding
- reno / tahoe
- sacramento
- san diego
- san luis obispo
- santa barbara
- santa maria
- SF bay area
- siskiyou county
- stockton
- susanville
- ventura county
- visalia-tulare
- yuba-sutter

columns:
['url', 'city', 'city_url', 'price', 'year', 'manufacturer', 'make',
       'condition', 'cylinders', 'fuel', 'odometer', 'title_status',
       'transmission', 'VIN', 'drive', 'size', 'type', 'paint_color',
       'image_url', 'desc', 'lat', 'long']

