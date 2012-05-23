import pickle
import os
import subprocess

datatotal = 0
utotal = 0
mtotal = 0
uhash = {} # uid to unique 0 ... n
mhash = {} # mid to unique 0 ... n
uhash_reverse = {}
mhash_reverse = {}

path = r'/Users/daniel/emelody/mysite/learning/'

f = open(os.path.join(path, 'ratings.txt'), 'r')
g = open(os.path.join(path, 'ratings_transformed.txt'), 'w')
for line in f:
  (uid, mid, rate) = line.strip().split(" ")
  datatotal += 1
  if uid not in uhash:
    uhash[uid] = utotal
    uhash_reverse[utotal] = uid
    utotal += 1
  if mid not in mhash:
    mhash[mid] = mtotal
    mhash_reverse[mtotal] = mid
    mtotal += 1
  g.write(str(uhash[uid]) + " " + str(mhash[mid]) + " " + rate + "\n")
f.close()
g.close()

d = open(os.path.join(path, 'decompose.c'), 'r')
d_new = open(os.path.join(path, 'decompose_transformed.c'), 'w')
for line in d:
  if "const int datatotal" in line:
    d_new.write(line.strip() + " = " + str(datatotal) + ";\n")
  elif "const int utotal" in line:
    d_new.write(line.strip() + " = " + str(utotal) + ";\n")
  elif "const int mtotal" in line:
    d_new.write(line.strip() + " = " + str(mtotal) + ";\n")
  else:
    d_new.write(line)
d.close()
d_new.close()

subprocess.call(['g++', os.path.join(path, 'decompose_transformed.c'), '-o', os.path.join(path, 'decompose')])
subprocess.call(os.path.join('.', path, 'decompose'))

p = open(os.path.join(path, 'predicted_ratings_transformed.txt'), 'r')
p_new = open(os.path.join(path, 'predicted_ratings.txt'), 'w')
for line in p:
  line_arr = line.strip().split(" ")
  p_new.write(str(uhash_reverse[int(line_arr[0])]) + " " + str(mhash_reverse[int(line_arr[1])]) + " " + line_arr[2] + "\n")
p.close()
p_new.close()

u = open(os.path.join(path, 'u_similarity_transformed.txt'), 'r')
u_new = open(os.path.join(path, 'u_similarity.txt'), 'w')
for line in u:
  line_arr = line.strip().split(" ")
  u_new.write(str(uhash_reverse[int(line_arr[0])]) + " " + str(uhash_reverse[int(line_arr[1])]) + " " + line_arr[2] + "\n")
u.close()
u_new.close()

m = open(os.path.join(path, 'm_similarity_transformed.txt'), 'r')
m_new = open(os.path.join(path, 'm_similarity.txt'), 'w')
for line in m:
  line_arr = line.strip().split(" ")
  m_new.write(str(mhash_reverse[int(line_arr[0])]) + " " + str(mhash_reverse[int(line_arr[1])]) + " " + line_arr[2] + "\n")
m.close()
m_new.close()

# subprocess.call(['rm', 'ratings_transformed.txt'])
# subprocess.call(['rm', 'predicted_ratings_transformed.txt'])
# subprocess.call(['rm', 'decompose_transformed.c'])
# subprocess.call(['rm', 'u_similarity_transformed.txt'])
# subprocess.call(['rm', 'm_similarity_transformed.txt'])
