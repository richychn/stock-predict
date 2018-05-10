require 'yaml'

class PredictController < ApplicationController
  def new
  	#nothing to do 
  end

  def learn
  	@input = params[:ticker]
    @result = %x[ipython python_test.py #{@input}][0..5]
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
