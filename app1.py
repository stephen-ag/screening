import json
from flask import Flask,render_template, request, jsonify, url_for,Response, redirect
import pandas as pd
#import matplotlib.pyplot as plt
#import xlwt
# need to install xlrd and openpyxl to use read_excel function in pandas
import os
from scipy.signal import find_peaks
import shutil
app = Flask(__name__)
@app.route('/')
@app.route('/home')
def home_page():

    return render_template('index1.html')

@app.route('/about')
def about():
    title= "About time point screening"
    return render_template('about.html', title=title)

@app.route('/delta', methods=['GET', 'POST'])
def delta_data():

    filepath =('Static\Temp.xlsx')
    output4 = pd.read_excel(filepath)
    df22 = output4[output4.filter(regex='^(?!Unnamed)').columns]
    #df22 = df2.drop('Time, sec', axis=1)  # drop the column name from the table
    col2 = df22.columns
    pack2 = []
    for i in col2:
        time_series2 = df22[i]
        indices2 = find_peaks(time_series2, distance=50)[0]  # 50 sample points considered for finding peak
        pack2.append(indices2)

        step = []
        for val in pack2:
            for j in val:
                step.append(j)
        # print(step)

    delta_pk = []
    for i in step:
        if i not in delta_pk:
            delta_pk.append(i)
    delta_list = delta_pk
    fss2 = [int(x) for x in delta_list]
    seriee2 = pd.Series(fss2)
    del2 = seriee2.tolist()
    fss2.sort()
    delta_df = df22.loc[fss2]
    return render_template('delta.html',delta=delta_df.to_html())

@app.route('/clear_data',methods=['GET', 'POST'])
def clear_data():
    filepath = ('Static\Tempvstime.xlsx')
    filepath1 = ('Static\Temp.xlsx')
    if os.path.isfile(filepath):
        os.remove(filepath)
        comment="Tempvstime file has been cleared"
    if os.path.isfile(filepath1):
        os.remove(filepath1)
        comment = "Temp File has been cleared"
    else:
        comment="No file Exists"
    return render_template('download.html', clear_data=comment)
@app.route('/valley_data', methods=['GET', 'POST'])
def valley_data():
    filepath = ('Static\Tempvstime.xlsx')
    output3 = pd.read_excel(filepath)
    #output3 = pd.read_excel(filepath, sheet_name='Temp vs Time', skiprows=3)
    output3 = output3[output3.filter(regex='^(?!Unnamed)').columns]
    from scipy.signal import find_peaks

    df11 = output3 * -1
    coll = df11.columns
    pack1 = []
    for i in coll:
        time_seriess = df11[i]
        iindices = find_peaks(time_seriess)[0]
        pack1.append(iindices)

    datt1 = []
    for i in pack1:
        for j in i:
            datt1.append(j)
    va = []
    for i in datt1:
        if i not in va:
            va.append(i)
    valley_list = va
    fss1 = [int(x) for x in valley_list]
    seriee1 = pd.Series(fss1)
    vvle = seriee1.tolist()
    fss1.sort()
    valley_df = output3.loc[fss1]

    return render_template('valley_data.html', data1=valley_df.to_html())


@app.route('/peak_data', methods=['GET', 'POST'])
def peak_data():
    if request.method == 'POST':
        #output2= request.form.get('fss')
        filepath = ('Static\Tempvstime.xlsx')

        #output2 = pd.read_excel(filepath, sheet_name='Temp vs Time',skiprows = 3)
        output2 = pd.read_excel(filepath)
        output2 = output2[output2.filter(regex='^(?!Unnamed)').columns]
        from scipy.signal import find_peaks
        col = output2.columns
        pack = []
        for i in col:
            time_series = output2[i]
            indices = find_peaks(time_series)[0]
            pack.append(indices)

        datt = []
        for i in pack:
            for j in i:
                datt.append(j)
        pk = []
        for i in datt:
            if i not in pk:
                pk.append(i)
        peak_list = pk
        fsss = [int(x) for x in peak_list]
        seriee = pd.Series(fsss)
        pple = seriee.tolist()
        fsss.sort()
        peak_df = output2.loc[fsss]
        return render_template('peak_data.html', data2=peak_df.to_html())


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        #file = request.form['upload-file']
        file = request.files['upload-file']
        if not os.path.isdir('Static'):
            os.mkdir('Static')

        filepath1 = os.path.join('Static', file.filename)
        print(filepath1)
        if os.path.isfile(filepath1):
            os.remove(filepath1)
        file.save(filepath1)
        #dest = os.path.join('Static' + 'worksheet.xlsx' )
        #os.rename(filepath1,dest)
        #data1 = pd.read_excel(file)

        data1 = pd.read_excel(filepath1,sheet_name='Temp vs Time', skiprows = 3)
        temp_data= pd.read_excel(filepath1,sheet_name='Temperature difference', skiprows = 1)
        data1 = data1[data1.filter(regex='^(?!Unnamed)').columns]
        data1.to_excel('Static\Tempvstime.xlsx',index=False)
        temp_data.to_excel('Static\Temp.xlsx', index=False)
        temp_data = temp_data[temp_data.filter(regex='^(?!Unnamed)').columns]
        #print(data1.shape)
        #print(temp_data.shape)
        dat1 = pd.DataFrame(data1)
        temp_df =pd.DataFrame(temp_data)
        df = dat1

        ####################### find max using scipy fuction for peak############################

        from scipy.signal import find_peaks
        col = df.columns
        pack = []
        for i in col:
            time_series = df[i]
            indices = find_peaks(time_series)[0]
            pack.append(indices)

        datt = []
        for i in pack:
            for j in i:
                datt.append(j)
        pk = []
        for i in datt:
            if i not in pk:
                pk.append(i)
        peak_list = pk
        fss = [int(x) for x in peak_list]
        seriee = pd.Series(fss)
        pple = seriee.tolist()
        fss.sort()
        peak_df = df.loc[fss]
        ####################### find max using scipy fuction for valley ############################
        df1 = df * -1
        col1 = df1.columns
        pack1 = []
        for i in col1:
            time_seriess = df1[i]
            iindices = find_peaks(time_seriess)[0]
            pack1.append(iindices)

        datt1 = []
        for i in pack1:
            for j in i:
                datt1.append(j)
        va = []
        for i in datt1:
            if i not in va:
                va.append(i)
        valley_list = va
        fss1 = [int(x) for x in valley_list]
        seriee1 = pd.Series(fss1)
        vvle = seriee1.tolist()
        fss1.sort()
        Valley_df = df.loc[fss1]

        ###################### find max for delta temperature values ############################

        df2= temp_df
        df22 = df2.drop('Time, sec', axis=1) # drop the column name from the table
        col2 = df22.columns
        pack2 = []
        for i in col2:
            time_series2 = df2[i]
            indices2 = find_peaks(time_series2, distance=50)[0] # 50 sample points considered for finding peak
            pack2.append(indices2)

            step = []
            for val in pack2:
                for j in val:
                    step.append(j)
            #print(step)

        delta_pk = []
        for i in step:
            if i not in delta_pk:
                delta_pk.append(i)
        delta_list = delta_pk
        fss2 = [int(x) for x in delta_list]
        seriee2 = pd.Series(fss2)
        del2 = seriee2.tolist()
        fss2.sort()
        delta_df = df.loc[fss2]
        merged = fss + fss1 + fss2

        merged_data =[]
        for i in merged:
            if i not in merged_data:
                merged_data.append(i)
        screened_list = merged_data
        fss3 = [int(x) for x in screened_list]
        fss3.sort()
        print(len(fss3))
        final_list = data1.loc[fss3]

        return Response(
            final_list.to_csv(),
            mimetype="text/csv",
            headers={"Content-disposition":
                         "attachment; filename=filename.csv"})


        #return render_template('data.html', data=fss, data1=fss1, data2=fss2, screened_list = fss3)
        #return render_template('data.html', data=merged_data)
       # return render_template('valley.html', data1=temp_df.to_html())


if __name__   ==   '__main__':
    app.run(debug=True)