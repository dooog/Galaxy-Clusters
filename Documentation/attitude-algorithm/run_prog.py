#!/usr/bin/env python
from random import uniform
from quat import quat
from math import pi
from rot_test import random_quat
import test_gen as tgen
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys


if __name__ == "__main__":	
  try: vec_test= int(sys.argv[1])
  except: vec_test = 1000
  
  print "Generating ",vec_test, " Test Vectors" 
  test_vectors = np.array(tgen.vector_cluster_gen(100,1))
  print test_vectors

  print "Generating a random quaternion"
  q = random_quat()


  	
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d') 
  
  
  ax.ylim((-1,1))
  ax.xlim((-1,1))
  ax.zlim((-1,1))
  
  vxs,vys,vzs = np.transpose(test_vectors)
  ax.scatter(vxs, vys, vzs, c='b', marker='^')
  
  uxs,uys,uzs = np.transpose(map(lambda v : q.rot(v) , test_vectors))
  ax.scatter(uxs,uys,uzs, c='r', marker='o')  
  

  
  ax.set_xlabel('X Label')
  ax.set_ylabel('Y Label')
  ax.set_zlabel('Z Label')

  plt.show()
