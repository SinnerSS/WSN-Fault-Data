import os
import xarray as xr
import pandas as pd

start_date = pd.to_datetime('2023-01-01')
end_date = pd.to_datetime('2023-12-31')
dates = pd.date_range(start=start_date, end=end_date, freq='D')

area = {'0': [100, 15], '1': [-70, -5], '2': [5, 20], '3': [-30, 65], '4': [95, 55]}

temp_data = {f'{code}_{i}' : [] for code in area for i in range(5)}
time_data = []  

for code, coords in area.items():
    time_data = []      
    point_coords = {}

    i = 5
    for offset_lon in range(0, 3, 2):
        for offset_lat in range(0, 3, 2):
            i -= 1
            point_coords[i] = (coords[0]+offset_lon, coords[1]+offset_lat)
    point_coords[0] = (coords[0]+1, coords[1]+1)  

    for date in dates:
        file_name = f'M2I1NXASM.5.12.4:MERRA2_400.inst1_2d_asm_Nx.{date.strftime("%Y%m%d")}.nc4.nc4'
        file_path = f'./raw/hour/area{code}/' + file_name 

        if(os.path.exists(file_path)):
            ds = xr.open_dataset(file_path)

            timestamps = ds['time'].values
            time_data.extend(timestamps)
            
            i=5
            for offset_lon in range(0, 11, 10):
                for offset_lat in range(0, 11, 10):
                    i-=1
                    t2m = ds['T2M'].sel(lon=coords[0]+offset_lon, lat=coords[1]+offset_lat, method="nearest")
                    temp_data[f'{code}_{i}'].extend(t2m.values)

            t2m = ds['T2M'].sel(lon=coords[0]+5, lat=coords[1]+5, method="nearest")
            temp_data[f'{code}_0'].extend(t2m.values)

            ds.close()

        else:
            i=5
            for offset_lon in range(0, 11, 10):
                for offset_lat in range(0, 11, 10):
                    i-=1
                    temp_data[f'{code}_{i}'].extend([float('nan')]*24)

            timestamps = pd.date_range(start=date, periods=24, freq="H")
            time_data.extend(timestamps)

    file_path = f'./data/hour/area{code}/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    
    for i in range(5):
        lon, lat = point_coords[i]
        print(f"Area {code}_{i} (lon={lon}, lat={lat}):")
        print(f"Time length: {len(time_data)}")
        print(f"Temperature length: {len(temp_data[f'{code}_{i}'])}")
        
        df = pd.DataFrame({
            "time": time_data,
            "t2m": temp_data[f'{code}_{i}'],
            "longitude": lon,
            "latitude": lat
        })
        filename = f"area{code}_lon{lon}_lat{lat}.csv"
        df.to_csv(file_path + filename, index=False)
