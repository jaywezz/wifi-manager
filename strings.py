# initializing string  
test_string = "OA384PTAC8 Confirmed. You have received ksh500.00 from JAMES WAWERU MUHINDI 0797391932 on 4/5/2010 at 4:11 PM New M-PESA balance is Ksh50.00"
array_word = []  
# initializing split word 
spl_word = 'ksh'
  
# printing original string  
print("The original string : " + str(test_string)) 
  
# printing split string  
print("The split string : " + str(spl_word)) 
  
# using partition() 
# Get String after substring occurrence 
res = test_string.partition(spl_word)[2]
array_word.append(res)

if res.split()[5].isnumeric():
    print("my friend this is a phone number")
    amount = res.split()[0]
    sender_name = res.split()[2] + ' ' + res.split()[3] + ' ' + res.split()[4]
    sender_number = res.split()[5]
    date = res.split()[7]
    time = res.split()[9]

else:
    print("contains only two names")
    amount = res.split()[0]
    sender_name = res.split()[2] + ' ' + res.split()[3]
    sender_number = res.split()[4]
    date = res.split()[6]
    time = res.split()[8] 
print (amount)
print (sender_name)
print (sender_number)
print (date)
print (time)

# print result 
print("String after the substring occurrence : " + res) 
