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
    #l = result.split(']')
    #puts result
    #@x = l[l.length-2]
    # l = l.split('[')
    # @output = '[' + l[l.length-1] + ']'
    #@output = YAML.load(result)
    #@model = @output[0]
    # @confidence = @output[1]
    # @result = @output[2]   
  end
end
