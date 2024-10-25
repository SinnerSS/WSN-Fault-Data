import os
import gc
import xarray as xr
import pandas as pd

start_date = pd.to_datetime('2023-01-01')
end_date = pd.to_datetime('2023-12-31')
dates_hour = pd.date_range(start=start_date, end=end_date, freq='d')

start_date = pd.to_datetime('2019-01-01')
dates_day = pd.date_range(start=start_date, end=end_date, freq='d')

area = {'0': [104, 19], '1': [-66, -1], '2': [9, 24], '3': [-26, 69], '4': [99, 59]}

for code, coords in area.items():
    gc.collect()
    time_data = []      
    temp_data = [[] for _ in range(5)]
    point_coords = [(0,0)] * 5

    i = 5
    for offset_lon in range(0, 3, 2):
        for offset_lat in range(0, 3, 2):
            i -= 1
            point_coords[i] = (coords[0]+offset_lon, coords[1]+offset_lat)
    point_coords[0] = (coords[0]+1, coords[1]+1)  

    for date in dates_hour:
        file_name = f'M2I1NXASM.5.12.4:MERRA2_400.inst1_2d_asm_Nx.{date.strftime("%Y%m%d")}.nc4.nc4'
        file_path = f'./raw/hour/area{code}/' + file_name 

        if(os.path.exists(file_path)):
            ds = xr.open_dataset(file_path)

            timestamps = ds['time'].values
            time_data.extend(timestamps)
            
            i=5
            for coord in point_coords:
                i-=1
                t2m = ds['T2M'].sel(lon=coord[0], lat=coord[1], method="nearest")
                temp_data[i].extend(t2m.values)

            ds.close()

        else:
            print(file_path + " not found!")
            i=5
            for coord in point_coords:
                i-=1
                temp_data[i].extend([float('nan')]*24)

            timestamps = pd.date_range(start=date, periods=24, freq="h")
            time_data.extend(timestamps)

    file_path = f'./data/hour/area{code}/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    for i in range(5):
        lon, lat = point_coords[i]
        print(f"Area {code}_{i} (lon={lon}, lat={lat}):")
        print(f"Time length: {len(time_data)}")
        print(f"Temperature length: {len(temp_data[i])}")
        
        df = pd.DataFrame({
            "time": time_data,
            "t2m": temp_data[i],
            "longitude": lon,
            "latitude": lat
        })
        filename = f"area{code}_lon{lon}_lat{lat}.csv"
        df.to_csv(file_path + filename, index=False)

    time_data = []
    temp_data = [[] for _ in range(5)]

    for date in dates_day:
        file_name = f'MERRA2_400.statD_2d_slv_Nx.{date.strftime("%Y%m%d")}.nc4.nc4'
        file_path = f'./raw/day/area{code}/' + file_name
        
        if(os.path.exists(file_path)):
            ds = xr.open_dataset(file_path)

            timestamps = ds['time'].values
            time_data.extend(timestamps)
            
            i=5
            for coord in point_coords:
                i-=1
                t2m = ds['T2MMEAN'].sel(lon=coord[0], lat=coord[1], method="nearest")
                temp_data[i].extend(t2m.values)

            ds.close()

        else:
            print(file_path + " not found!")
            i=5
            for coord in point_coords:
                i-=1
                temp_data[i].extend([float('nan')])

            timestamps = pd.date_range(start=date, periods=1, freq="d")
            time_data.extend(timestamps)

    file_path = f'./data/day/area{code}/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    for i in range(5):
        lon, lat = point_coords[i]
        print(f"Area {code}_{i} (lon={lon}, lat={lat}):")
        print(f"Time length: {len(time_data)}")
        print(f"Temperature length: {len(temp_data[i])}")
        
        df = pd.DataFrame({
            "time": time_data,
            "t2m": temp_data[i],
            "longitude": lon,
            "latitude": lat
        })
        filename = f"area{code}_lon{lon}_lat{lat}.csv"
        df.to_csv(file_path + filename, index=False)
