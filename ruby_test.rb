
#require 'json'
require 'yaml'
result = %x[ipython alltogether.py AMZN]
#result = "[0.50495049504950495, 1]"
#result = YAML.load(result)
#result = JSON.parse result 
#l = result.split('[')
#puts '[' + l[l.length-1]
#puts result[0]
puts result[result.length]