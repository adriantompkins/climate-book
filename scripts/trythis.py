import os

# open the file, make a list of all filenames, close the file
#with open('names.csv') as names_file:
    # use .strip() to remove trailing whitespace and line breaks
 #   names= [line.strip() for line in names_file] 

#for filename in os.listdir('path'):
 #   for name in names:
  #      for i, years in enumerate(range(2003,2020)):
        # no need for re.search, just use the "in" operator
   #     if name in filename:
             # move the file
     #        os.rename(os.path.join('path', filename), '/path/to/somewhere/else')
    #         break
    
import os
for i, years in enumerate(range(2003,204)):
    for filename in os.listdir(directory):
        if filename.startswith(*i*): 
          print(os.path.join(directory, filename))
            continue
        else:
            continue
