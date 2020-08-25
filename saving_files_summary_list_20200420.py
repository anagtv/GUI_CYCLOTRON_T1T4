import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
import os
from tkinter import *
from pandas import ExcelWriter
plt.rcParams.update({'font.size': 16})
plt.rcParams["figure.figsize"] = (15,10)
import sys
sys.path.append("/Users/anagtv/Desktop/Cyclotron_python")
sys.path.append("/Users/anagtv/Documents/Beta-Beat.src-master")
#from tfs_files import tfs_pandas
from mpl_interaction import figure_pz
import matplotlib.pyplot as plt
import tfs
import datetime
from datetime import timedelta
import matplotlib.dates as md
from matplotlib.widgets import CheckButtons


COLORS = ['#1E90FF','#FF4500','#32CD32',"#6A5ACD","#20B2AA","#00008B","#A52A2A","#228B22"]
COLUMNS_SOURCE = ["FILE","DATE","TARGET","FOIL","CURRENT_MAX", "CURRENT_MIN","CURRENT_AVE","CURRENT_STD","VOLTAGE_MAX","VOLTAGE_MIN","VOLTAGE_AVE","VOLTAGE_STD","HFLOW",
    "RATIO_MAX", "RATIO_MIN","RATIO_AVE","RATIO_STD","SOURCE_PERFORMANCE"]
COLUMNS_VACUUM = ["FILE","DATE","TARGET","FOIL","PRESSURE_MAX","PRESSURE_MIN","PRESSURE_AVE","PRESSURE_STD"]
COLUMNS_MAGNET = ["FILE","DATE","TARGET","FOIL","CURRENT_MAX","CURRENT_MIN","CURRENT_AVE","CURRENT_STD"]
COLUMNS_RF =  ["FILE","DATE","TARGET","FOIL","DEE1_VOLTAGE_MAX","DEE1_VOLTAGE_MIN","DEE1_VOLTAGE_AVE","DEE1_VOLTAGE_STD","DEE2_VOLTAGE_MAX","DEE2_VOLTAGE_MIN","DEE2_VOLTAGE_AVE","DEE2_VOLTAGE_STD",
    "FORWARD_POWER_MAX","FORWARD_POWER_MIN","FORWARD_POWER_AVE","FORWARD_POWER_STD","REFLECTED_POWER_MAX","REFLECTED_POWER_MIN","REFLECTED_POWER_AVE","REFLECTED_POWER_STD",
    "PHASE_LOAD_MAX","PHASE_LOAD_MIN","PHASE_LOAD_AVE","PHASE_LOAD_STD",
    "FLAP1_MAX","FLAP1_MIN","FLAP1_AVE","FLAP1_STD","FLAP2_MAX","FLAP2_MIN","FLAP2_AVE","FLAP2_STD",]
COLUMNS_BEAM = ["FILE","DATE","TARGET","FOIL","COLL_CURRENT_L_MAX","COLL_CURRENT_L_MIN","COLL_CURRENT_L_AVE","COLL_CURRENT_L_STD","COLL_CURRENT_R_MAX","COLL_CURRENT_R_MIN","COLL_CURRENT_R_AVE","COLL_CURRENT_R_STD"
    ,"RELATIVE_COLL_CURRENT_L_MAX","RELATIVE_COLL_CURRENT_L_MIN","RELATIVE_COLL_CURRENT_L_AVE","RELATIVE_COLL_CURRENT_L_STD",
    "RELATIVE_COLL_CURRENT_R_MAX","RELATIVE_COLL_CURRENT_R_MIN","RELATIVE_COLL_CURRENT_R_AVE","RELATIVE_COLL_CURRENT_R_STD",
    "TARGET_CURRENT_MAX","TARGET_CURRENT_MIN","TARGET_CURRENT_AVE","TARGET_CURRENT_STD","FOIL_CURRENT_MAX","FOIL_CURRENT_MIN","FOIL_CURRENT_AVE","FOIL_CURRENT_STD",
    "RELATIVE_TARGET_CURRENT_MAX","RELATIVE_TARGET_CURRENT_MIN","RELATIVE_TARGET_CURRENT_AVE","RELATIVE_TARGET_CURRENT_STD",
    "EXTRACTION_LOSSES_MAX","EXTRACTION_LOSSES_MIN","EXTRACTION_LOSSES_AVE","EXTRACTION_LOSSES_STD"]
COLUMNS_EXTRACTION = ["FILE","DATE","TARGET","FOIL","CAROUSEL_POSITION_MAX","CAROUSEL_POSITION_MIN","CAROUSEL_POSITION_AVE","CAROUSEL_POSITION_STD"
    ,"BALANCE_POSITION_MAX","BALANCE_POSITION_MIN","BALANCE_POSITION_AVE","BALANCE_POSITION_STD"]
COLUMNS_TRANSMISSION = ["FILE","DATE","TARGET","TRANSMISSION","FOIL"]

def _parse_args():
    parser = OptionParser()
    parser.add_option("-i", "--input",
                    help="Input measurement path",
                    metavar="INPUT", dest="input_path")
    parser.add_option("-o", "--output",
                    help="Output measurement path",
                    metavar="OUTPUT", dest="output_path")
    parser.add_option("-c", "--current",
                    help="Target current",
                    metavar="TCURRENT", dest="target_current")
    options, _ = parser.parse_args()
    return options.input_path,options.output_path,options.target_current

def get_data_tuple(path_file):
    all_parts = []
    logfile = open(path_file,"r")
    print ("path")
    print (path_file)
    for line in logfile:
         parts = line.split()
         all_parts.append(
            parts)
    target_number = (np.array(all_parts[0])[1])
    date_stamp = (np.array(all_parts[0])[8])
    if len(np.array(all_parts[0])) == 10: 
        #print ("HEREEEEE")
        date_stamp = (np.array(all_parts[0])[8] + "0" + np.array(all_parts[0])[9] )
        #print (date_stamp)
    #print ("DATEEEEEEEEE")
    #print (len((np.array(all_parts[0]))))
    #print ((np.array(all_parts[0])))
    #print (date_stamp)
    real_values = all_parts[4:]
    return real_values,target_number,date_stamp 

def get_data(real_values):
    #print ("real values here")
    #print (real_values[0])
    data_df = pd.DataFrame.from_records(real_values)
    #print (data_df)
    column_names = ["Time","Arc_I","Arc_V","Gas_flow","Dee_1_kV","Dee_2_kV","Magnet_I","Foil_I","Coll_l_I","Target_I","Coll_r_I","Vacuum_P","Target_P","Delta_Dee_kV","Phase_load","Dee_ref_V","Probe_I","He_cool_P","Flap1_pos","Flap2_pos","Step_pos","Extr_pos","Balance","RF_fwd_W","RF_refl_W","Foil_No"]
    column_names_nf = ["Time","Arc_I","Arc_V","Gas_flow","Dee_1_kV","Dee_2_kV","Magnet_I","Foil_I","Coll_l_I","Target_I","Coll_r_I","Vacuum_P","Target_P","Delta_Dee_kV","Phase_load","Dee_ref_V","Probe_I","He_cool_P","Flap1_pos","Flap2_pos","Step_pos","Extr_pos","Balance","RF_fwd_W","RF_refl_W"]
    try:
       data_df = data_df.drop([0,1,2], axis=0)
    except:
       data_df = data_df.drop([0],axis=0)
    try: 
       data_df.columns = column_names
    except:
       data_df.columns = column_names_nf 
    return data_df

def get_time(excel_data_df,current):
    #print (excel_data_df)
    time = excel_data_df.Time[excel_data_df['Target_I'].astype(float) > float(current)]
    relative_time = time 
    return time


def get_transmission(df_isochronism,probe_current,df_subsystem_source,file,target_number,date_stamp,df_transmission):
    foil_current_max_isochronism = np.max(df_isochronism.Foil_I)/probe_current
    transmission = foil_current_max_isochronism*100
    print ("ISOCHRONISMMM")
    print (df_isochronism)
    print (df_isochronism.Foil_I)
    print (np.max(df_isochronism.Foil_I))
    print (foil_current_max_isochronism)
    print (probe_current)
    print ("TRANSMISSION")
    print (transmission)
    foil_number = np.average(df_subsystem_source.Foil_No)
    transmission_list = [[np.float(file),date_stamp,target_number,transmission,foil_number]] 
    print (transmission_list)
    df_transmission_i = pd.DataFrame((transmission_list),columns=COLUMNS_TRANSMISSION)      
    df_transmission = df_transmission.append(df_transmission_i,ignore_index=True)
    return df_transmission
 

def get_isochronism(data_df):
    maximum_value = float(max(data_df.Magnet_I))
    minimum_value = float(min(data_df.Magnet_I))
    maximum_value_str = str(maximum_value)
    minimum_value_str = str(minimum_value)
    intial_index = data_df.Magnet_I[data_df.Magnet_I == minimum_value_str].index[0]
    final_index = data_df.Magnet_I[data_df.Magnet_I == maximum_value_str].index[0]
    magnet_current = data_df.Magnet_I.loc[intial_index:final_index].astype(float)
    coll_current_l = data_df.Coll_l_I.loc[intial_index:final_index].astype(float)
    coll_current_r = data_df.Coll_r_I.loc[intial_index:final_index].astype(float)
    target_current = data_df.Target_I.loc[intial_index:final_index].astype(float)
    foil_current = data_df.Foil_I.loc[intial_index:final_index].astype(float)
    df_column_isochronism = ["Magnet_I","Foil_I","Coll_l_I","Target_I","Coll_r_I"]
    df_subsystem_values_beam = [magnet_current,foil_current,coll_current_l,target_current,coll_current_r]
    df_isochronism = pd.concat(df_subsystem_values_beam,axis=1,keys=df_column_isochronism)
    return df_isochronism


def get_ion_source_performance(data_df):
    maximum_value = float(max(data_df.Magnet_I))
    minimum_value = float(min(data_df.Magnet_I))
    maximum_value_str = str(maximum_value)
    minimum_value_str = str(minimum_value)
    intial_index = data_df.Magnet_I[data_df.Magnet_I == minimum_value_str].index[0] - 3
    probe_current = float(data_df.Probe_I[intial_index])
    if probe_current == 0.0:
        intial_index = intial_index - 2
        probe_current = float(data_df.Probe_I[intial_index])
    ion_source_current = float(data_df.Arc_I[intial_index])   
    source_performance = (float(probe_current)/float(ion_source_current))
    df_column_ion_source_performance = ["Ion_source_I","Probe_stable_I","Source_performance"]
    subsystem_source_performance = [ion_source_current,probe_current,source_performance]
    print ("SOURCE PERFORMANCE!!!!!!!")
    print (subsystem_source_performance)
    print (minimum_value_str,maximum_value_str)
    return probe_current,ion_source_current,source_performance

def get_foil_number(excel_data_df,current):
    foil_number = excel_data_df.Foil_No[excel_data_df['Target_I'].astype(float) > float(current)].astype(int)
    return foil_number

def get_collimator_parameters(excel_data_df,current):
    collimator_r = excel_data_df.Coll_r_I[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    collimator_l = excel_data_df.Coll_l_I[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return collimator_r,collimator_l

def get_source_parameters(excel_data_df,current):
    source_voltage = excel_data_df.Arc_V[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    gas_flow = excel_data_df.Gas_flow[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    source_current = excel_data_df.Arc_I[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return source_voltage,source_current,gas_flow

def get_rf_parameters(excel_data_df,current):
    dee2_voltage = excel_data_df.Dee_2_kV[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    dee1_voltage = excel_data_df.Dee_1_kV[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return dee1_voltage,dee2_voltage

def get_rf_parameters_power(excel_data_df,current):
    forwarded_power = excel_data_df.RF_fwd_W[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    reflected_power = excel_data_df.RF_refl_W[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    phase_load = excel_data_df.Phase_load[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return forwarded_power,reflected_power,phase_load

def get_rf_parameters_sparks(excel_data_df,source_current):
    dee2_voltage = excel_data_df.Dee_2_kV[excel_data_df['Arc_I'].astype(float) > float(source_current)].astype(float)
    dee1_voltage = excel_data_df.Dee_1_kV[excel_data_df['Arc_I'].astype(float) > float(source_current)].astype(float)
    return dee1_voltage,dee2_voltage

def get_rf_parameters_power_sparks(excel_data_df,source_current):
    forwarded_power = excel_data_df.RF_fwd_W[excel_data_df['Arc_I'].astype(float) > float(source_current)].astype(float)
    reflected_power = excel_data_df.RF_refl_W[excel_data_df['Arc_I'].astype(float) > float(source_current)].astype(float)
    phase_load = excel_data_df.Phase_load[excel_data_df['Arc_I'].astype(float) > float(source_current)].astype(float)
    return forwarded_power,reflected_power,phase_load

def get_rf_parameters_flaps_sparks(excel_data_df,source_current):
    Flap1_pos = excel_data_df.Flap1_pos[excel_data_df['Arc_I'].astype(float) > float(source_current)].astype(float)
    Flap2_pos = excel_data_df.Flap2_pos[excel_data_df['Arc_I'].astype(float) > float(source_current)].astype(float)
    return Flap1_pos,Flap2_pos

def get_rf_parameters_flaps(excel_data_df,current):
    Flap1_pos = excel_data_df.Flap1_pos[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    Flap2_pos = excel_data_df.Flap2_pos[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return Flap1_pos,Flap2_pos

def get_magnet_parameters(excel_data_df,current):
    magnet_current = excel_data_df.Magnet_I[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return magnet_current

def get_target_pressure(excel_data_df,current):
    target_pressure = excel_data_df.Target_P[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return target_pressure

def get_target_parameters(excel_data_df):
    max_current = 0.9*(np.max(excel_data_df['Target_I'].astype(float)))
    #print ("MAX CURRENT HEREEEE")
    #print (max_current)
    #print ("numpy values")
    #print (np.array(excel_data_df.Target_I).astype(np.float))
    #print (np.max(np.array(excel_data_df.Target_I).astype(np.float)))
    target_current = excel_data_df.Target_I[excel_data_df['Target_I'].astype(float) > float(max_current)].astype(float)
    return target_current,max_current


def get_source_parameters_limit(excel_data_df):
    max_source_current = 0.05*(np.max(excel_data_df['Arc_I'].astype(float)))
    #print ("GETTING SOURCE CURRENT")
    #print (max_source_current)
    return max_source_current

def get_extraction_parameters(excel_data_df,current):
    extraction_current = excel_data_df.Foil_I[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return extraction_current

def get_extraction_parameters_position(excel_data_df,current):
    carousel_position = excel_data_df.Extr_pos[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    balance_position = excel_data_df.Balance[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return carousel_position,balance_position

def get_vacuum_parameters(excel_data_df,current):
    vacuum_level = excel_data_df.Vacuum_P[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return vacuum_level

def get_plots_three_functions_area(self,data_df,time,ylabel,pn):
    time_list = (list(range(len(time))))
    x = range(len(self.df_subsystem_beam_selected.Foil_I))
    y1 = [data_df.Coll_l_I + data_df.Coll_l_I]
    y2 = [data_df.Target_I]
    y3 = [data_df.Foil_I]
    self.sc1.axes[pn].fill_between(x,0,np.array(y3)[0],label= "Fo")
    self.sc1.axes[pn].fill_between(x,0,np.array(y2)[0],label= "Target")
    self.sc1.axes[pn].fill_between(x,0,np.array(y1)[0],label= "Collimators")
    self.sc1.axes[pn].legend(loc='best',ncol=1,fontsize=10)
    self.sc1.axes[pn].set_xlabel("Time [s]",fontsize=10)
    self.sc1.axes[pn].set_ylabel(str(ylabel))
    ticks_to_use = time[::int(len(time)/6)]   
    ticks_to_use_list = time_list[::int(len(time)/6)] 
    self.sc1.axes[pn].set_xticks(ticks_to_use_list)
    self.sc1.axes[pn].set_xticklabels(ticks_to_use)
    #self.sc1.axes[pn].set_yticks(np.arange(min_value,max_value*1.1, step=5))
    self.sc1.axes[pn].tick_params(labelsize=10)

def get_plots_two_functions_source(self,function_horizontal,function1_vertical,function2_vertical,label1,label2,ylabel,xlabel,pn):
    function_horizontal_list = (list(range(len(function_horizontal))))
    #print ("HEREEEEEE")
    #print (function_horizontal)
    #print (np.max(function_horizontal))
    #print (function1_vertical)
    #print (function2_vertical)
    self.sc4.axes[pn].errorbar(function_horizontal,function1_vertical,label=label1,picker=5,fmt="o")
    self.sc4.axes[pn+1].errorbar(function_horizontal,function2_vertical,label=label2,picker=5,fmt="o")
    self.sc4.axes[pn].legend(loc='best',ncol=5,fontsize=10)
    self.sc4.axes[pn+1].legend(loc='best',ncol=5,fontsize=10)
    self.sc4.axes[pn].set_xlabel(str(xlabel),fontsize=10)
    self.sc4.axes[pn].set_xlim([0,10])
    self.sc4.axes[pn].set_ylabel(str(ylabel),fontsize=10)
    self.sc4.axes[pn+1].set_xlabel(str(xlabel),fontsize=10)
    self.sc4.axes[pn+1].set_xlim([0,10])
    self.sc4.axes[pn+1].set_ylabel(str(ylabel),fontsize=10)
    max_function1 = (float(np.max(function1_vertical)))
    min_function1 = (float(np.min(function1_vertical)))
    max_function2 = (float(np.max(function2_vertical)))
    min_function2 = (float(np.min(function2_vertical)))
    max_value = np.max([max_function1,max_function2])
    min_value = np.max([min_function1,min_function2])
    #ticks_to_use = function_horizontal[::int(len(function_horizontal)/6)]   
    #ticks_to_use_list = function_horizontal[::int(len(function_horizontal)/6)] 
    #self.sc4.axes[pn].set_xticks(ticks_to_use_list)
    #self.sc4.axes[pn].set_xticklabels(ticks_to_use)
    #self.sc1.axes[pn].set_yticks(np.arange(min_value,max_value*1.1, step=5))
    #self.sc4.axes[pn].tick_params(labelsize=10)

def get_plots_one_functions_source(self,function_horizontal,function1_vertical,ylabel,xlabel,pn):
    function_horizontal_list = (list(range(len(function_horizontal))))
    self.sc4.axes[pn].errorbar(function_horizontal,function1_vertical,fmt="o",picker=5)
    print ("HORIZONTAL FUNCTION")
    print (function_horizontal)
    print ("VERTICAL FUNCTION")
    print (function1_vertical)
    self.sc4.axes[pn].set_ylabel(str(ylabel),fontsize=10)
    self.sc4.axes[pn].set_xlabel(str(xlabel),fontsize=10)
    max_value = (float(np.max(function1_vertical)))
    min_value = (float(np.min(function1_vertical)))
    print (min(function_horizontal))
    print (max(function_horizontal))
    self.sc4.axes[pn].set_xlim([0.95*min(function_horizontal),1.01*max(function_horizontal)])
    self.sc4.axes[pn].tick_params(labelsize=10)

def get_plots_two_functions_all(self,function1,function2,time,label1,label2,ylabel,pn):
    time_list = (list(range(len(time))))
    self.sc1.axes[pn].plot(time_list,function1,label=label1,picker=5)
    self.sc1.axes[pn].plot(time_list,function2,label=label2,picker=5)
    self.sc1.axes[pn].legend(loc='best',ncol=5,fontsize=10)
    self.sc1.axes[pn].set_xlabel("Time [s]",fontsize=10)
    self.sc1.axes[pn].set_ylabel(str(ylabel),fontsize=10)
    max_function1 = (float(np.max(function1)))
    min_function1 = (float(np.min(function1)))
    max_function2 = (float(np.max(function2)))
    min_function2 = (float(np.min(function2)))
    max_value = np.max([max_function1,max_function2])
    min_value = np.max([min_function1,min_function2])
    ticks_to_use = time[::int(len(time)/6)]   
    ticks_to_use_list = time_list[::int(len(time)/6)] 
    self.sc1.axes[pn].set_xticks(ticks_to_use_list)
    self.sc1.axes[pn].set_xticklabels(ticks_to_use)
    #self.sc1.axes[pn].set_yticks(np.arange(min_value,max_value*1.1, step=5))
    self.sc1.axes[pn].tick_params(labelsize=10)

def get_plots_one_functions_all(self,function1,time,label1,ylabel1,pn):
    time_list = (list(range(len(time))))
    self.sc1.axes[pn].plot(time_list,function1,label=label1,picker=5)
    #self.sc1.axes[pn].plot(time,function2,label=file_names[1])
    self.sc1.axes[pn].legend(loc='best',ncol=5,fontsize=10)
    self.sc1.axes[pn].set_xlabel("Time [s]",fontsize=10)
    self.sc1.axes[pn].set_ylabel(str(ylabel1),fontsize=10)
    max_value = (float(np.max(function1)))
    min_value = (float(np.min(function1)))
    print (len(time)/7)
    ticks_to_use = time[::int(len(time)/6)]   
    ticks_to_use_list = time_list[::int(len(time)/6)] 
    yticks_to_use = function1.index[::int(len(function1)/6)]
    print ("FUNCTION")
    print (function1.index)
    print (yticks_to_use)
    print (min(function1))
    print (max(function1)+1)
    diference = max(function1)+2 - min(function1)
    print (diference)
    #print (int(diference/20))
    #print (np.arange(min(function1), max(function1)+1, (diference/10)))
    self.sc1.axes[pn].set_xticks(ticks_to_use_list)
    self.sc1.axes[pn].set_xticklabels(ticks_to_use)
    #self.sc1.axes[pn].set_yticks(np.arange(min(function1), max(function1)+0.15,(round(diference/10,2))))
    #self.sc1.axes[pn].set_yticks([0.9*min_value,1.1*max_value])
    self.sc1.axes[pn].tick_params(labelsize=10)

def get_plots_tunning(self,current_col,current_target,current_foil,magnet_current,pn):
    self.sc1.axes[pn].plot(magnet_current,current_col,'o',label="Collimators",picker=5)
    self.sc1.axes[pn].plot(magnet_current,current_target,'o',label="Target",picker=5)
    self.sc1.axes[pn].plot(magnet_current,current_foil,'o',label="Foil",picker=5)
    #self.sc1.axes[pn].plot(time,function2,label=file_names[1])
    self.sc1.axes[pn].legend(loc='best',ncol=5,fontsize=10)
    self.sc1.axes[pn].set_xlabel("Magnet Current [A]",fontsize=10)
    self.sc1.axes[pn].set_ylabel(str(r"Current [$\mu$A]"),fontsize=10)
    print ("HEREEEEEEE")
    ##print (ticks_to_use_list)
    print (magnet_current)
    self.sc1.axes[pn].tick_params(labelsize=10)

def getting_average_values(file_name):
    [real_values,target_number,date_stamp ] = get_data_tuple(file_name)
    data_df = get_data(real_values)
    vacuum = get_vacuum_parameters(data_df,0)
    vacuum_average = round(np.average(vacuum)*1e5,2)
    magnet_current = get_magnet_parameters(data_df,0)
    magnet_average = np.average(magnet_current)
    return target_number,vacuum_average,magnet_average



def get_statistic_values(value):
    average_value = (np.mean(value))
    std_value = (np.std(value))
    try:
       max_value = (np.max(value))
       min_value = (np.min(value))
    except:
       max_value = 0
       min_value = 0
    return average_value,std_value,max_value,min_value

def get_raw_parameters(excel_data_df):
    [target_current,current] = get_target_parameters(excel_data_df)
    time = get_time(excel_data_df,current)
    foil_number = get_time(excel_data_df,current)
    return target_current,current,time,foil_number
   
def get_subsystems_dataframe_source(excel_data_df,current,target_number,target_current,time,foil_number):
    df_column_names_source = ["Time","Foil_No","Arc_I","Arc_V","Gas_flow","Ratio_current"]
    source_voltage,source_current,gas_flow = get_source_parameters(excel_data_df,current)
    ratio_current = source_current/(target_current)
    df_subsystem_values_source = [time,foil_number,source_current,source_voltage,gas_flow,ratio_current]  
    df_subsystem_source = pd.concat(df_subsystem_values_source, axis=1, keys=df_column_names_source)
    return df_subsystem_source

def get_subsystems_dataframe_vacuum(excel_data_df,current,target_number,target_current,time,foil_number):
    df_column_names_vacuum = ["Time","Foil_No","Vacuum_P"]
    vacuum_level = get_vacuum_parameters(excel_data_df,current)
    magnet_current = get_magnet_parameters(excel_data_df,current)
    df_subsystem_values_vacuum = [time,foil_number,vacuum_level]
    df_subsystem_vacuum = pd.concat(df_subsystem_values_vacuum,axis=1,keys=df_column_names_vacuum)
    return df_subsystem_vacuum

def get_subsystems_dataframe_magnet(excel_data_df,current,target_number,target_current,time,foil_number):    
    df_column_names_magnet = ["Time","Foil_No","Magnet_I"]
    magnet_current = get_magnet_parameters(excel_data_df,current)
    df_subsystem_valuesmagnet = [time,foil_number,magnet_current]
    df_subsystem_magnet = pd.concat(df_subsystem_valuesmagnet,axis=1,keys=df_column_names_magnet)
    return df_subsystem_magnet

def get_subsystems_dataframe_rf(excel_data_df,current,target_number,target_current,time,foil_number):
    df_column_names_rf = ["Time","Foil_No","Dee_1_kV","Dee_2_kV","RF_fwd_W","RF_refl_W","Phase_load","Flap1_pos","Flap2_pos"]
    dee1_voltage,dee2_voltage = get_rf_parameters(excel_data_df,current) 
    forwarded_power,reflected_power,phase_load = get_rf_parameters_power(excel_data_df,current)
    flap1_pos,flap2_pos = get_rf_parameters_flaps(excel_data_df,current)
    df_subsystem_values_rf = [time,foil_number,dee1_voltage,dee2_voltage,forwarded_power,reflected_power,phase_load,flap1_pos,flap2_pos]
    df_subsystem_rf = pd.concat(df_subsystem_values_rf,axis=1,keys=df_column_names_rf)
    return df_subsystem_rf

def get_subsystems_dataframe_rf_sparks(excel_data_df,current,target_number,target_current,time,foil_number):
    df_column_names_rf = ["Dee_1_kV","Dee_2_kV","RF_fwd_W","RF_refl_W","Phase_load","Flap1_pos","Flap2_pos"]
    dee1_voltage,dee2_voltage = get_rf_parameters_sparks(excel_data_df,current) 
    forwarded_power,reflected_power,phase_load = get_rf_parameters_power_sparks(excel_data_df,current)
    flap1_pos,flap2_pos = get_rf_parameters_flaps_sparks(excel_data_df,current)
    df_subsystem_values_rf = [dee1_voltage,dee2_voltage,forwarded_power,reflected_power,phase_load,flap1_pos,flap2_pos]
    df_subsystem_rf = pd.concat(df_subsystem_values_rf,axis=1,keys=df_column_names_rf)
    return df_subsystem_rf

def get_subsystems_dataframe_extraction(excel_data_df,current,target_number,target_current,time,foil_number):
    df_column_names_extraction = ["Time","Foil_No","Extr_pos","Balance"]
    carousel_position,balance_position = get_extraction_parameters_position(excel_data_df,current)
    df_subsystem_values_extraction = [time,foil_number,carousel_position,balance_position]
    df_subsystem_extraction = pd.concat(df_subsystem_values_extraction,axis=1,keys=df_column_names_extraction)
    return df_subsystem_extraction

def get_subsystems_dataframe_beam(excel_data_df,current,target_number,target_current,time,foil_number):
    df_column_names_beam = ["Time","Foil_No","Foil_I","Coll_l_I","Target_I","Coll_r_I","Coll_l_rel","Coll_r_rel","Target_rel","Extraction_losses"]
    collimator_r,collimator_l = get_collimator_parameters(excel_data_df,current) 
    extraction_current = get_extraction_parameters(excel_data_df,current)
    collimator_r_rel = collimator_r/extraction_current*100
    collimator_l_rel = collimator_l/extraction_current*100
    target_rel = (target_current)/extraction_current*100
    extraction_losses = (1-(target_current+collimator_l+collimator_r)/extraction_current)*100
    df_subsystem_values_beam = [time,foil_number,extraction_current,collimator_l,target_current,collimator_r,collimator_l_rel,collimator_r_rel,target_rel,extraction_losses]
    df_subsystem_beam = pd.concat(df_subsystem_values_beam,axis=1,keys=df_column_names_beam)
    return df_subsystem_beam

def get_subsystems_dataframe_pressure(excel_data_df,current,target_number,target_current,time,foil_number):
    df_column_names_pressure = ["Time","Foil_No","Target_P"]
    target_pressure = get_target_pressure(excel_data_df,current)
    df_subsystem_values_pressure = [time,foil_number,target_pressure]
    df_subsystem_pressure = pd.concat(df_subsystem_values_pressure,axis=1,keys=df_column_names_pressure)
    return df_subsystem_pressure


def get_summary_ion_source(df_subsystems_source,source_performance,file,target_number,date_stamp,df_source): 
    source_current = df_subsystems_source.Arc_I
    source_voltage = df_subsystems_source.Arc_V
    gas_flow = df_subsystems_source.Gas_flow
    ratio_current = df_subsystems_source.Ratio_current
    foil_number = np.average(df_subsystems_source.Foil_No)
    ave_source_current,std_source_current,max_source_current,min_source_current = get_statistic_values(source_current)  
    ave_source_voltage,std_source_voltage,max_source_voltage,min_source_voltage = get_statistic_values(source_voltage)  
    ave_gas_flow,std_gas_flow,max_gas_flow,min_gas_flow = get_statistic_values(gas_flow) 
    ave_ratio_current,std_ratio_current,max_ratio_current,min_ratio_current = get_statistic_values(ratio_current)
    df_source_values = [[file,date_stamp,target_number,foil_number,
    float(max_source_current),float(min_source_current),float(ave_source_current),float(std_source_current),
    float(max_source_voltage),float(min_source_voltage),float(ave_source_voltage),float(std_source_voltage),
    float(max_gas_flow),
    float(max_ratio_current),float(min_ratio_current),float(ave_ratio_current),float(std_ratio_current),float(source_performance)
    ]]
    df_source_i = pd.DataFrame(df_source_values,columns=COLUMNS_SOURCE)
    df_source = df_source.append(df_source_i,ignore_index=True)
    return df_source

def get_summary_vacuum(df_subsystems_vacuum,file,target_number,date_stamp,df_vacuum):
    vacuum_level = df_subsystems_vacuum.Vacuum_P
    foil_number = np.average((df_subsystems_vacuum.Foil_No))
    ave_vacuum,std_vacuum,max_vacuum,min_vacuum = get_statistic_values(vacuum_level)
    vacuum_values = [[file,date_stamp,target_number,foil_number,float(max_vacuum)*1e5,float(min_vacuum)*1e5,float(ave_vacuum)*1e5,float(std_vacuum)*1e5]]
    df_vacuum_i = pd.DataFrame((vacuum_values),columns=COLUMNS_VACUUM)
    df_vacuum = df_vacuum.append(df_vacuum_i,ignore_index=True)
    return df_vacuum

def get_summary_magnet(df_subsystems_magnet,file,target_number,date_stamp,df_magnet):
    magnet_current = df_subsystems_magnet.Magnet_I
    foil_number = np.average((df_subsystems_magnet.Foil_No))
    ave_magnet_current,std_magnet_current,max_magnet_current,min_magnet_current = get_statistic_values(magnet_current)
    magnet_values = [[file,date_stamp,target_number,foil_number,float(max_magnet_current),float(min_magnet_current),float(ave_magnet_current),float(std_magnet_current)]]
    df_magnet_i = pd.DataFrame((magnet_values),columns=COLUMNS_MAGNET)
    df_magnet = df_magnet.append(df_magnet_i,ignore_index=True)
    return df_magnet

def get_summary_rf(df_subsystems_rf,file,target_number,date_stamp,df_rf):
    dee1_voltage = df_subsystems_rf.Dee_1_kV
    dee2_voltage = df_subsystems_rf.Dee_2_kV
    forwarded_power = df_subsystems_rf.RF_fwd_W
    reflected_power = df_subsystems_rf.RF_refl_W
    phase_load = df_subsystems_rf.Phase_load
    flap1_pos = df_subsystems_rf.Flap1_pos
    flap2_pos = df_subsystems_rf.Flap2_pos
    foil_number = np.average((df_subsystems_rf.Foil_No))
    ave_dee1_voltage,std_dee1_voltage,max_dee1_voltage,min_dee1_voltage = get_statistic_values(dee1_voltage)   
    ave_dee2_voltage,std_dee2_voltage,max_dee2_voltage,min_dee2_voltage = get_statistic_values(dee2_voltage)
    ave_forwarded_power,std_forwarded_power,max_forwarded_power,min_forwarded_power = get_statistic_values(forwarded_power)
    ave_reflected_power,std_reflected_power,max_reflected_power,min_reflected_power = get_statistic_values(reflected_power)
    ave_flap1_pos,std_flap1_pos,max_flap1_pos,min_flap1_pos = get_statistic_values(flap1_pos)
    ave_flap2_pos,std_flap2_pos,max_flap2_pos,min_flap2_pos = get_statistic_values(flap2_pos)
    ave_phase_load,std_phase_load,max_phase_load,min_phase_load = get_statistic_values(flap2_pos)
    rf_values = [[file,date_stamp,target_number,foil_number,max_dee1_voltage,min_dee1_voltage,ave_dee1_voltage,std_dee1_voltage,max_dee2_voltage,min_dee2_voltage,ave_dee2_voltage,std_dee2_voltage,
    max_forwarded_power,min_forwarded_power,ave_forwarded_power,std_forwarded_power,max_reflected_power,min_reflected_power,ave_reflected_power,std_reflected_power,max_phase_load,min_phase_load,ave_phase_load,std_phase_load,max_flap1_pos,min_flap1_pos,ave_flap1_pos,std_flap1_pos,
    max_flap2_pos,min_flap2_pos,ave_flap2_pos,std_flap2_pos]]
    df_rf_i = pd.DataFrame((rf_values),columns=COLUMNS_RF)      
    df_rf = df_rf.append(df_rf_i,ignore_index=True)
    return df_rf


def get_summary_extraction(df_subsystems_extraction,file,target_number,date_stamp,df_extraction):
    carousel_position = df_subsystems_extraction.Extr_pos
    balance_position = df_subsystems_extraction.Balance
    foil_number = np.average((df_subsystems_extraction.Foil_No))
    ave_carousel_position,std_carousel_position, max_carousel_position, min_carousel_position = get_statistic_values(carousel_position)
    ave_balance_position,std_balance_position, max_balance_position, min_balance_position = get_statistic_values(balance_position)
    extraction_values = [[file,date_stamp,target_number,foil_number,max_carousel_position,min_carousel_position,ave_carousel_position,std_carousel_position,max_balance_position,min_balance_position,ave_balance_position,std_balance_position]]
    df_extraction_i = pd.DataFrame((extraction_values),columns=COLUMNS_EXTRACTION)      
    df_extraction = df_extraction.append(df_extraction_i,ignore_index=True)
    return df_extraction

def get_summary_beam(df_subsystems_beam,file,target_number,date_stamp,df_beam):
    target_current = df_subsystems_beam.Target_I
    extraction_current = df_subsystems_beam.Foil_I 
    collimator_r = df_subsystems_beam.Coll_r_I   
    collimator_l = df_subsystems_beam.Coll_l_I  
    collimator_r_rel = df_subsystems_beam.Coll_r_rel 
    collimator_l_rel = df_subsystems_beam.Coll_l_rel
    target_rel = df_subsystems_beam.Target_rel
    extraction_losses = df_subsystems_beam.Extraction_losses
    foil_number = np.average((df_subsystems_beam.Foil_No))
    ave_extraction_current,std_extraction_current,max_extraction_current,min_extraction_current = get_statistic_values(extraction_current)
    ave_target_current,std_target_current,max_target_current,min_target_current = get_statistic_values(target_current)
    ave_collimator_r,std_collimator_r, max_collimator_r, min_collimator_r = get_statistic_values(collimator_r)
    ave_collimator_l,std_collimator_l, max_collimator_l, min_collimator_l = get_statistic_values(collimator_l)
    ave_collimator_r_rel,std_collimator_r_rel, max_collimator_r_rel, min_collimator_r_rel = get_statistic_values(collimator_r_rel)
    ave_collimator_l_rel,std_collimator_l_rel, max_collimator_l_rel, min_collimator_l_rel = get_statistic_values(collimator_l_rel)
    ave_target_rel,std_target_rel,max_target_rel,min_target_rel = get_statistic_values(target_rel)
    ave_extraction_losses,std_extraction_losses,max_extraction_losses,min_extraction_losses = get_statistic_values(extraction_losses)
    beam_values = [[file,date_stamp,target_number,foil_number,
    max_collimator_l,min_collimator_l, ave_collimator_l, std_collimator_l,
    max_collimator_r,min_collimator_r, ave_collimator_r, std_collimator_r,
    max_collimator_l_rel,min_collimator_l_rel, ave_collimator_l_rel, std_collimator_l_rel,
    max_collimator_r_rel,min_collimator_r_rel, ave_collimator_r_rel, std_collimator_r_rel,
    max_target_current,min_target_current,ave_target_current,std_target_current,
    max_extraction_current,min_extraction_current,ave_extraction_current,std_extraction_current,
    max_target_rel,min_target_rel,ave_target_rel,std_target_rel,
    max_extraction_losses,min_extraction_losses,ave_extraction_losses,std_extraction_losses]]
    df_beam_i = pd.DataFrame((beam_values),columns=COLUMNS_BEAM )      
    df_beam = df_beam.append(df_beam_i,ignore_index=True)
    return df_beam


def main(input_path,output_path,target_current):
    df_source = pd.DataFrame(columns=COLUMNS_SOURCE)
    df_vacuum = pd.DataFrame(columns=COLUMNS_VACUUM)
    df_magnet = pd.DataFrame(columns=COLUMNS_MAGNET)
    df_beam = pd.DataFrame(columns=COLUMNS_BEAM )
    df_rf = pd.DataFrame(columns=COLUMNS_RF)
    df_extraction = pd.DataFrame(columns=COLUMNS_EXTRACTION)
    df_transmission = pd.DataFrame(columns=COLUMNS_TRANSMISSION)
    input_path_names = input_path[0]
    print ("HEREEEEEE")
    print (input_path)
    #print (input_path.pop(0))
    #input_path.pop(0) 
    file_number = []
    input_path_names = input_path[0]
    input_path.pop(0) 
    input_path_filtered = []
    file_path = []
    for file in (input_path):
        file_path.append(file)
        input_path_filtered.append(os.path.getsize(os.path.join(input_path_names, file)))
    input_path_filtered_array = np.array(input_path_filtered)
    file_path_array = np.array(file_path)
    print (input_path_filtered_array)
    file_path_array_max = file_path_array[input_path_filtered_array > 0.1*max(input_path_filtered_array)]
    #file_path_no_array = file_path_array[input_path_filtered_array < 0.4*max(input_path_filtered_array)]
    possible_normal = []
    possible_pre_irradiation = []
    for file in file_path_array_max:
        file_path = os.path.join(input_path_names, file)
        #print (file)
        file_number.append(float(file[:-4]))
        real_values,target_number,date_stamp = get_data_tuple(file_path)
        # Get the dataframe from logfile 
        #date_stamp_all.append((date_stamp))
        excel_data_df = get_data(real_values)
        target_current = excel_data_df.Target_I.astype(float)
        print ("AVERAGE CURRENT")
        print (np.average(target_current))
        #print (excel_data_df.Target_I[excel_data_df['Target_I'].astype(float) == 25.0].astype(float))
        print ("LENS")
        print (len(excel_data_df.Target_I[excel_data_df['Target_I'].astype(float) == 50.0].astype(float)))
        print (len(excel_data_df.Target_I[excel_data_df['Target_I'].astype(float) == 25.0].astype(float)))
        print (len(excel_data_df.Target_I[excel_data_df['Target_I'].astype(float) == 0.0].astype(float)))
        print (len(excel_data_df.Target_I[excel_data_df['Target_I'].astype(float) == 25.0].astype(float)) +len(excel_data_df.Target_I[excel_data_df['Target_I'].astype(float) ==0.0].astype(float)))
        pre_irradiation_len = (len(excel_data_df.Target_I[excel_data_df['Target_I'].astype(float) == 50.0].astype(float))) + (len(excel_data_df.Target_I[excel_data_df['Target_I'].astype(float) == 25.0].astype(float))) + (len(excel_data_df.Target_I[excel_data_df['Target_I'].astype(float) == 0.0].astype(float)))
        print (len(excel_data_df.Target_I.astype(float)))
        print (pre_irradiation_len)
        print (pre_irradiation_len/len(excel_data_df.Target_I.astype(float)))
        print ("RELATIVE")
        pre_irradiation_len_relative = (pre_irradiation_len/len(excel_data_df.Target_I.astype(float)))
        print (pre_irradiation_len)
        print ("FILE")
        print (file)
        #print (excel_data_df.Time[excel_data_df['Target_I'].astype(float) == 25.0])
        #print (len(excel_data_df.Time[excel_data_df['Target_I'].astype(float) == 25.0])/len(excel_data_df.Target_I.astype(float)))
        if (pre_irradiation_len_relative) > 0.3:
            possible_pre_irradiation.append(file)
        else:
            possible_normal.append(file)
    reasons_small_file = []
    for file in (possible_normal):
        file_path = os.path.join(input_path_names, file)
        print (file)
        file_number.append(float(file[:-4]))
        real_values,target_number,date_stamp = get_data_tuple(file_path)
        # Get the dataframe from logfile 
        #date_stamp_all.append((date_stamp))
        excel_data_df = get_data(real_values)
        [target_current,current] = get_target_parameters(excel_data_df)
        max_source_current = get_source_parameters_limit(excel_data_df)
        time = get_time(excel_data_df,current)
        try:
           foil_number = get_foil_number(excel_data_df,current)
        except:
           foil_number = get_target_pressure(excel_data_df,current)
        df_subsystem_source = get_subsystems_dataframe_source(excel_data_df,current,target_number,target_current,time,foil_number)
        df_subsystem_vacuum = get_subsystems_dataframe_vacuum(excel_data_df,current,target_number,target_current,time,foil_number)
        df_subsystem_magnet = get_subsystems_dataframe_magnet(excel_data_df,current,target_number,target_current,time,foil_number)
        df_subsystem_rf = get_subsystems_dataframe_rf(excel_data_df,current,target_number,target_current,time,foil_number)
        df_subsystem_rf_sparks = get_subsystems_dataframe_rf_sparks(excel_data_df,max_source_current,target_number,target_current,time,foil_number)
        df_subsystem_extraction = get_subsystems_dataframe_extraction(excel_data_df,current,target_number,target_current,time,foil_number)
        df_subsystem_beam = get_subsystems_dataframe_beam(excel_data_df,current,target_number,target_current,time,foil_number)
        df_subsystem_pressure = get_subsystems_dataframe_pressure(excel_data_df,current,target_number,target_current,time,foil_number)
        df_isochronism = get_isochronism(excel_data_df)
        [probe_current,ion_source_current,df_source_performance] = get_ion_source_performance(excel_data_df)
        df_source = get_summary_ion_source(df_subsystem_source,df_source_performance,str(file[:-4]),target_number[1],date_stamp,df_source)
        df_vacuum = get_summary_vacuum(df_subsystem_vacuum,str(file[:-4]),target_number[1],date_stamp,df_vacuum)
        df_magnet = get_summary_magnet(df_subsystem_magnet,str(file[:-4]),target_number[1],date_stamp,df_magnet)
        df_rf = get_summary_rf(df_subsystem_rf,str(file[:-4]),target_number[1],date_stamp,df_rf)
        df_extraction = get_summary_extraction(df_subsystem_extraction,str(file[:-4]),target_number[1],date_stamp,df_extraction)
        df_beam = get_summary_beam(df_subsystem_beam,str(file[:-4]),target_number[1],date_stamp,df_beam)
        df_transmission = get_transmission(df_isochronism,probe_current,df_subsystem_source,str(file[:-4]),target_number[1],date_stamp,df_transmission)
        # GETTING STADISTIC NUMBERS
        # summary voltage 
        
    df_rf = df_rf.dropna()
    df_extraction = df_extraction.dropna()
    df_source = df_source.dropna()
    df_vacuum = df_vacuum.dropna()
    df_magnet = df_magnet.dropna()
    df_beam = df_beam.dropna()

    df_rf = df_rf.sort_values(by=['FILE'])
    df_extraction = df_extraction.sort_values(by=['FILE'])
    df_source = df_source.sort_values(by=['FILE'])
    df_vacuum = df_vacuum.sort_values(by=['FILE'])
    df_magnet = df_magnet.sort_values(by=['FILE'])
    df_beam = df_beam.sort_values(by=['FILE'])
    df_transmission = df_transmission.sort_values(by=['FILE'])
 


    tfs_output_source = os.path.join(output_path,"table_summary_source.out")
    tfs_output_vacuum = os.path.join(output_path,"table_summary_vacuum.out")
    tfs_output_magnet = os.path.join(output_path,"table_summary_magnet.out")
    tfs_output_beam = os.path.join(output_path,"table_summary_beam.out")
    tfs_output_extraction = os.path.join(output_path,"table_summary_extraction.out")
    tfs_output_rf = os.path.join(output_path,"table_summary_rf.out")
    tfs_output_trans = os.path.join(output_path,"table_summary_transmission.out")

    tfs.write(tfs_output_source, df_source)
    tfs.write(tfs_output_vacuum, df_vacuum)
    tfs.write(tfs_output_magnet, df_magnet)
    print ("df_beam")
    print (df_beam)
    tfs.write(tfs_output_beam, df_beam)
    tfs.write(tfs_output_extraction, df_extraction)
    tfs.write(tfs_output_rf, df_rf)
    tfs.write(tfs_output_trans,df_transmission)

    #tfs.write(tfs_output_extraction_balance,df_extraction_balance_position_all)
    #print ("NO LONG FILES")
    #print (file_path_no_array)
    #print ("POSSIBLE FAILURE")
    #print (possible_failure)
    print ("POSSIBLE PRE IRRADIATION")
    print (possible_pre_irradiation)


if __name__ == "__main__":
    _input_path,_output_path,target_current = _parse_args()
    main(_input_path,_output_path,target_current)
