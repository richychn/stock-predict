require 'yaml'

class PredictController < ApplicationController
  def new
  	#nothing to do 
    @ticker = ""
  end

  def learn
  	@ticker = params[:ticker]
    #@test = "hello"
    result = %x[ipython alltogether.py #{@ticker}]#[0..5]
    l = result.split("\n")
    #puts result
    l = l[l.length-2]
    @output = YAML.load(l)
    @model = @output[0]
    @confidence = @output[1]
    @result = @output[2]   
  end
end
