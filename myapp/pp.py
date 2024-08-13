import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def data_preprocessing_pipline(data):
    #identifying numerical and categorical columns
    num_features = data.select_dtypes(include=['integer','float']).columns
    cat_features = data.select_dtypes('object').columns
    
    #imputing missing vlaues 
    data[num_features] = data[num_features].fillna(data[num_features].mean())
    data[cat_features] = data[cat_features].fillna(data[cat_features].mode().iloc[0])
    
    # Handling outliers
    for feature in num_features :
        Q1 = data[feature].quantile(0.25)
        Q3 = data[feature].quantile(0.75)
        IQR = Q3 - Q1
        low_bound = Q1 - (1.5 * IQR)
        upp_bound = Q3 + (1.5 * IQR)
        # data[feature] = np.where( data[feature] < low_bound or data[feature].any() > upp_bound , data[feature].mean() , data[feature])
        
        
    # Normalization 
    # scaler = StandardScaler()
    # scaled_data = scaler.fit_transform(data[num_features])
    # data[num_features] = scaler.transform(data[num_features])
    print('process is successfully completed')
    return data


def missing_values_count(data) :
    total_missing_values = data.isnull().sum()
    return total_missing_values



def pie_chart(data) :
    total_missing_values=data.isnull().sum()

    a1 ={}
    for i in total_missing_values.keys() :
        if total_missing_values[i] == 0 :
            continue
        else :
            a1[i] = total_missing_values[i]

    a1 = pd.Series(a1)

    plt.switch_backend('Agg')
    fig = plt.figure(figsize = (10,8))
    ax = fig.add_subplot(111)
    ax.pie( a1 , labels = a1.index , colors=['gold','silver','pink','green','blue','red'],autopct = '%1.1f%%' , startangle=140)
    # ax.set_title('proportion of missing vlaues')

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer,format = 'png')
    buffer.seek(0)

    pie_data = base64.b64encode(buffer.read()).decode()

    plt.close(fig)
     
    
    return pie_data



# print("base64 pie chart data :" , pie_data[:100])