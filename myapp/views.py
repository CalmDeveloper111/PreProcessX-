from django.shortcuts import render , HttpResponse , get_object_or_404 , redirect
from . import pp
import pandas as pd 
import numpy as np
from myapp.models import datasets
from django.http import FileResponse


# Create your views here.

def index(request) :

    data = datasets.objects.all().values()

    context = {
        'data' : data
    }


    return render(request,'index.html' , context)

def file_upload(request) :
    if request.method == 'POST' :
        uploaded_file = request.FILES['file']
        data = pd.read_csv(uploaded_file)

        return data

        # result = process(data)
        # result_html = result.to_html(index=False)
        # return render_template(request,result_full_process,result_missing_values_count_before,result_missing_values_count_after)

        # return render(request,'analysisresult.html',{'result':result_html})

        # return render_template(request,result_html)
    else :
        return render(request,'upload.html')
    

def process(request) :
    data = file_upload(request)

    # before imputation count
    result_missing_values_count_before = pp.missing_values_count(data)
    df = result_missing_values_count_before.to_frame()
    result_missing_values_count_before = df.to_html(index=True)
    pie_data = pp.pie_chart(data)
    execute = pp.data_preprocessing_pipline(data)
    result_full_process = execute.to_html(index=False)
    return missing_values_count(request,result_full_process,result_missing_values_count_before,data,pie_data)


def missing_values_count(request,result_full_process,result_missing_values_count_before,data,pie_data) :
    execute = pp.missing_values_count(data)
    df = execute.to_frame()
    result_missing_values_count_after = df.to_html(index=True)
    
    return  render_template(request,result_full_process,result_missing_values_count_before,result_missing_values_count_after , pie_data)


    # pie(request,result_full_process,result_missing_values_count_before,result_missing_values_count_after,data)


# def pie(request , result_full_process,result_missing_values_count_before,result_missing_values_count_after ,data) :

#     piechart = pp.pie_chart(data)



    # return render_template(request,result_full_process,result_missing_values_count_before,result_missing_values_count_after , piechart)



def render_template(request,result_full_process,result_missing_values_count_before,result_missing_values_count_after,piechart) :
    return render(request,'analysisresult.html',{'result_full':result_full_process,
                                                 'result_counts_after' : result_missing_values_count_after,
                                                   'result_counts_before' : result_missing_values_count_before,
                                                   'pie_chart':piechart})
    


def dataset(request , id) :

    file = get_object_or_404(datasets , id = id)

    file_path = file.file.path
    response = FileResponse(open(file_path , 'rb'))
    response['Content-Disposition'] = f'attachment; filename = "{file.name}"'

    return response

    # if file.file :
    #     file_path = file.file.path
    #     with open(file_path , 'r') as f :
    #         file_content = f.read()

    # context = {
    #     'file' : file ,
    #     'file_content' : file_content , 
    # }

    # return render(request , 'dataset.html' , context)