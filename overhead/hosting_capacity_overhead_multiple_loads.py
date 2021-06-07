import pandapower as pp
from numpy.random import choice
from numpy.random import normal
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import math
from overhead import overhead_network_for_hosting_capacity_Multiple_Values

warnings.filterwarnings("ignore")


july_LoadProfile_KW = [1.207, 1.1541, 1.0882, 0.9982, 0.9022, 0.8484, 0.8334,
                       0.8633, 0.3256, 0.7992, 1.30865, 0.8263, 0.93595, 1.254,
                       1.331, 1.1725, 1.4316, 1.621, 1.3541, 1.1422, 0.7352,
                       1.1045, 1.1111, 1.1948]

def convert_from_kW_to_MW(number):
    return number / 1000

def convert_to_sn_mva_with_cosf(number):
    return number / 0.85

# Convert from kW to MW
julyLoadProfile = list(map(convert_from_kW_to_MW, july_LoadProfile_KW))

# Convert to S power with pf=0.85
julyLoadProfile = list(map(convert_to_sn_mva_with_cosf, julyLoadProfile))

def violations(net):
    pp.runpp(net)
    if net.res_line.loading_percent.max() > 50:
        #print("line overloading violation")
        print("max load" ,net.res_line.i_ka[0] * 1000)
        print("real power" ,net.res_line.p_from_mw[0] * 1000)
        print("reactive power" ,net.res_line.q_from_mvar[0] * 1000)
        print()

        return (True, "Line \n Overloading")
    elif net.res_trafo.loading_percent.max() > 50:
        print("transformer overloading violation")
        return (True, "Transformer \n Overloading")
    elif net.res_bus.vm_pu.max() > 1.05:
        #print("bus overvoltage violation")
        return (True, "Voltage \n Violation")
    else:
        return (False, None)


def chose_bus(net):
    return choice(net.load.bus.values)


def get_plant_size_mw():
    return round(normal(loc=0.005, scale=0.001), 3)


iterations = 50
results = pd.DataFrame(columns=["installed", "violation"])

results_list = []
boxplot_results = []

#for loadValue in julyLoadProfile:
for i in range(iterations):
    net = overhead_network_for_hosting_capacity_Multiple_Values.overhead_network(0.0003256)
    installed_mw = 0
    while 1:
        violated, violation_type = violations(net)
        if violated:
            results.loc[i] = [installed_mw, violation_type]
            break
        else:
            plant_size = get_plant_size_mw()
            pp.create_sgen(net, chose_bus(net), p_mw=plant_size, q_mvar=0)
            installed_mw += plant_size


    boxplot_results.append(list(results.installed * 1000) )

    results_list.append(results.installed.mean() * 1000)
    #print(results.installed.mean())
#print(len(results_list))
# -plant_size * tan(acos(0.95))
# -(plant_size * math.tan(math.acos(0.95)))


# plt.bar(time_steps, results_list, color=(0.2, 0.4, 0.6, 0.6))
# plt.xlabel("Timesteps")
# plt.ylabel("Installed Capacity [kW]")
# plt.show()
#
# sns.boxplot(data=boxplot_results)
# plt.xlabel("Timesteps")
# plt.ylabel("Installed Capacity [kW]")
# plt.show()
#
#
# # %matplotlib inline
# plt.rc('xtick', labelsize=18)  # fontsize of the tick labels
# plt.rc('ytick', labelsize=18)  # fontsize of the tick labels
# plt.rc('legend', fontsize=18)  # fontsize of the tick labels
# plt.rc('axes', labelsize=20)  # fontsize of the tick labels
# plt.rcParams['font.size'] = 20
#
# sns.set_style("whitegrid", {'axes.grid': True})

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
ax = axes[0]
sns.boxplot(data=results_list * 1000, width=.1, ax=ax, orient="v")
ax.set_xticklabels([""])
ax.set_ylabel("Installed Capacity [kW]")

ax = axes[1]
ax.axis("equal")
results.violation.value_counts().plot(kind="pie", ax=ax, autopct=lambda x: "%.0f %%" % x)
ax.set_ylabel("")
ax.set_xlabel("")
sns.despine()
plt.tight_layout()

plt.show()
