
#require 'json'
require 'yaml'
result = %x[ipython alltogether.py AMZN]
#result = "[0.50495049504950495, 1]"
#result = YAML.load(result)
#result = JSON.parse result 
l = result.split(']')
l = l[l.length-2]
l = l.split('[')
output = '[' + l[l.length-1] + ']'
output = YAML.load(output)
puts output
# arr = l[0] + ']'
# result = YAML.load(arr)
# puts result[1]
#length = result.length
#puts result[(length/4)..length]
#puts result[0]
