
#require 'json'
require 'yaml'
result = %x[ipython alltogether.py AAPL]
#result = "[0.50495049504950495, 1]"
#result = YAML.load(result)
#result = JSON.parse result 
l = result.split(']')
l = l[l.length-2]
l = l.split('[')
output = '[' + l[l.length-1] + ']'
output = YAML.load(output)
confidence = (output[1] * 100).to_i
if (output[2] == 1)
    puts "The best model is" + output[0] + "with confidence score" + confidence.to_s + "% that stock price will increase by 10% next year"
elsif (output[2] == 0)
    puts "The best model is" + output[0] + "with confidence score" + confidence.to_s + "% that stock price will about the same next year"
else
    puts "The best model is" + output[0] + "with confidence score" + confidence.to_s + "% that stock price will lose more than 10% of its value next year"
end 
# arr = l[0] + ']'
# result = YAML.load(arr)
# puts result[1]
#length = result.length
#puts result[(length/4)..length]
#puts result[0]
