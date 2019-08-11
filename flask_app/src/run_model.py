import pickle

def run_model(df_data):
    # loading model.pkl and returning prediction
    model = pickle.load(open("trained_models/model.pkl","rb"))
    result = model.predict(df_data)
    return result[0]

def recommendation(price, df):
    
    recommend_price= run_model(df)
    recommend_price=int(round(recommend_price))

    #price delta: recommended prict - original posting price
    delta_price=recommend_price-int(price)

    #URL of Craigslist page diplaying carlist in recommended price range
    rp_low=recommend_price//100*100
    rp_high=rp_low+100
    rec_search='https://sfbay.craigslist.org/search/cta?min_price={rp_low}&max_price={rp_high}'.format(rp_low=rp_low, rp_high=rp_high)

    return recommend_price, delta_price, rec_search