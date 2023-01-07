import main_code
from main_code import time_between_function_call
import matplotlib.pyplot as plt
import time

x_obj=500
y_obj=500
x_array = []
y_array= []
# for i in range(0,10000):
#         # get x,y from aruco or color detection
#     main_code.movedrone(x_obj , y_obj)
#     time.sleep(time_between_function_call)
#     x_array.append(x_obj)
#     y_array.append(y_obj)
#     print(f'{i} iteration x coordinate was{x_obj} y coordinate was {y_obj}\n')
# plt.plot(x_array,y_array, label = "drone Position")
# plt.legend()
# plt.ylim(-1000,1000)
# plt.xlim(-1000,1000)
# plt.show()

main_code.takeoff()