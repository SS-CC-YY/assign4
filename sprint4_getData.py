import csv
import errno
import os

def readParams(inFile = ""):
#https://stackoverflow.com/questions/19579997/how-to-catch-empty-user-input-using-a-try-and-except-in-python
  try:
    name = open(inFile, mode="r", encoding="utf8")
    if not name:
      raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), name)
    else:
      with name as f:
        reader = csv.reader(f)
        header = next(reader)
        params = next(reader)
        #print(line)
        return (header, params) 
  except FileNotFoundError as e:
    print(e)


def getData(fn = ""):
  ##############################################################################
  # get data
  name = "amazon_co-ecommerce_sample.csv"

  #print(name)

  l = []
  category = []

  with open(name, encoding="utf8") as f:
    reader = csv.reader(f)
    # get the column names
    category = next(reader)
    for row in reader: 
      l.append(row)
  f.close()

  ##############################################################################
  # construct the 2d array
  rows, cols = (len(l)+1, len(category)+1) 
  db = []
  for r in range(len(category)):
    col = []
    for c in range(len(l)):#col
      col.append(l[c][r])
    db.append(col)

  ##############################################################################
  #return the header list and db
  return db