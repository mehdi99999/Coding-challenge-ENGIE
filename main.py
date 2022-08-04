from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/productionplan/', methods=['POST'])
def calculateProductionPlan():
    data = request.json
    load = data['load']
    feature = data['powerplants']
    fuels = data['fuels']
    
    for k in range (len(feature)):
        if feature[k]['type']=='windturbine':
            feature[k]['minimum_price'] = 0
        elif feature[k]['type']=='turbojet':
            feature[k]['minimum_price'] = fuels['kerosine(euro/MWh)']/(feature[k]['efficiency'])
        elif feature[k]['type']=='gasfired':
            feature[k]['minimum_price'] = feature[k]['pmin']*(fuels['gas(euro/MWh)']+0.3*fuels['co2(euro/ton)'])/(feature[k]['efficiency'])

    #trier pour optimiser le coût
    for i in range(1, len(feature)):
        current_position = i
        current_element = feature[i]  
        while current_position > 0 and current_element['minimum_price'] < feature[current_position-1]['minimum_price']:
            feature[current_position] = feature[current_position-1]
            current_position -= 1
        feature[current_position] = current_element
    
    
    
    name_total = []
    p_total = []
    p=0
    tempLoad = load
    
    for j in range (len(feature)):
        if tempLoad <= 0:
            p = 0
            
        else:    
            if feature[j]['type'] == 'windturbine':
                p = min(feature[j]['pmax']*fuels['wind(%)']/100,tempLoad)
            elif feature[j]['type'] == 'gasfired' or feature[j]['type'] == 'turbojet':
                p = min(feature[j]['pmax'],tempLoad)
                
                if p < feature[j]['pmin']:
                    p_total[j-1]=p_total[j-1]-(feature[j]['pmin'] - p)
                    p = feature[j]['pmin']
                    tempLoad = p
                    
            #updating load    
            tempLoad = tempLoad - p
            
        #adding corresponding p and name to the output
        name_total.append(feature[j]['name'])
        p_total.append(round(p,1))
        
    p = p_total
    name = name_total
    response={}

    for k in range (len(p)):
        response[k]={
                'name': name[k],
                'p': p[k]}

    return(response)


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
    