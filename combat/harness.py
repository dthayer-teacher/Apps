
class Race:
    def __init__(self):
        self.race_number = 0
        self.speed_rate=0
        self.num_horses = 0
        self.calc_speed=0
        # self.num_speed = num_speed
        self.race_speeds ={}
        self.beat_speed = {}
        self.calc_loop()
    def calc_loop(self): 
        self.how_many=0

        race_file = open('race.txt','r')
        line = race_file.readline()
        line = line.rstrip("\n")
        self.num_of_races=int(line)
        while line != '':
            
            line = race_file.readline()
            while self.how_many<self.num_of_races:
                self.how_many+=1
                
                line = line.rstrip("\n")
                self.race_number= int(line)
                self.class_name = race_file.readline()
                self.class_name=self.class_name.rstrip("/n")
                name_list.append(self.class_name)
                self.num_horses = race_file.readline()
                self.num_horses =int(self.num_horses.rstrip("\n"))
                self.speed_rate = race_file.readline()
                self.speed_rate =int(self.speed_rate.rstrip("\n"))
                self.horse_number = 0
                self.num_speed=0
                self.extra_speed=0
                self.race_speeds={}
            
                while self.horse_number<self.num_horses:
                    count = 0
                    self.num_speed=0
                    self.speed=0
                    self.calc_speed=0
                    self.extra_speed=0
                    self.horse_number = race_file.readline()
                    self.horse_number = int(self.horse_number.rstrip("\n"))
                    self.speed = race_file.readline()
                    self.speed=self.speed.rstrip("\n")
                    while self.speed!="End":
                        # print("in loop")
                        count +=1
                        self.num_speed +=1
                        self.speed=int(self.speed)
                        # print(self.speed)
                        if self.speed > self.speed_rate:
                            self.extra_speed+=1
                        if count<= 2:
                            self.speed = 2*self.speed
                            self.num_speed+=1
                            if self.speed  ==0: 
                                self.num_speed = self.num_speed-2
                        if count>2:
                            if self.speed ==0:
                                self.num_speed = self.num_speed - 1
                        self.calc_speed += self.speed
                        # print(self.calc_speed)
                        self.speed = race_file.readline()
                        self.speed=self.speed.rstrip("\n")
                    # self.horse_number+=1
                    # print("read end")

                    if self.num_speed==0:
                        self.num_speed=1
                    self.horse_speed = self.calc_speed/self.num_speed
                    self.race_speeds[self.horse_number]=self.horse_speed
                    self.beat_speed[self.horse_number]=self.extra_speed

                self.sorted_dict = dict(sorted(self.race_speeds.items(), key=lambda x: x[1], reverse=True))
                # print(self.sorted_dict)
                print("------------------------------")
                print("Race",self.how_many)
                print("------------------------------")
                print("Predicted Order of Finish")
                print("--------- ----- -- ------")
                for key,value in self.sorted_dict.items():
                    
                        print(key, ':', "%.2f"%value,":","%.2f"%(value-self.speed_rate),":",self.beat_speed[key])

                line = race_file.readline()

        #     line = line+line
        #     print(line)
        #     line = race_file.readline()
        # race_file.close()
        # for i in range(1,self.num_horses+1):
        #     self.calc_speed=0
        #     self.extra_speed = 0
        #     print("Horse number "+str(i))
        #     print("----- ------ -")
        #     self.num_speed = int(input("How many speed entries: "))
        #     print("------------------------------------")
        #     for j in range(1,self.num_speed+1):
        #         self.speed = int(input("Enter speed "+str(j)+": "))
        #         if self.speed > self.speed_rate:
        #             self.extra_speed+=1
        #         if j<= 2:
        #             self.speed = 2*self.speed
        #             self.num_speed+=1
        #             if self.speed  ==0: 
        #                 self.num_speed = self.num_speed-2
        #         if j>2:
        #             if self.speed ==0:
        #                 self.num_speed = self.num_speed - 1
        #         self.calc_speed += self.speed 
        #     self.horse_speed = self.calc_speed/self.num_speed
        #     self.race_speeds[i]=self.horse_speed
        #     self.beat_speed[i]=self.extra_speed
        # self.sorted_dict = dict(sorted(self.race_speeds.items(), key=lambda x: x[1], reverse=True))

        # print(self.sorted_dict)
        # print("Predicted Order of Finish")
        # print("--------- ----- -- ------")
        # for key,value in self.sorted_dict.items():
            
        #         print(key, ':', "%.2f"%value,":","%.2f"%(value-self.speed_rate),":",self.beat_speed[key])


# with open("test.txt","w") as testtxt:
#           testtxt.write("test")
name_list = []

# race_number = int(input("How many races: "))

# num_horses = int(input("How many horses in race: "))

# race_speeds ={}
# beat_speed = {}

calc_speed = 0
print("hello")
# class_rating = int(input("What is the class rating of the race: "))

# race = Race(race_number,class_rating,num_horses)
race = Race()
# for name in name_list:

#     print(name)
# for i in range(1,num_horses+1):
#     calc_speed=0
#     extra_speed = 0
#     print("Horse number "+str(i))
#     print("----- ------ -")
#     num_speed = int(input("How many speed entries: "))
#     print("------------------------------------")
#     for j in range(1,num_speed+1):
#         speed = int(input("Enter speed "+str(j)+": "))
#         if speed > class_rating:
#              extra_speed+=1
#         if j<= 2:
#             speed = 2*speed
#             num_speed+=1
#             if speed  ==0: 
#                  num_speed = num_speed-2
#         if j>2:
#              if speed ==0:
#                   num_speed = num_speed - 1
#         calc_speed += speed 
#     horse_speed = calc_speed/num_speed
#     race_speeds[i]=horse_speed
#     beat_speed[i]=extra_speed


# print(race_speeds)


# sorted_dict = dict(sorted(race_speeds.items(), key=lambda x: x[1], reverse=True))

# print(sorted_dict)
# print("Predicted Order of Finish")
# print("--------- ----- -- ------")
# for key,value in sorted_dict.items():
    
#         print(key, ':', "%.2f"%value,":","%.2f"%(value-class_rating),":",beat_speed[key])




