from flask import Flask,Markup, render_template
import pymongo
import random
from datetime import datetime,timedelta  
import doctest
from itertools import permutations
import dns
import folium
from math import sin, cos, sqrt, atan2, radians
app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb+srv://sitesh:Sitesh$$#5@cluster0-9jms6.azure.mongodb.net/test?retryWrites=true&w=majority")

def get_per_waste(): 
    time = datetime.now() - timedelta(days = 1) 

    mydb = myclient["Waste_Management"]
    timestampStr = time.strftime("%d-%b-%Y")
    mycol = mydb[timestampStr]
    waste_per_wet = []
    res_name_wet = []
    waste_per_dry = []
    res_name_dry = []
    for x in mycol.find():
        if (x['_id'] % 2 == 0):
            waste_per_wet.append(x['waste_per'])
            res_name_wet.append(x['Res_name'])
        else:
            waste_per_dry.append(x['waste_per'])
            res_name_dry.append(x['Res_name'])
    
    return waste_per_wet,res_name_wet,waste_per_dry,res_name_dry
'''waste_wet,corr_wet,name_wet = get_cor_wet()
#for k in corr:
 #   plt.plot(k[:,0],k[:,1])
for i,j in corr_wet:
    #print(i)
    plt.plot([0,i],[0,j],'ro')
time2 = datetime.now()
time2Str=time2.strftime("%m%d%Y%H%M")  
path_img_wet = "static/images/"+"wet_"+time2Str+".png"
plt.savefig(path_img_wet)'''
'''
for i,j in corr_dry:
    #print(i)
    plt.plot([0,i],[0,j],'ro')
time3 = datetime.now()
time3Str=time3.strftime("%m%d%Y%H%M")  
path_img_dry = "static/images/"+"dry_"+time3Str+".png"
plt.savefig(path_img_dry)
'''
def get_corr():
    time = datetime.now() - timedelta(days = 1) 

    mydb = myclient["Waste_Management"]
    timestampStr = time.strftime("%d-%b-%Y")
    mycol = mydb[timestampStr]
    corr_dry = []
    corr_wet = []
    for x in mycol.find():
        if (x['waste_per']>=60):
        
            if (x['_id'] % 2 == 0):
                corr_wet.append(x['Res_cor'])
            else:
                
                corr_dry.append(x['Res_cor'])
    
    return corr_wet,corr_dry
waste_per_wet,name_wet,waste_per_dry,name_dry =get_per_waste()
def get_map(corr_lst,waste_per,waste_type):
    c=[]
    for i in waste_per:
        if i < 60:
            c.append("green")
           
        else:
            c.append("red")
    Starting_point = [12.97229,77.68118]
    corr_lst.append(Starting_point)
    my_map4 = folium.Map([12.97229,77.68118],zoom_start = 12) 
    folium.Marker([13.0708,77.65186],popup = 'Rest1',icon=folium.Icon(color=c[0])).add_to(my_map4) 
    folium.Marker([13.02248,77.55055],popup = 'Rest2',icon=folium.Icon(color=c[1])).add_to(my_map4) 
    folium.Marker([12.99196,77.58831],popup = 'Rest3',icon=folium.Icon(color=c[2])).add_to(my_map4)
    folium.Marker([12.96736,77.59559],popup = 'Rest4',icon=folium.Icon(color=c[3])).add_to(my_map4)
    folium.Marker([12.97923,77.72845],popup = 'Rest5',icon=folium.Icon(color=c[4])).add_to(my_map4)
    folium.Marker([12.82465,77.68118],popup = 'Rest6',icon=folium.Icon(color=c[5])).add_to(my_map4)
    folium.Marker([12.97229,77.68118],popup = 'Starting point',icon=folium.Icon(color='darkpurple')).add_to(my_map4)

    

    database_list=travelling_salesman(corr_lst) 
    print(database_list)
    folium.PolyLine(locations = database_list,line_opacity = 0.5).add_to(my_map4)
    path_str = "C:\\Users\\flash\\Desktop\\prro_fin\\templates\\map"+ waste_type+".html"
    my_map4.save(path_str)
#############3=================#####################3
cor_wet,cor_dry = get_corr()
    
def dist(p1,p2):
    R = 6373.0

    lat1 = radians(p1[0])
    lon1 = radians(p1[1])
    lat2 = radians(p2[0])
    lon2 = radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def total_distance(points):
    """
    Returns the length of the path passing throught
    all the points in the given order.

    >>> total_distance([[1,2],[4,6]])
    5.0
    >>> total_distance([[3,6],[7,6],[12,6]])
    9.0
    """
    return sum([dist(point, points[index + 1]) for index, point in enumerate(points[:-1])])
def travelling_salesman(points, start=[12.97229,77.68118]):
    """
    Finds the shortest route to visit all the cities by bruteforce.
    Time complexity is O(N!), so never use on long lists.

    >>> travelling_salesman([[0,0],[10,0],[6,0]])
    ([0, 0], [6, 0], [10, 0])
    >>> travelling_salesman([[0,0],[6,0],[2,3],[3,7],[0.5,9],[3,5],[9,1]])
    ([0, 0], [6, 0], [9, 1], [2, 3], [3, 5], [3, 7], [0.5, 9])
    """
    if start is None:
        start = points[0]
    return min([perm for perm in permutations(points) if perm[0] == start], key=total_distance)
    

    
 
@app.route("/home")
def home_page():
    #waste_per,corr,name =get_cor_wet()
    #name_info = zip(waste_per,name)
    return render_template('home.html')
    
@app.route("/map")
def google_map1():
    waste_per_wet,name_wet,waste_per_dry,name_dry =get_per_waste()
    cor_wet,cor_dry = get_corr()
    get_map(cor_dry,waste_per_dry,"dry")
    return render_template('mapdry.html')
@app.route("/map1")
def google_map2():
    waste_per_wet,name_wet,waste_per_dry,name_dry =get_per_waste()
    cor_wet,cor_dry = get_corr()
    get_map(cor_wet,waste_per_wet,"wet")
    return render_template('mapwet.html')
@app.route("/wet_chart")
def chart_wet():
    waste_per_wet1,name_wet1,waste_per_dry1,name_dry1 =get_per_waste()
    
    return render_template('chart_v2.html',waste_per=waste_per_wet1,name=name_wet1)
    
@app.route("/dry_chart")
def chart_dry():
    waste_per_wet1,name_wet1,waste_per_dry1,name_dry1 =get_per_waste()
    return render_template('chart_v2.html',waste_per=waste_per_dry1,name=name_dry1)
@app.route("/mylink1")
def clear_bar1():
    waste_per_dry[0] = "0" 
   
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
    
@app.route("/mylink2")
def clear_bar2():
    waste_per_dry[1] = "0" 
   
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
    
@app.route("/mylink3")
def clear_bar3():
    waste_per_dry[2] = "0" 
    
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
 
@app.route("/mylink4")
def clear_bar4():
    waste_per_dry[3] = "0" 
   
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
    
@app.route("/mylink5")
def clear_bar5():
    waste_per_dry[4] = "0" 
   
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
    
@app.route("/mylink6")
def clear_bar6():
    waste_per_dry[5] = "0"
   
    return render_template('chart_v2.html',waste_per=waste_per_dry,name = name_dry)
    
@app.route("/mylink1")
def clear_bar7():
    waste_per_wet[0] = "0" 
   
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
    
@app.route("/mylink2")
def clear_bar8():
    waste_per_wet[1] = "0" 
   
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
   
@app.route("/mylink3")
def clear_bar9():
    waste_per_wet[2] = "0" 
    
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
 
@app.route("/mylink4")
def clear_bar10():
    waste_per_wet[3] = "0" 
   
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
    
@app.route("/mylink5")
def clear_bar11():
    waste_per_wet[4] = "0" 
   
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
    
@app.route("/mylink6")
def clear_bar12():
    waste_per_wet[5] = "0"
   
    return render_template('chart_v2.html',waste_per=waste_per_wet,name = name_wet)
    

'''
@app.route('/dry_path')
def dry():
  return render_template('chrt.html', name = 'new_plot', url =path_img_dry)

@app.route('/wet_path')
def wet():
  return render_template('chrt.html', name = 'new_plot', url =path_img_wet)
'''
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001,debug="True")