import folium
def get_map(corr_lst,waste_per,waste_type):
    c=[]
    for i in waste_per:
        if i < "60":
            c.append("green")
        else:
            c.append("red")

    my_map4 = folium.Map([13.0541,77.61955],zoom_start = 15) 
    sensor_level=[23,67,89,7,86,98]
    folium.Marker([13.0541,77.61955],popup = 'Rest1',icon=folium.Icon(color=c[0])).add_to(my_map4) 
    folium.Marker([13.05477,77.61179],popup = 'Rest2',icon=folium.Icon(color=c[1])).add_to(my_map4) 
    folium.Marker([13.05436,77.60706],popup = 'Rest3',icon=folium.Icon(color=c[2])).add_to(my_map4)
    folium.Marker([13.05098,77.60819],popup = 'Rest4',icon=folium.Icon(color=c[3])).add_to(my_map4)
    folium.Marker([13.0479,77.61232],popup = 'Rest5',icon=folium.Icon(color=c[4])).add_to(my_map4)
    folium.Marker([13.04754,77.61984],popup = 'Rest6',icon=folium.Icon(color=c[5])).add_to(my_map4)
    folium.Marker([13.05213,77.62473],popup = 'Starting point',icon=folium.Icon(color='red')).add_to(my_map4)


    database_list=corr_lst        

    folium.PolyLine(locations = database_list,line_opacity = 0.5).add_to(my_map4)
    path_str = "C:\\Users\\flash\\Desktop\\prro_fin\\templates\\map"+ waste_type+".html"
    my_map4.save(path_str)