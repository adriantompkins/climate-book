import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# --- New Imports ---
import cartopy.crs as ccrs
from metpy.plots import SkewT
from metpy.units import units
import metpy.calc as mpcalc
from matplotlib.widgets import Button

# --- 1. Define File Paths and URL ---
LOCAL_FILE_PATH = os.path.expanduser('./era5_pressure_data.nc')
URL = 'http://clima-dods.ictp.it/Users/tompkins/data/era5/era5_pressure_data.nc'

# --- 2. Check for local file and download if missing ---
if not os.path.exists(LOCAL_FILE_PATH):
    print(f"File not found at: {LOCAL_FILE_PATH}")
    print(f"Attempting to download from {URL} using wget...")
    
    download_dir = os.path.dirname(LOCAL_FILE_PATH)
    os.makedirs(download_dir, exist_ok=True)
    
    status = os.system(f"wget -O {LOCAL_FILE_PATH} {URL}")
    
    if status != 0:
        print(f"Error: wget command failed. Status code: {status}")
        print("Please make sure 'wget' is installed and in your system's PATH,")
        print(f"or manually download the file from the URL to {LOCAL_FILE_PATH}")
        exit()
    print("Download complete.")
else:
    print(f"Using existing local file: {LOCAL_FILE_PATH}")


# --- 3. Load and process data (now locally) ---
print("Loading data from local file...")
try:
    ds = xr.open_dataset(LOCAL_FILE_PATH)
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error opening file: {e}")
    exit()

# --- 4. Select the Time for the Interactive Plot ---
try:
    times_00z = ds.valid_time[ds.valid_time.dt.hour == 0]
    if len(times_00z) == 0:
        print("Error: No 00Z time found in the file.")
        exit()
    
    time_to_plot = times_00z.isel(valid_time=0)
    time_str = pd.to_datetime(time_to_plot.values).strftime('%Y-%m-%d %HZ')
    print(f"Set to interactive mode for time: {time_str}")

    background_field = ds['t'].sel(valid_time=time_to_plot).isel(pressure_level=0)

except Exception as e:
    print(f"Error selecting data: {e}")
    ds.close()
    exit()

# --- 5. Setup the Interactive Figure ---
print("Setting up interactive plot...")

fig = plt.figure(figsize=(10, 12))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 2], right=0.85) 

ax_map = fig.add_subplot(gs[0], projection=ccrs.PlateCarree())
skew = SkewT(fig, subplot=gs[1], rotation=45)

# --- 6. Draw the Initial Map ---
ax_map.set_title("Click on a location to plot profile")
ax_map.coastlines(color='black')
ax_map.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
ax_map.set_extent([ds.longitude.min(), ds.longitude.max(), 
                   ds.latitude.min(), ds.latitude.max()], crs=ccrs.PlateCarree())

background_field.plot.contourf(
    ax=ax_map, 
    transform=ccrs.PlateCarree(),
    cmap='coolwarm', 
    add_colorbar=False
)

# --- 7. Draw the Initial (Empty) Skew-T ---
skew.ax.set_ylim(1050, 100)
skew.ax.set_xlabel('Temperature (°C)')
skew.ax.set_ylabel('Pressure (hPa)')
skew.ax.set_title("Profile (click map to load)")

skew.plot_dry_adiabats(color='gray', linestyle='--', linewidth=1)
skew.plot_moist_adiabats(color='blue', linestyle='--', linewidth=1)
skew.plot_mixing_lines(color='green', linestyle=':', linewidth=1)

# --- 8. State variables for managing plots ---
temp_line_plots = []
dew_line_plots = []
map_markers = []
parcel_line_plots = []
profile_data_storage = []

plot_colors = plt.cm.get_cmap('tab10').colors
color_index = 0

# --- 9. Define Event Functions ---

def onclick(event):
    """Handles click events on the map."""
    global color_index, profile_data_storage
    
    if event.inaxes != ax_map:
        return

    click_lon = event.xdata
    click_lat = event.ydata
    click_lon_0_360 = click_lon % 360
    
    print(f"Clicked at: Lat={click_lat:.2f}, Lon={click_lon:.2f} (map) -> {click_lon_0_360:.2f} (data)")

    try:
        profile = ds.sel(
            latitude=click_lat, 
            longitude=click_lon_0_360, 
            valid_time=time_to_plot,
            method='nearest'
        )
        
        P = profile['pressure_level'].values * units.hPa
        T = profile['t'].values * units.kelvin
        q = profile['q'].values * units('kg/kg')
        Td = mpcalc.dewpoint_from_specific_humidity(P, T, q)
        
        mask = ~np.isnan(T.magnitude) & ~np.isnan(Td.magnitude)
        P_clean, T_clean, Td_clean = P[mask], T[mask], Td[mask]
        
        if len(P_clean) < 2:
            print("  Skipping: Not enough valid data at this point.")
            return

        actual_lat = profile.latitude.values
        actual_lon = profile.longitude.values
        color = plot_colors[color_index % len(plot_colors)]
        color_index += 1
        
        label = f"({actual_lat:.1f}N, {actual_lon:.1f}E)"
        
        temp_line = skew.plot(P_clean, T_clean, color=color, linewidth=2, label=f'T {label}')
        dew_line = skew.plot(P_clean, Td_clean, color=color, linestyle='--', linewidth=2, label=f'q {label}')
        
        temp_line_plots.append(temp_line[0])
        dew_line_plots.append(dew_line[0])
        
        new_marker = ax_map.plot(actual_lon, actual_lat, 'o', 
                                 markersize=8, color=color, 
                                 markeredgecolor='black',
                                 transform=ccrs.PlateCarree())
        map_markers.append(new_marker[0])

        profile_data_storage.append({
            'P': P_clean,
            'T': T_clean,
            'Td': Td_clean,
            'color': color
        })
        
        skew.ax.set_title(f"Profiles for {time_str}")
        if skew.ax.get_legend():
            skew.ax.get_legend().remove()
        skew.ax.legend(fontsize='small', loc='upper left', bbox_to_anchor=(0, 1))

        fig.canvas.draw_idle()

    except Exception as e:
        print(f"  Error processing click: {e}")

def clear_parcel_lines():
    """Helper function to remove only parcel lines."""
    global parcel_line_plots
    for line in parcel_line_plots:
        line.remove()
    parcel_line_plots.clear()

def plot_parcels(event):
    """Handles click events on the 'Plot Parcels' button."""
    global parcel_line_plots, profile_data_storage
    print("Plotting parcel ascents...")
    
    clear_parcel_lines()
    
    if not profile_data_storage:
        print("  No profiles to plot. Click on the map first.")
        return

    for profile in profile_data_storage:
        P = profile['P']
        T = profile['T']
        Td = profile['Td']
        color = profile['color']

        P_start, T_start, Td_start = P[0], T[0], Td[0]
        
        try:
            parcel_path = mpcalc.parcel_profile(P, T_start, Td_start)
            
            # ❗️ CHANGED: Updated linewidth from 1 to 2
            parcel_line = skew.plot(P, parcel_path, color=color, linewidth=2, linestyle=':')
            
            parcel_line_plots.append(parcel_line[0])

        except Exception as e:
            print(f"  Could not calculate parcel for profile: {e}")
    
    fig.canvas.draw_idle()


def reset_plot(event):
    """Handles click events on the 'Reset' button."""
    global color_index, profile_data_storage, parcel_line_plots
    print("Resetting Skew-T plot...")
    
    for line in temp_line_plots: line.remove()
    for line in dew_line_plots: line.remove()
    for marker in map_markers: marker.remove()
    for line in parcel_line_plots: line.remove()
        
    temp_line_plots.clear()
    dew_line_plots.clear()
    map_markers.clear()
    parcel_line_plots.clear()
    profile_data_storage.clear()
    
    color_index = 0
    
    skew.ax.set_title("Profile (click map to load)")
    if skew.ax.get_legend():
        skew.ax.get_legend().remove()
        
    fig.canvas.draw_idle()

def exit_program(event):
    """Handles click events on the 'Exit' button."""
    print("Exiting program...")
    plt.close(fig) 


# --- 10. Connect Events and Show the Plot ---

cid = fig.canvas.mpl_connect('button_release_event', onclick)

ax_button_parcels = fig.add_axes([0.87, 0.80, 0.1, 0.05]) 
button_parcels = Button(ax_button_parcels, 'Plot Parcels')
button_parcels.on_clicked(plot_parcels)

ax_button_reset = fig.add_axes([0.87, 0.73, 0.1, 0.05])
button_reset = Button(ax_button_reset, 'Reset Plot')
button_reset.on_clicked(reset_plot)

ax_button_exit = fig.add_axes([0.87, 0.66, 0.1, 0.05]) 
button_exit = Button(ax_button_exit, 'Exit Program')
button_exit.on_clicked(exit_program)


print("\n--- Interactive window is now open ---")
print("Click on the map to get started.")
plt.show()

# --- 11. Close the dataset when the plot window is closed ---
ds.close()
print("Plot window closed. Dataset closed.")



