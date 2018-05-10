require 'yaml'

class PredictionsController < ApplicationController
  before_action :prediction_id, only: [ :show, :destroy ]

  def index
    @predictions = Prediction.all
  end 
  
  def new
    @prediction = Prediction.new
  end

  def create
  	@ticker = params[:ticker]
    if (Prediction.exists?(ticker: @ticker))
      redirect_to error_path_url
    else
      result = %x[ipython alltogether.py #{@ticker}]
      arr = result.split("\n")
      arr = arr[arr.length-2]
      if (arr[0] == "[" and arr[arr.length-1] == "]")
       # byebug
        @output = YAML.load(arr)
        @model = @output[0]
        @confidence = @output[1].to_f
        @result = @output[2]  
        @prediction = Prediction.new(ticker: @ticker, model: @model, confidence: @confidence, result: @result)
        @prediction.save
        redirect_to prediction_path(@prediction)
      else
        redirect_to error_path_url
      end
    end
  end

  def show
    #@output = output(@prediction.id)
    ticker_ = @prediction.ticker 
    model_ = @prediction.model
    confidence_ = @prediction.confidence * 100
    result_ = @prediction.result

    if (result_ == 1)
        @print = "YA! Using the " + model_ + ", we are " + confidence_.to_s + " percent confident that the stock price for " + ticker_ + " will increase by 10 percent or more next year"
    elsif (result_ == 0)
        @print =  "YA! Using the " + model_ + ", we are " + confidence_.to_s + " percent confident that the stock price for " + ticker_ + " will stay relatively the same next year"
    else
        @print = "YA! Using the " + model_ + ", we are " + confidence_.to_s + " percent confident that the stock price for " + ticker_ + " will decrease by 10 percent or more next year"
    end 

  end  

  def destroy 
    @prediction.destroy
    redirect_to predictions_path
  end 

  def error 
    @error_message = "Error could be: 1. Company predicted before 2. Ticker invalid 3. Ticker not found. Please try again"
  end


  private 

  def prediction_id 
    @prediction = Prediction.find(params[:id])
  end 
end
