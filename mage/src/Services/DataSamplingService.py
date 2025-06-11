import random
from mage.src.Utils.data_utils import empty_data_from_keys
import numpy as np

class DataSamplingService:

    def sample_sequential(data, segmentation):
        category, size = DataSamplingService.parse_segmentation(segmentation)
        samples = []
        start = 0
        end = 0


        while(start < len(data['timestamp'])):
            
            if category == 'M':
                end = DataSamplingService.sample_months(data, start, size)
                subset = DataSamplingService.build_set(data, start, end)
                samples.append(subset)

            elif category == 'Y':
                end = DataSamplingService.sample_years(data, start, size)
                subset = DataSamplingService.build_set(data, start, end)
                samples.append(subset)

            start = end

        return samples

    def sample_random(data, segmentation, total_samples):

        category, size = DataSamplingService.parse_segmentation(segmentation)
        samples = []

        for i in range(0, total_samples):
            random_pick = random.randint(0, len(data['timestamp']) - 1)

            if category == 'M':
                start = DataSamplingService.find_month_start(data, random_pick)
                end = DataSamplingService.sample_months(data, start, size)
                subset = DataSamplingService.build_set(data, start, end)
                samples.append(subset)

            elif category == 'Y':
                start = DataSamplingService.find_year_start(data, random_pick)
                end = DataSamplingService.sample_years(data, start, size)
                subset = DataSamplingService.build_set(data, start, end)
                samples.append(subset)

        return samples

    def parse_segmentation(segmentation):
        return segmentation[-1], int(segmentation[:-1])

    def sample_days(data, start, years):
        curr_year = data['timestamp'][0].day
        year_count = 0

        for i in range(start, len(data['timestamp'])):
            ts = data['timestamp'][i]
            if ts.year != curr_year:
                month_count = month_count + 1

            if year_count == years:
                return i
            
    def sample_months(data, start, months):
        curr_month = data['timestamp'][start].month
        month_count = 0

        for i in range(start, len(data['timestamp'])):
            ts = data['timestamp'][i]
            if ts.month != curr_month:
                month_count = month_count + 1
                curr_month = ts.month

            if month_count == months:
                return i
        return i

    def sample_years(data, start, years):
        curr_year = data['timestamp'][start].year
        year_count = 0

        for i in range(start, len(data['timestamp'])):
            ts = data['timestamp'][i]
            if ts.year != curr_year:
                year_count = year_count + 1
                curr_year = ts.year

            if year_count == years:
                return i
        return i
    
    def find_month_start(data, start):
        start_month = data['timestamp'][start].month

        for i in range(start, 0, -1):
            ts = data['timestamp'][i]

            if ts.month != start_month:
                return i + 1
            
        return 0
            
    def find_year_start(data, start):
        start_year = data['timestamp'][start].year

        for i in range(start, 0, step=-1):
            ts = data['timestamp'][i]

            if ts.year != start_year:
                return i + 1
                
    def build_set(data, start, end):
        new_data = empty_data_from_keys(data)
        for i in range(start, end):
            for key in data:
                if isinstance(data[key], dict):
                    for k in data[key]:
                        new_data[key][k] = np.append(new_data[key][k], data[key][k][i])
                else:
                    new_data[key] = np.append(new_data[key], data[key][i])
        return new_data
    

