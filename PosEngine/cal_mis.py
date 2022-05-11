import numpy as np

standard_distance_camera  = 0.12#米
standard_distance_horizontal = 672
standard_distance_depth = standard_distance_horizontal/2/np.sqrt(3)
standard_distance_vertical = 376
standard_ver_d_depth = 10/10

x1_list = [409,
      374.5,
      316,
      295.5,
      403,
      339.2564087,
      502,
      523.5,
      366.5,
      308.1428528,
      272,
      386.5,
      ]
y1_list = [212.50,
243.50,
214.00,
161.00,
168.00,
162.94,
164.00,
229.50,
280.00,
241.00,
156.50,
14.00,
]
x2_list = [248.68,
232.23,
180.50,
154.00,
234.50,
194.50,
314.50,
334.00,
222.50,
173.00,
134.50,
219.50,
]
y2_list=[213.05,
243.77,
213.50,
161.00,
167.50,
163.00,
163.50,
229.50,
280.50,
240.50,
157.00,
14.50,
]

def cal_xyz(lx,ly,rx,ry):
    # 如果在中线左边
    print(lx,ly,rx,ry)
    if lx < standard_distance_horizontal / 2:
        angle1 = np.pi / 2 + np.arctan((standard_distance_horizontal / 2 - lx) / standard_distance_depth)
    else:
        angle1 = np.pi / 2 - np.arctan((lx - standard_distance_horizontal / 2) / standard_distance_depth)
    if rx<standard_distance_horizontal/2:
        angle2 = np.pi/2+np.arctan((standard_distance_horizontal/2-rx)/standard_distance_depth)
    else:
        angle2 = np.pi/2-np.arctan((rx-standard_distance_horizontal/2)/standard_distance_depth)
    X = 0.12/(1-np.tan(angle1)/np.tan(angle2))-0.06
    Z = np.tan(angle1)*(X+0.06)
    Y =Z/(standard_distance_vertical/2/standard_ver_d_depth/(((ly+ry)/2)-standard_distance_vertical/2))
    X*=1000
    Y*=1000
    Z*=1000
    return X,Y,Z


def print_list(a):
    for i in range(len(a)):
        print(a[i])

X_list=[]
Y_list=[]
Z_list=[]
for i in range(len(x1_list)):
      X,Y,Z = cal_xyz(x1_list[i]+1,y1_list[i],x2_list[i],y2_list[i])
      X_list.append(X)
      Y_list.append(Y)
      Z_list.append(Z)

print("X")
print_list(X_list)
print("Y")
print_list(Y_list)
print("Z")
print_list(Z_list)



