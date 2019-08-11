import flask
from flask import Flask, render_template, request
from src.data_preproc import make_simple, df_stand, get_dummy, model_readable, content_extract, chain_reaction
from src.run_model import run_model, recommendation

#create instance
app=Flask(__name__)

#flask! run index!
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/price',methods = ['POST'])
def price():
    if request.method == 'POST':

        #getting URL as a string
        posturl = request.form['posturl']
        
        #extrating the informations from URL posting
        title, _, price, _, carinfo_df, df_data = chain_reaction(posturl)

        #running model, returns recommendation
        recommend_price, delta_price, rec_search = recommendation(price, df_data)
  
        return render_template("price.html",posturl=posturl, delta_price=delta_price, rec_search=rec_search, post_title=title, post_price=price, recommend_price=recommend_price, carinfo_table=carinfo_df)

if __name__ == '__main__':
    app.run(port=5000, debug=True)