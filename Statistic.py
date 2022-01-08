import random
from datetime import timedelta
import datetime
import math

import numpy as np
import pandas as pd

import settings


class Statistic:

    def __init__(self):
        self.filepath = settings.FILE_PATH_CSV
        self.col_names = ["looking_time", "date_time", "Layout"]
        #self.create_csv(self.filepath, self.fill_DataTable())
        _dataframe = self.get_dataframe_from_csv(self.filepath, self.col_names)
        self.dataframe = self.set_dtype_coloumns(_dataframe, self.col_names)

    def fill_DataTable(self):
        dataTable = []

        for m in range(1, 13):
            for i in self.detectDaysOfaMonth(f"2022-{m}-01"):
                for h in range(9, 21):
                    zufall = random.randint(30, 50)

                    date = datetime.datetime(year=2022, month=m, day=i, hour=h,
                                             minute=random.randint(0, 59), second=random.randint(0, 59))

                    time_1 = timedelta.total_seconds(
                        datetime.timedelta(minutes=random.randint(0, 6), seconds=random.randint(0, 59)))

                    dataTable.append((str(time_1), str(date), random.randint(1,
                                                                             4)))

        return dataTable

    def create_csv(self, file_path, logging_table):
        try:
            file = open(file_path, "a+")
            for row in logging_table:
                for i, column in enumerate(row):

                    if i < len(row) - 1:
                        file.write(f"{column}\t")
                    else:
                        file.write(f"{column}\n")
            file.close()
            return True

        except:
            return False

    def get_dataframe_from_csv(self, filepath, col_name):
        dataframe = pd.read_csv(filepath, sep='\t', header=None, names=col_name)
        return dataframe

    def set_dtype_coloumns(self, dataframe, col_name):
        df2 = dataframe.copy()
        df2[col_name[0]].astype(float)
        df2[col_name[2]].astype(int)
        df2[col_name[1]] = pd.to_datetime(dataframe[col_name[1]])
        df3 = df2.set_index([col_name[1]])

        return df3

    def getDataOfSpecificDate(self, date_time, index_dateOption, index_layout_option):

        x_axis = None
        y_axis = None

        if index_layout_option < 4:
            # Data from the selected year
            if index_dateOption == 2:
                x_axis, y_axis = self.axisYearData(date_time, index_layout_option+1)

            # Data from the selected month of the year
            elif index_dateOption == 1:
                x_axis, y_axis = self.axisMonthData(date_time, index_layout_option+1)

            # Data from the selected date for each hour
            elif index_dateOption == 0:

                x_axis, y_axis = self.axisDailyData( date_time,index_layout_option+1)


        elif index_layout_option == 4:
            x_axis, y_axis = self.compareLayouts(4)

        return x_axis, y_axis

    def axisDailyData(self, date_time,layout):

        # get values for the x- axis
        x_axis = [i for i in range(0, 23)]
        y_axis=[]

        try:
            df = self.dataframe.loc[date_time]
            dummy_df = df.dataframe[df.dataframe[self.col_names[2]] == layout]
            data = [dummy_df.between_time(f"{i}:00:00", f"{i + 1}:00:00") for i in range(0, 23)]

            for df in data:
                mean = df[self.col_names[0]].mean()
                if math.isnan(mean):
                    y_axis.append(0)
                else:
                    y_axis.append(mean)

        except:
            y_axis = [0 for i in range(0,23)]


        return x_axis, y_axis

    def axisMonthData(self, date_time, layout):

        # eperate date time in year, month, day
        y, m, d = date_time.split(sep="-")

        # get the days of the selected  month
        days = self.detectDaysOfaMonth(date_time)
        y_axis = []

        for day in days:

            try:
                # select the dataframe
                data_frame = self.dataframe[self.dataframe[self.col_names[2]] == layout]
                dummy_df = data_frame.loc[f"{y}-{m}-{day}"]
                mean = dummy_df[self.col_names[0]].mean()

                if math.isnan(mean):
                    y_axis += [0]
                else:
                    y_axis += [mean]

            except:
                y_axis += [0]


        return days, y_axis

    def axisYearData(self, date_time, layout):

        # seperate date time in year, month, day
        y, m, d = date_time.split(sep="-")
        months = [i for i in range(1, 13)]
        y_axis = []

        for month in months:

            try:
                # select the dataframe
                data_frame = self.dataframe[self.dataframe[self.col_names[2]] == layout]
                dummy_df = data_frame.loc[f"{y}-{month}"]
                mean = dummy_df[self.col_names[0]].mean()
                if math.isnan(mean):
                    y_axis += [0]
                else:
                    y_axis += [mean]

            except:
                y_axis += [0]

        return months, y_axis

    def detectDaysOfaMonth(self, date_time):
        y, m, d = date_time.split(sep="-")
        date = datetime.datetime(int(y), int(m), 1)
        day_numbers = []

        for i in range(0, 32):
            dummy_date = date + datetime.timedelta(days=i)
            if date.month != dummy_date.month:
                break
            day_numbers += [i + 1]

        return day_numbers

    def compareLayouts(self, number_of_Layouts):

        x_axis = [i for i in range(1, number_of_Layouts + 1)]
        y_axis = []

        for layout in x_axis:
            dummy_df = self.dataframe[self.dataframe[self.col_names[2]] == layout]
            mean = dummy_df[self.col_names[0]].mean()

            if math.isnan(mean):
                y_axis += [0]
            else:
                y_axis += [mean]

        return x_axis, y_axis
