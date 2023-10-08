from django.shortcuts import render
from django.db import connection
import pandas as pd
from .forms import ExcelUploadForm
from .models import combine_reports
import openpyxl

# Create your views here.

def index(request):
    if request.method == 'POST':
        df_to_Dataset = combine_reports()
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file, na_filter=False)  #Replace NaN with empty String -> ' '

            def remove_chars(column_name):
                return column_name.replace('VP: ', '')

            df.rename(columns=remove_chars, inplace=True) #Remove leading 'VP:' from header row

            row_num_start = 0
            row_num_end = df.index.stop

            df['Failure Long Text'] = df.loc[row_num_start:row_num_end, 'long text failure1'].astype(str) + df.loc[row_num_start:row_num_end, 'long text failure2'].astype(str) + \
                                      df.loc[row_num_start:row_num_end, 'long text failur3'].astype(str) + df.loc[row_num_start:row_num_end, 'long text failur4'].astype(str) + \
                                      df.loc[row_num_start:row_num_end, 'long text failur5'].astype(str) + df.loc[row_num_start:row_num_end, 'long text failur6'].astype(str)

            df['Diagnose Long Text'] = df.loc[row_num_start:row_num_end, 'long text diag1'] + df.loc[row_num_start:row_num_end, 'long text diag2'] + \
                                                   df.loc[row_num_start:row_num_end, 'long text diag3'] + df.loc[row_num_start:row_num_end, 'long text diag4'] + \
                                                   df.loc[row_num_start:row_num_end, 'long text diag5'] + df.loc[row_num_start:row_num_end, 'long text diag6']

            df['Remedy Long Text'] = df.loc[row_num_start:row_num_end, 'long text remedy1'] + df.loc[row_num_start:row_num_end, 'long text remedy2'] +\
                                             df.loc[row_num_start:row_num_end, 'long text remedy3'] + df.loc[row_num_start:row_num_end, 'long text remedy4'] + \
                                             df.loc[row_num_start:row_num_end, 'long text remedy5'] + df.loc[row_num_start:row_num_end, 'long text remedy6']

            df['Reason Long Text'] = df.loc[row_num_start:row_num_end, 'long text reason1'] + df.loc[row_num_start:row_num_end, 'long text reason2'] + \
                                         df.loc[row_num_start:row_num_end, 'long text reason3'] + df.loc[row_num_start:row_num_end, 'long text reason5'] + \
                                         df.loc[row_num_start:row_num_end, 'long text reason6']

            df['Comment Long Text'] = df.loc[row_num_start:row_num_end, 'long text com.1'] + df.loc[row_num_start:row_num_end, 'long text com.2'] + \
                                          df.loc[row_num_start:row_num_end, 'long text com.3']

            df['Comment extension Text'] = df.loc[row_num_start:row_num_end, 'long text ext. Com.1'] + df.loc[row_num_start:row_num_end, 'long text ext. Com.2'] + \
                                               df.loc[row_num_start:row_num_end, 'long text ext. Com.3']

            columns_to_remove = ['long text failure1', 'long text failure2','long text failur3','long text failur4','long text failur5','long text failur6','long text diag1',
                                 'long text diag2','long text diag3','long text diag4','long text diag5','long text diag6', 'long text remedy1', 'long text remedy2', 'long text remedy3',
                                 'long text remedy4', 'long text remedy5', 'long text remedy6', 'long text reason1', 'long text reason2', 'long text reason3',
                                 'long text reason5', 'long text reason6', 'long text com.1', 'long text com.2', 'long text com.3', 'long text ext. Com.1', 'long text ext. Com.2', 'long text ext. Com.3']

            df_filtered = df.drop(columns=columns_to_remove)

            new_column_order = ['Report', 'Machine number',  'Operating hours of machine', 'Picture report flag' , '1st use day date', 'Failure date',  'Repair date', 'BGZ- master struct',
            'Material number main failure par',  'System text', 'Text harvet',  'Text harvest conditions',  'Text failure code',  'Failure Long Text', 'Diagnose Long Text', 'Remedy Long Text',
                                'Reason Long Text', 'Comment Long Text', 'Comment extension Text', 'long text extra t1', 'long text man.tim1']

            df_rearranged = df_filtered[new_column_order]

            df_rearranged.loc[:, '1st use day date'] = pd.to_datetime(df_rearranged['1st use day date'], format='%d %m %y')
            df_rearranged.loc[:, '1st use day date'] = df_rearranged['1st use day date'].dt.strftime('%Y-%m-%d')

            df_rearranged.loc[:, 'Failure date'] = pd.to_datetime(df_rearranged['Failure date'], format='%d %m %y')
            df_rearranged.loc[:, 'Failure date'] = df_rearranged['Failure date'].dt.strftime('%Y-%m-%d')

            df_rearranged.loc[:, 'Repair date'] = pd.to_datetime(df_rearranged['Repair date'], format='%d %m %y')
            df_rearranged.loc[:, 'Repair date'] = df_rearranged['Repair date'].dt.strftime('%Y-%m-%d')

            df_rearranged= df_rearranged.iloc[0:]

            for index, row in df_rearranged.iloc[0:].iterrows():
                value = combine_reports(
                    report=row[0],
                    machine=row[1],
                    hours=row[2],
                    image=row[3],
                    report_date=row[4],
                    failure_date=row[5],
                    repair_date=row[6],
                    bgz_master=row[7],
                    part_number=row[8],
                    system_text=row[9],
                    harvest_text=row[10],
                    failure_code=row[11],
                    failure_long_text=row[12],
                    failure_diagnose_text=row[13],
                    remedy_text=row[14],
                    reason_text=row[15],
                    comment_text=row[16],
                    comment_ext_text=row[17],
                    long_text_extra=row[18],
                    repair_long_text=row[19]
                )
                value.save()


            table_data = df_rearranged.to_dict('records')  #Prepare for Table view
            return render(request,  'fieldreports_view/index.html',  {'table_data': table_data})

    else:
        form = ExcelUploadForm()

    return render(request, 'fieldreports_view/index.html',  {'form': form})