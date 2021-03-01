import csv
import sys
import sprint4_getData
'''
reference help:
https://www.geeksforgeeks.org/python-finding-strings-with-given-substring-in-list/
'''

'''
0 uniq_id
1 product_name
2 manufacturer
3 price
4 number_available_in_stock
5 number_of_reviews
6 number_of_answered_questions
7 average_review_rating
8 amazon_category_and_sub_category
9 customers_who_bought_this_item_also_bought
10 description
11 product_information
12 product_description
13 items_customers_buy_after_viewing_this_item
14 customer_questions_and_answers
15 customer_reviews
16 sellers
'''

################################################################################
# param[0] searches through data[8] for a subcategory (static set to toys)
# param[1] searches through data[8] for main category
# param[2] specifies how many items to return
def byUniqId(param = [], data = []):
  
  uniq_ids = []
  sorted_by_uniq_id = []
  
  for i in range(len(data[0])):
    if (data[8][i].find(param[0]) >= 0) or (data[8][i].find(param[1]) >= 0):
      row = []
      # the first index will be the identifier, then append
      # the columns of data. index 0 is the uniq id
      row.append(data[0][i])
      for j in range(len(data)):
        row.append(data[j][i])
      uniq_ids.append(row)
  #[row][col]#
  #sort the list by uniq_id
  uniq_ids.sort()
  sorted_by_uniq_id = uniq_ids

  ''' 
  #can create files and send them if we want
  #######
  # write 
  with open("uniq_id_output.csv", 'w', newline='') as outfile:
    output = csv.writer(outfile, delimiter=',')
    output.writerow(['input_item_type']+['input_item_category']+['input_number_to_generate']+['output_item_name']+['output_item_rating']+['output_item_num_reviews\n'])
    for row in range(len(sorted_by_uniq_id)):
      for col in range(6):
        s = str(sorted_by_uniq_id[row][2]).encode("utf-8")
        output.writerow([param[0]]+[param[1]]+[param[2]]+[s]+[sorted_by_uniq_id[row][6]])
  '''
  return sorted_by_uniq_id

###############################################################################
# param[0] searches through data[8] for a subcategory (static set to toys)
# param[1] searches through data[8] for main category
# param[2] specifies how many items to return
def byNumOfReviews(param = [], data = []):

  num_reviews = []
  sorted_by_num_reviews = []

  size = len(data[0])
  for i in range(size):
    # 8 is the category type and or subcategory
    if (data[8][i].find(param[0]) >= 0) or (data[8][i].find(param[1]) >= 0):
      row = []
      # the first index will be the identifier, then append
      # the columns of data. index 5 is the number of reviews
      if data[5][i]:
        rev = int(data[5][i])
      row.append(rev)
      for j in range(len(data)):
        row.append(data[j][i])
      num_reviews.append(row)
                                                                                 
  num_reviews.sort(key=None, reverse=True)
  sorted_by_num_reviews = num_reviews

  '''
  #can create files and send them if we want
  #######
  # write 
  with open("number_of_reviews_output.csv", 'w', newline='') as outfile:
    output = csv.writer(outfile, delimiter=',')
    output.writerow(['input_item_type']+['input_item_category']+['input_number_to_generate']+['output_item_name']+['output_item_rating']+['output_item_num_reviews\n'])
    for row in range(len(sorted_by_num_reviews)):
      for col in range(6):
        s = str(sorted_by_num_reviews[row][2]).encode("utf-8")
        output.writerow([param[0]]+[param[1]]+[param[2]]+[s]+[sorted_by_num_reviews[row][6]])
  '''
  return  sorted_by_num_reviews[0:int(10 * param[2])]

###############################################################################
# param[0] searches through data[8] for a subcategory (static set to toys)
# param[1] searches through data[8] for main category
# param[2] specifies how many items to return
# average_reviw_rating / highest to lowest / index 7
def byAvgRevRating(param = [], data = []):

  avg_rev_ratings = []
  sorted_by_avg_rev_rating = []

  size = len(data[0])
  for i in range(size):
    # 8 is the category type and or subcategory
    if (data[8][i].find(param[0]) >= 0) or (data[8][i].find(param[1]) >= 0):
      row = []
      # the first index will be the identifier, then append
      # the columns of data. index 7 is the average reveiw rating 
      if data[7][i]:
        rev = data[7][i]
      row.append(rev[0:3])
      for j in range(len(data)):
        row.append(data[j][i])
      avg_rev_ratings.append(row)
                                                                                 
  avg_rev_ratings.sort(key=None, reverse = True)
  sorted_by_avg_rev_rating = avg_rev_ratings 

  '''
  #can create files and send them if we want
  #######
  # write 
  with open("avg_rev_rating_output.csv", 'w', newline='') as outfile:
    output = csv.writer(outfile, delimiter=',')
    output.writerow(['input_item_type']+['input_item_category']+['input_number_to_generate']+['output_item_name']+['output_item_rating']+['output_item_num_reviews\n'])
    for row in range(len(sorted_by_avg_rev_rating)):
      for col in range(6):
        s = str(sorted_by_avg_rev_rating[row][2]).encode("utf-8")
        output.writerow([param[0]]+[param[1]]+[param[2]]+[s]+[sorted_by_avg_rev_rating[row][6]])
  '''
  return sorted_by_avg_rev_rating[0:int(param[2])]