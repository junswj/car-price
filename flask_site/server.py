# Import libraries
import pandas  as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import pickle
import os
import flask
from flask import Flask, render_template, request

#create instance
app=Flask(__name__)

#flask! run index!
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

def make_simple(df,col='model'):
    df[col]=df[col].fillna('null')
    df[col]=df[col].str.lower()
    df[col]=df[col].str.replace('-','')
    df[col]=df[col].str.replace(' ','')
    df[col]=df[col].str.replace('_',' ')
    car_model=['silverado', 'f150', 'civic', 'accord', 'f250', 'camry', 'tacoma', 'corolla', 'wrangler',
              'sierra', 'prius', 'f350', 'altima', 'mustang', 'cherokee', 'x5', 'x3', 'tundra', 'fusion', 'focus',
               'tahoe', 'jetta', 'yukon', 'crv', 'explorer', 'sentra', 'cooper', 'escape', 'sienna', '328i', 'sonata',
               'rav4', 'odyssey', 'elantra', 'outback', 'suburban', 'a4', '4runner', 'camaro', 'cruze', 'e350', 
               'highlander', 'rogue', '3series', 'escalade', 'charger', 'impala', 'ranger', 'pilot', 'malibu',
               'challenger', 'forester', 'impreza', 'expedition', 'genesis','gti','cclass', 'corvette', 'frontier', 'colorado',
                'passat', 'mdx', 'optima', 'versa', 'sprinter', 'equinox', 'is250', 'is350','edge', 'grand caravan', 'eclass',
               'santafe', 'mazda3', 'durango', 'tsx', '5series','7series' 'f550', 'xc90', 'q5','soul', 'cruiser','wrx','golf', 'sorento', 
               'traverse', 'acadia', 'pathfinder', 'beetle', 'xterra', '1500', '2500', '3500']
    for i in car_model:
        df[col][df[col].str.contains(i)]=i
    df[col][df[col].apply(lambda x: x not in car_model)]='null'
    try:
        df.drop(columns=['VIN'], inplace=True)
    except:
        pass
    
    return df

def df_stand(df,year):
    df['year'] = (2020-year)/40
    df['mileage'] = df['odometer'].apply(lambda x : (int(x)-93453)/104729)
    df.drop(columns=['odometer'], inplace=True)
    return df

def get_dummy(df):
    dummy_col=df.select_dtypes('object').columns
    new_df=pd.get_dummies(df, columns=dummy_col, dummy_na=True,prefix=dummy_col)
    return new_df

def content_extract(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.content, "html")
    
    title=soup.title.text.strip()
    year=int(title[:4])
    
    
    title_txt=soup.find("span", {"class": "postingtitletext"})
    price=title_txt.find_all("span")
    price=price[1].text.strip()
    price=int(price.replace('$',''))
    
    image_data = soup.find("div", {"class": "slide first visible"})
    image=image_data.find_all("img")
    image_url=str(image[0]).split()[2].replace('src="', "").replace('"',"")
    
    spec_div = soup.find("div", {"class": "mapAndAttrs"})
    spec_row=spec_div.find_all("span")
    spec_raw=[str(i) for i in spec_row]
    if len(spec_raw)>12:
        spec_raw=spec_raw[:12]
    
    spec_list=[i.replace('<span>', '').replace('</span>', '').replace('<b>', '').replace('</b>', '') for i in spec_raw]
    spec_list[0]='model: '+spec_list[0]
    spec_coord=[i.split(': ') for i in spec_list]
    
    display_dict={}
    for i,k in spec_coord:
        display_dict[i]=[k]
    display_df=pd.DataFrame.from_dict(display_dict).T 
    display_df.columns=['Posting Information']   
    
    spec_dict={}
    for i,k in spec_coord:
        spec_dict[i.replace(' ','_')]=[k.replace(' ','_')]
    raw_df=pd.DataFrame.from_dict(spec_dict)
    
    return title, year, price, image_url, display_df, raw_df

def model_readable(df,year):
    df=make_simple(df)
    df=df_stand(df,year)
    df=get_dummy(df)
    
    features=['year', 'mileage', 'model_1500', 'model_2500', 'model_328i', 'model_3500', 'model_3series',
          'model_4runner', 'model_5series', 'model_a4', 'model_acadia', 'model_accord', 'model_altima',
          'model_beetle', 'model_camaro', 'model_camry', 'model_cclass', 'model_challenger', 'model_charger',
           'model_cherokee', 'model_civic', 'model_colorado', 'model_cooper', 'model_corolla', 'model_corvette',
           'model_cruiser', 'model_cruze', 'model_crv', 'model_durango', 'model_e350', 'model_eclass',
           'model_edge', 'model_elantra', 'model_equinox', 'model_escalade', 'model_escape', 'model_expedition',
           'model_explorer', 'model_f150', 'model_f250', 'model_f350', 'model_focus', 'model_forester',
           'model_frontier', 'model_fusion', 'model_genesis', 'model_golf', 'model_gti', 'model_highlander',
           'model_impala', 'model_impreza', 'model_is250', 'model_is350', 'model_jetta', 'model_malibu',
           'model_mazda3', 'model_mdx', 'model_mustang', 'model_null', 'model_odyssey', 'model_optima',
           'model_outback', 'model_passat', 'model_pathfinder', 'model_pilot', 'model_prius', 'model_q5',
           'model_ranger', 'model_rav4', 'model_rogue', 'model_santafe', 'model_sentra', 'model_sienna',
           'model_sierra', 'model_silverado', 'model_sonata', 'model_sorento', 'model_soul', 'model_sprinter',
           'model_suburban', 'model_tacoma', 'model_tahoe', 'model_traverse', 'model_tsx', 'model_tundra',
           'model_versa', 'model_wrangler', 'model_wrx', 'model_x3', 'model_x5', 'model_xc90', 'model_xterra',
           'model_yukon', 'model_nan', 'condition_excellent', 'condition_fair', 'condition_good', 'condition_like new',
           'condition_new', 'condition_salvage', 'condition_nan', 'cylinders_10_cylinders', 'cylinders_12_cylinders',
          'cylinders_3_cylinders', 'cylinders_4_cylinders', 'cylinders_5_cylinders', 'cylinders_6_cylinders',
           'cylinders_8_cylinders', 'cylinders_other', 'cylinders_nan', 'fuel_diesel', 'fuel_electric', 'fuel_gas', 'fuel_hybrid',
           'fuel_other', 'fuel_nan', 'title_status_clean', 'title_status_lien', 'title_status_missing', 'title_status_parts only',
           'title_status_rebuilt', 'title_status_salvage', 'title_status_nan', 'transmission_automatic', 'transmission_manual',
           'transmission_other', 'transmission_nan', 'drive_4wd', 'drive_fwd', 'drive_rwd', 'drive_nan', 'size_compact',
           'size_full-size', 'size_mid-size', 'size_sub-compact', 'size_nan', 'type_SUV', 'type_bus', 'type_convertible',
           'type_coupe', 'type_hatchback', 'type_mini-van', 'type_offroad', 'type_other', 'type_pickup',
           'type_sedan', 'type_truck', 'type_van', 'type_wagon', 'type_nan', 'paint_color_black', 'paint_color_blue',
           'paint_color_brown', 'paint_color_custom', 'paint_color_green', 'paint_color_grey', 'paint_color_orange',
           'paint_color_purple', 'paint_color_red', 'paint_color_silver', 'paint_color_white', 'paint_color_yellow',
           'paint_color_nan']
    
    data_array=np.zeros(len(features))
    df_data=pd.DataFrame(data_array.reshape(1,-1), columns=features)
    for i in df:
        if df[i][0]!=0:
            df_data[i]=df[i][0]
    
    return df_data

def chain_reaction(url):
    title, year, price, image_url, display_df, raw_df = content_extract(url)
    df_data=model_readable(raw_df, year)

    carinfo_df=[display_df.to_html(classes='data', header="True")]

    return title, year, price, image_url, carinfo_df, df_data   




def run_model(df_data):
   
    model = pickle.load(open("model.pkl","rb"))
    result = model.predict(df_data)
    return result[0]

@app.route('/price',methods = ['POST'])
def price():
    if request.method == 'POST':
        # to_predict_list = request.form.to_dict()
        # to_predict_list=list(to_predict_list.values())
        # to_predict_list = list(map(int, to_predict_list))

        posturl = request.form['posturl']
        #title, year, price, image_url, carinfo_df, df_data = chain_reaction(url)

        title, _, price, _, carinfo_df, df_data = chain_reaction(posturl)

        recommend_price= run_model(df_data)
        recommend_price=int(round(recommend_price))
        rp_low=recommend_price//100*100
        rp_high=rp_low+100
        rec_search='https://sfbay.craigslist.org/search/cta?min_price={rp_low}&max_price={rp_high}'.format(rp_low=rp_low, rp_high=rp_high)
  
        return render_template("price.html", rec_search=rec_search, post_title=title, post_price=price, recommend_price=recommend_price, carinfo_table=carinfo_df)

if __name__ == '__main__':
    app.run(port=5000, debug=True)