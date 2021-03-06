import tensorflow as tf
import h5py
import cv2
import numpy as np


def getModelConfig(file):
    return tf.keras.models.load_model(file).get_config()


def getLayersName(file):
    
    layer_name = []
    
    model = getModelConfig(file)
    model = model['layers']
    model_length = len(model)

    for i in range(model_length):
        model_name = model[i]['class_name']
        layer_name.append(model_name)

    return layer_name


def getModelLayersConfig(file):
    
    model_config_list = []
    

    model_config = getModelConfig(file)
    model_config = model_config['layers']
    model_config_length = len(model_config)

    for i in range(model_config_length):
        model_config_in_for = model_config[i]['config'].items()
        model_i = []

        for i in model_config_in_for:
            model_i.append(i)

        model_config_list.append(model_i)

    return model_config_list
    
    
def showModelSummary(file):
    tf.keras.models.load_model(file).summary()
    
    
def getModelLayersConfigNormalization(file):
    model_layer_config = getModelLayersConfig(file)
    
    # <-- Nomarlization -->
    all_model_legnth = len(model_layer_config)
    NoneType_index = []
    
    for i in range(all_model_legnth):
        model_lenght = len(model_layer_config[i])
        
        for j in range(model_lenght):
            value = model_layer_config[i][j][1]
            if(value == None):
                NoneType_index.append([i, 
                                       j, 
                                       model_layer_config[i][j]
                                      ])

    for data in NoneType_index:
        i, j, removeData = data
        model_layer_config[i].remove(removeData)
    # <-- FINISH -->    
    
    return model_layer_config

def getOptimazer(file):
    try:
        path = file
        f = h5py.File(path, 'r')
        f_keys = list(f.keys())
        f_keys_keys = list(f[f_keys[1]].keys())
        return f_keys_keys[0]
    except:
        return None

def printLayer(path):
    
    layers_name = getLayersName(path) 
    data = getModelLayersConfigNormalization(path)
    optimazier = getOptimazer(path)
    
    print(f"Optimazer : {optimazier}\n")
    for i in range(len(data)):

        init_new = 0

        print(f"Layer_{i} | Name : {layers_name[i]}")

        if (i == 0):
            init = 1
            batch_input_shape = data[i][2][1]

            for j in batch_input_shape:
                if (j == None):
                    j = 1
                init = init * j 

            print(f"Layer_{i} | input_shape : {batch_input_shape}")
            print(f"Layer_{i} | output_shape : {init}")
            print(f"Layer_{i} | Paragms : {init_new}\n")


        else:

            if(data[i][3][0] == "units"):

                nowlayer = i

                neruons = data[i][3][1]
                init_new = init * data[i][3][1] + data[i][3][1]
                init = data[i][3][1] # init update

                print(f"Layer_{i} | Neurons : {neruons}")
                print(f"Layer_{i} | Paragms : {init_new}\n")


            elif(data[i][3][0] == "rate"):

                rate = data[i][3][1] * 100

                print(f"Layer_{i} | Rate : {rate}%")
                print(f"Layer_{i} | Paragms : {init_new}\n")



            elif(data[i][3][0] == "activation"):

                funtion_name = data[i][3][1]

                print(f"Layer_{i} | Funtion : {funtion_name}")
                print(f"Layer_{i} | Paragms : {init_new}\n")


            else:
                # unknow part need update this part
                print("XXXXXXXXXXXX")
                print(f"Layer_{i} | {data[i][3][0]} : {data[i][3][1]}")
                
                
def getLayersInfo(path):
    return_list = []
    try:
        layers_name = getLayersName(path) 
        data = getModelLayersConfigNormalization(path)
        optimazier = getOptimazer(path)

        return_list.append({"optimazier" : optimazier})

        for i in range(len(data)):

            init_new = 0

            if (i == 0):
                init = 1
                batch_input_shape = data[i][2][1]

                for j in batch_input_shape:
                    if (j == None):
                        j = 1
                    init = init * j 


                layer_data_dic = {
                    "layer" : layers_name[i],
                    "input_shape" : batch_input_shape,
                    "output_shape" : init,
                    "paragms" : init_new
                }

                return_list.append(layer_data_dic)


            else:

                if(data[i][3][0] == "units"):

                    nowlayer = i

                    neruons = data[i][3][1]
                    init_new = init * data[i][3][1] + data[i][3][1]
                    init = data[i][3][1] # init update

                    layer_data_dic = {
                        "layer" : layers_name[i],
                        "neruons" : neruons,
                        "paragms" : init_new
                    }

                    return_list.append(layer_data_dic)

                elif(data[i][3][0] == "rate"):

                    rate = data[i][3][1] * 100


                    layer_data_dic = {
                        "layer" : layers_name[i],
                        "rate" : rate,
                        "paragms" : init_new
                    }

                    return_list.append(layer_data_dic)

                elif(data[i][3][0] == "activation"):

                    funtion_name = data[i][3][1]

                    layer_data_dic = {
                        "layer" : layers_name[i],
                        "funtion" : funtion_name,
                        "paragms" : init_new
                    }

                    return_list.append(layer_data_dic)

                else:
                    print("XXXXXXXXXXXX")
                    return_list.append(None)
    finally:
        return return_list
    
    
def getBlankImage(height, width, dimension=3):
    return np.zeros((height, width, dimension), np.uint8)

def showImage(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def getArrowStartPoint(circle_center, radius):
    x, y = circle_center
    return (x-radius, y)

def getArrowEndPoint(circle_center, radius):
    x, y = circle_center
    return (x+radius, y)

def getSectionWight(section_num, section, wight):
    
    if (wight % section_num == 0):
        new_w = (wight / section_num)
    else:
        new_w = int(wight / section_num)
    
    if (new_w % 2 == 0):
        move_w = (new_w * (section-1)) + (new_w / 2)
    else:
        move_w = (new_w * (section-1)) + int(new_w / 2)
        
    return move_w

def getSectionHeigh(h, num):
    
    if (h % num == 0):  
        distance = h / num
    else:
        if (num >= int(h / num)):
            distance = int(h / num)
        else:
            distance = int(h / num) - 1
            
    blank_piexl = (h - (distance * num))

    sub_h = h - blank_piexl    
    add_h = 0
    return_h_list = []
    
    while(True):
        if(add_h == sub_h):
            break
        else:
            return_h_list.append(add_h + (blank_piexl / 2))
            add_h = add_h + distance
    
    return return_h_list

def drawingNerons(img, data, radius=1, color=(255, 255, 255)):
    for i in data:
        img = cv2.circle(img=img,
                         center=i,
                         radius=radius,
                         color=color,
                         thickness=-1)
    return img

def getNeuronPostion(img_w, img_h, number_of_section, section, number_of_neuron):
    
    x = getSectionWight(wight=img_w, 
                        section_num=number_of_section, 
                        section=section)
    
    
    y = getSectionHeigh(h=img_h, 
                        num=number_of_neuron)
    circe_center = []
    for i in y:
        data = (int(x), int(i + ((img_h - y[len(y) - 1]) / 2)))
        circe_center.append(data)
    return circe_center

def drawingLines(img, data, radius=1):
    
    values = []
    for now_data in range(len(data)):
        values.append(data[now_data])
    

    for a in range(len(values)):
        if (len(values)-1 >= (a+1)):
            for i in values[a]:
                for j in values[a+1]:
                    img = cv2.line(img=img,
                                   pt1=getArrowEndPoint(i, radius),
                                   pt2=getArrowStartPoint(j, radius),
                                   color=(255, 255, 0))
        else:
            pass

    return img

# Data Sequence n_neuron, n_sction_number
def getAllNeurons(img, img_w, img_h, number_of_sction, data):
    tmp_list = []
    
    for i in range(len(data)):
        tmp_list.append(data[i])
    
    return_list = []
    for i in range(len(tmp_list)):
        data = getNeuronPostion(img_w=img_w,
                                         img_h=img_h,
                                         number_of_neuron=tmp_list[i][0],
                                         number_of_section=number_of_sction,
                                         section=tmp_list[i][1])
        return_list.append(data)
    
    
    return return_list

def getDenseList(path):
    model_data = getLayersInfo(path)
    dense_list = []
    for i in range(len(model_data)):
        if i == 0:
            pass
        else:
            data = model_data[i]['layer']
            if data == "Dense":
                getData = ( model_data[i]['neruons'], i)
                dense_list.append(getData)
    return dense_list

def save(img):
    cv2.imwrite("saved.png", img)
    
def model_neurons_position(data, max_num=50, max2min=15):
    return_list = []
    for i in range(len(data)):
        if(data[i][0] > max_num):
            num, sec = data[i]
            num = max2min
            return_list.append([num, sec])
        else:
            return_list.append(list(data[i]))
    return return_list