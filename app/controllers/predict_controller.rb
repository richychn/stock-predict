require 'yaml'
class PredictController < ApplicationController
  def new
  	#nothing to do 
  end

  def learn
  	@input = params[:ticker]
    result = %x[ipython app/assets/backend/alltogether.py #{@input}]
    l = result.split(']')
    l = l[l.length-2]
    l = l.split('[')
    @output = '[' + l[l.length-1] + ']'
    @output = YAML.load(@output)
    @model = @output[0]
    @confidence = @output[1]
    @result = @output[2]   
  end
end
