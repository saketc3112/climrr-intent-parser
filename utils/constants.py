from typing import Optional

# Defined globally so we can access keys for matching logic
FULL_KEY_MAP = {
    # ------------------ SIMPLE ANNUALS ------------------
    ("Heating Degree Days", "Annual", "Historical"): "hdd_hist",
    ("Heating Degree Days", "Annual", "Mid-Century RCP8.5"): "hdd_rcp85_midc",
    ("Cooling Degree Days", "Annual", "Historical"): "cdd_hist",
    ("Cooling Degree Days", "Annual", "Mid-Century RCP8.5"): "cdd_rcp85_midc",
    ("Days Without Precipitation", "Annual", "Historical"): "noprecip_hist",
    ("Days Without Precipitation", "Annual", "Mid-Century RCP4.5"): "noprecip_rcp45_midc",
    ("Days Without Precipitation", "Annual", "End-Century RCP4.5"): "noprecip_rcp45_endc",
    ("Days Without Precipitation", "Annual", "Mid-Century RCP8.5"): "noprecip_rcp85_midc",
    ("Days Without Precipitation", "Annual", "End-Century RCP8.5"): "noprecip_rcp85_endc",
    ("Annual Precipitation", "Annual", "Historical"): "precipann_hist",
    ("Annual Precipitation", "Annual", "Mid-Century RCP4.5"): "precipann_rcp45_midc",
    ("Annual Precipitation", "Annual", "End-Century RCP4.5"): "precipann_rcp45_endc",
    ("Annual Precipitation", "Annual", "Mid-Century RCP8.5"): "precipann_rcp85_midc",
    ("Annual Precipitation", "Annual", "End-Century RCP8.5"): "precipann_rcp85_endc",
    ("Wind Speed", "Annual", "Historical"): "windspeed_hist",
    ("Wind Speed", "Annual", "Mid-Century RCP4.5"): "windspeed_rcp45_midc",
    ("Wind Speed", "Annual", "End-Century RCP4.5"): "windspeed_rcp45_endc",
    ("Wind Speed", "Annual", "Mid-Century RCP8.5"): "windspeed_rcp85_midc",
    ("Wind Speed", "Annual", "End-Century RCP8.5"): "windspeed_rcp85_endc",
    
    # ------------------ TEMP MAX/MIN ------------------
    # Annual
    ("Average Maximum Temperature", "Annual", "Historical"): "tempmaxann_hist",
    ("Average Maximum Temperature", "Annual", "Mid-Century RCP4.5"): "tempmaxann_rcp45_midc",
    ("Average Maximum Temperature", "Annual", "End-Century RCP4.5"): "tempmaxann_rcp45_endc",
    ("Average Maximum Temperature", "Annual", "Mid-Century RCP8.5"): "tempmaxann_rcp85_midc",
    ("Average Maximum Temperature", "Annual", "End-Century RCP8.5"): "tempmaxann_rcp85_endc",
    ("Average Minimum Temperature", "Annual", "Historical"): "tempminann_hist",
    ("Average Minimum Temperature", "Annual", "Mid-Century RCP4.5"): "tempminann_rcp45_midc",
    ("Average Minimum Temperature", "Annual", "End-Century RCP4.5"): "tempminann_rcp45_endc",
    ("Average Minimum Temperature", "Annual", "Mid-Century RCP8.5"): "tempminann_rcp85_midc",
    ("Average Minimum Temperature", "Annual", "End-Century RCP8.5"): "tempminann_rcp85_endc",
    
    # Seasonal (Winter/Spring/Summer/Autumn)
    ("Average Maximum Temperature", "Winter", "Historical"): "tempmax_seas_hist_winter",
    ("Average Maximum Temperature", "Winter", "Mid-Century RCP8.5"): "tempmax_seas_rcp85_midc_winter",
    ("Average Maximum Temperature", "Winter", "End-Century RCP8.5"): "tempmax_seas_rcp85_endc_winter",
    ("Average Minimum Temperature", "Winter", "Historical"): "tempmin_seas_hist_winter",
    ("Average Minimum Temperature", "Winter", "Mid-Century RCP8.5"): "tempmin_seas_rcp85_midc_winter",
    ("Average Minimum Temperature", "Winter", "End-Century RCP8.5"): "tempmin_seas_rcp85_endc_winter",
    
    ("Average Maximum Temperature", "Spring", "Historical"): "tempmax_seas_hist_spring",
    ("Average Maximum Temperature", "Spring", "Mid-Century RCP8.5"): "tempmax_seas_rcp85_mid_spring",
    ("Average Maximum Temperature", "Spring", "End-Century RCP8.5"): "tempmax_seas_rcp85_end_spring",
    ("Average Minimum Temperature", "Spring", "Historical"): "tempmin_seas_hist_spring",
    ("Average Minimum Temperature", "Spring", "Mid-Century RCP8.5"): "tempmin_seas_rcp85_mid_spring",
    ("Average Minimum Temperature", "Spring", "End-Century RCP8.5"): "tempmin_seas_rcp85_end_spring",

    ("Average Maximum Temperature", "Summer", "Historical"): "tempmax_seas_hist_summer",
    ("Average Maximum Temperature", "Summer", "Mid-Century RCP8.5"): "tempmax_seas_rcp85_mid_summer",
    ("Average Maximum Temperature", "Summer", "End-Century RCP8.5"): "tempmax_seas_rcp85_end_summer",
    ("Average Minimum Temperature", "Summer", "Historical"): "tempmin_seas_hist_summer",
    ("Average Minimum Temperature", "Summer", "Mid-Century RCP8.5"): "tempmin_seas_rcp85_mid_summer",
    ("Average Minimum Temperature", "Summer", "End-Century RCP8.5"): "tempmin_seas_rcp85_end_summer",

    ("Average Maximum Temperature", "Autumn", "Historical"): "tempmax_seas_hist_autum",
    ("Average Maximum Temperature", "Autumn", "Mid-Century RCP8.5"): "tempmax_seas_rcp85_mid_autumn",
    ("Average Maximum Temperature", "Autumn", "End-Century RCP8.5"): "tempmax_seas_rcp85_end_autumn",
    ("Average Minimum Temperature", "Autumn", "Historical"): "tempmin_seas_hist_autum",
    ("Average Minimum Temperature", "Autumn", "Mid-Century RCP8.5"): "tempmin_seas_rcp85_mid_autumn",
    ("Average Minimum Temperature", "Autumn", "End-Century RCP8.5"): "tempmin_seas_rcp85_end_autumn",

    # ------------------ HEAT INDEX ------------------
    ("Daily Max Heat Index", "Annual", "Historical"): "heatindex_HIS_DayMax",
    ("Daily Max Heat Index", "Annual", "Mid-Century RCP8.5"): "heatindex_M85_DayMax",
    ("Daily Max Heat Index", "Annual", "End-Century RCP8.5"): "heatindex_E85_DayMax",
    ("Seasonal Max Heat Index", "Annual", "Historical"): "heatindex_HIS_SeaMax",
    ("Seasonal Max Heat Index", "Annual", "Mid-Century RCP8.5"): "heatindex_M85_SeaMax",
    ("Seasonal Max Heat Index", "Annual", "End-Century RCP8.5"): "heatindex_E85_SeaMax",
    ("Days with Max Heat Index Over 95", "Annual", "Historical"): "heatindex_HIS_Day95",
    ("Days with Max Heat Index Over 95", "Annual", "Mid-Century RCP8.5"): "heatindex_M85_Day95",
    ("Days with Max Heat Index Over 105", "Annual", "Historical"): "heatindex_HIS_Day105",
    ("Days with Max Heat Index Over 105", "Annual", "Mid-Century RCP8.5"): "heatindex_M85_Day105",
    
    # ------------------ FIRE WEATHER INDEX (UNIFIED) ------------------
    # Maps to the BASE PREFIX (e.g. FWIBins_HistWin). 
    # The extractor logic appends _95, _NC, or _Avg based on user query.
    
    # Annual (Added as per request)
    ("Fire Weather Index", "Annual", "Historical"): "FWIBins_Hist",
    ("Fire Weather Index", "Annual", "Mid-Century RCP8.5"): "FWIBins_Mid",
    ("Fire Weather Index", "Annual", "End-Century RCP8.5"): "FWIBins_End",

    # Winter
    ("Fire Weather Index", "Winter", "Historical"): "FWIBins_HistWin",
    ("Fire Weather Index", "Winter", "Mid-Century RCP8.5"): "FWIBins_MidWin",
    ("Fire Weather Index", "Winter", "End-Century RCP8.5"): "FWIBins_EndWin",
    
    # Spring
    ("Fire Weather Index", "Spring", "Historical"): "FWIBins_HistSpr",
    ("Fire Weather Index", "Spring", "Mid-Century RCP8.5"): "FWIBins_MidSpr",
    ("Fire Weather Index", "Spring", "End-Century RCP8.5"): "FWIBins_EndSpr",

    # Summer
    ("Fire Weather Index", "Summer", "Historical"): "FWIBins_HistSum",
    ("Fire Weather Index", "Summer", "Mid-Century RCP8.5"): "FWIBins_MidSum",
    ("Fire Weather Index", "Summer", "End-Century RCP8.5"): "FWIBins_EndSum",
    
    # Autumn
    ("Fire Weather Index", "Autumn", "Historical"): "FWIBins_HistAut",
    ("Fire Weather Index", "Autumn", "Mid-Century RCP8.5"): "FWIBins_MidAut",
    ("Fire Weather Index", "Autumn", "End-Century RCP8.5"): "FWIBins_EndAut",
}

def get_final_data_key(variable_name, seasonality, scenario_part) -> Optional[str]:
    """
    Translates the combination of (Variable Name, Seasonality, Scenario) into 
    the exact column name used in the FullData.csv.
    """
    exact_column_name = FULL_KEY_MAP.get((variable_name, seasonality, scenario_part))
    if exact_column_name:
        return exact_column_name
    return None

