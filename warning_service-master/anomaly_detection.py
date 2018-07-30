import numpy as np
import math 
import random

class Amean :

    def __init__(self, input_list=[], angle_list=[]) :
      
        self.time_list = list(input_list)
        self.angle_list = list(angle_list)

        self.update_flag = True
        self.update_counter = 0

        self.TRAIN_SIZE = 150
        return


# ================
    def __log (self, msg) :
        with open("log.txt","a") as f :
            f.write(msg + '\n')
        return 


    def __update_list (self, current, input_list=[], size=700, loop=5) :    
        if self.update_flag : loop = 5     
        sorted_list = sorted(input_list)
        time_list = list(input_list)
        for index in range(len(sorted_list)) :
            if current < sorted_list[index] or index== len(sorted_list)-1 : 
                time_list.append (current)
                for i in range(loop) :
                    if index + i < len(sorted_list) :
                        time_list.append ((current + sorted_list[index + i]) / 2)
                    if index - i > 0 :
                        time_list.append ((current + sorted_list[index - i]) / 2)
                break
        while len(time_list) > size :
            time_list.pop(0)
        return time_list
        

    def __update (self, current, angle) :   
        self.time_list = self.__update_list(current=current, input_list=self.time_list)
        self.angle_list = self.__update_list(current=angle, input_list=self.angle_list)     
        return
    
    def __update_init (self, current, angle) :
        self.time_list.append(current)
        self.angle_list.append(angle)
        return

#=====================
    def __algoA (self, current, time_list=[], thres=[0.03, 0.95]) :
        # This algo base on splitting thres on value (timelist)
        def index(position) :
            return int(math.floor(len(time_list)*position))

        time_list = sorted(time_list)

        if current > time_list[index(thres[1])] :
            if current > (np.average([time_list[index(thres[1])],max(time_list)])) :
                self.update_flag = False
                return -1

        if current < time_list[index(thres[0])] :
            self.update_flag = False
            return 0
        else :
            self.update_flag = True
            return 1
            
    
    def __check_medium_range(self, time_list, thres) :
        # stop using this func
        def index(position) :
            return int(math.floor(len(time_list)*position))
        
        time_list = sorted(time_list)

        pos_min = index(thres[0])
        pos_max =index(thres[1])

        medium = np.average(time_list[pos_min : pos_max])

        min_med = np.average([x for x in time_list[pos_min:pos_max] if x < medium])
        max_med = np.average([x for x in time_list[pos_min:pos_max] if x > medium])

        return [min_med, max_med]


        
    def __get_warning (self, thres, value) :
        def get_safe_range (time_list, thres) :
            time_list = sorted(time_list)
            minimum = time_list[int(math.floor(len(time_list) * thres[0]))]
            maximum = time_list[int(math.floor(len(time_list) * thres[1]))]
            return [minimum, maximum]
        def get_warning_level (time_list, thres, value) :
            safe_range = get_safe_range(time_list, thres)
            if value >= safe_range[0] and value <= safe_range[1]:
                return 0
            # if not safe : 
            if value < safe_range [0] :
                time_list_1 = [x for x in time_list if x < safe_range[0]]
                if value <= np.average(time_list_1) : return 3
                time_list_2 = [x for x in time_list_1 if x > np.average(time_list_1)]
                if value <= np.average(time_list_2) : return 2
                else : return 1
            if value > safe_range [1]:
                time_list_1 = [x for x in time_list if x > safe_range[1]]
                if value >= np.average(time_list_1) : return 3
                time_list_2 = [x for x in time_list_1 if x < np.average(time_list_1)]
                if value >= np.average(time_list_2) : return 2
                else : return 1
            

        anomaly_result = 0

        w = [0.6, 0.4]

        t0 = get_warning_level(self.time_list, thres[0], value[0])
        anomaly_result += w[0] * t0
        print("anomaly_result1 ",anomaly_result)

        t1 = get_warning_level(self.angle_list, thres[1], value[1])
        anomaly_result += w[1] * t1
        print("anomaly_result2 ",anomaly_result)
        return math.floor(anomaly_result)
        # t_med = self.__check_medium_range(self.time_list, thres[0])
        # result = [min([result[0], t_med[0]]), max([result[1], t_med[1]])]
        # return anomaly_result
      

#======================================    
    def get_list (self) :
        return self.time_list
    

    def train (self, input_list=[], angle_list=[]) :
        for i in range(len(input_list)) :
            self.predict(input_list[i], angle_list[i])
        return


    def predict (self, current, angle) :
        current = float(current)
        angle = float(angle)
        print("Len of data: ", len(self.time_list))
        if len(self.time_list) < self.TRAIN_SIZE :
            self.__update_init(current=current, angle=angle)  
            return ''
        
        # self.__log(str(current) + ' ' + str(angle))
        self.update_flag = True

        thres_1 = [0.1, 0.92]
        thres_2 = [0.025, 0.98]
        thres_val = [0,0]
        msg = ""
        
        thres = [thres_1, thres_2]
        value = [current, angle]
        warning_level = self.__get_warning(thres, value)

        # traning
        self.__algoA(current=current, time_list=self.time_list,thres=thres_1)
        self.__algoA(current=angle, time_list=self.angle_list,thres=thres_2)
        
        self.__update(current=current, angle=angle)
        print("warning_level: ", warning_level)
        return warning_level





























# def __algoB (self, current) :
#         # This algo is based on the medium incresing or decreasing of data
#         thres = 1.35
#         thres_1 = 2.05
#         average = np.average(self.queue)
#         change = [(self.queue[i+1] - self.queue[i]) for i in range(len(self.queue) - 1)]
#         max_increase = np.max(change)
#         average_increase = np.average([x for x in change if x > 0])
#         min_decrease = np.min(change)
#         average_decrease = np.average([x for x in change if x < 0])
        
#         current = current - self.queue[-1]
#         # print (":::", increase, decrease, current)
#         if current > 0 :
#             if current > thres * max_increase and current > thres_1 * average_increase :
#                 self.update_flag = False
#                 return -1
#             else : return True 
#         if current < 0 :
#             if current < thres * min_decrease and current < thres_1 * average_decrease :
#                 self.update_flag = False
#                 return 0
#             else : return True 



# result_2 = self.__algoB(current)
        # if not result_2 : 
        #     if update : self.__update(current=current, angle=angle)
        #     return {'id':result_2, 'msg':"Co su tang giam bat thuong trong do thi so voi nhung ngay truoc do", 'thres':thres_val}