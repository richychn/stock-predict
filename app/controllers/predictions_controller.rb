require 'yaml'

class PredictionsController < ApplicationController
  before_action :article_id, only: [ :show, :destroy ]

  def index
    @predictions = Prediction.all
  end 
  
  def new
    @prediction = Prediction.new
  end

  def create
  	@ticker = params[:ticker]
    result = %x[ipython alltogether.py #{@ticker}]#[0..5]
    arr = result.split("\n")
    arr = arr[arr.length-2]
    byebug 
    @output = YAML.load(l)
    @model = @output[0]
    @confidence = @output[1].to_f
    @result = @output[2].to_i   
    @prediction = Prediction.new(ticker: @ticker, model: @model, confidence: @confidence, result: @result)

    @prediction.save
    redirect_to prediction_path(@prediction)
  end

  def show
    @output = output(p)

  end  

  def destroy 
    @prediction.destroy
    redirect_to prediction_path
  end 

  private 

  def prediction_id 
    @prediction = Prediction.find(params[:id])
  end 

  def output(p)
    ticker_ = p.ticker 
    model_ = p.model
    confidence_ = p.confidence * 100
    result_ = p.result

    if (result_ == 1)
        return "YA! With the" + output[0] + ", we are " + confidence.to_s + " percent confident that the stock price for " + ticker + " will increase by 10 percent or more next year"
    elsif (result_ == 0)
        return "YA! With the" + output[0] + ", we are " + confidence.to_s + " percent confident that the stock price for " + ticker + " will stay relatively the same next year"
    else
        return "YA! With the" + output[0] + ", we are " + confidence.to_s + " percent confident that the stock price for " + ticker + " will decrease by 10 percent or more next year"
    end 
  end

end
