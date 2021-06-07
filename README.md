# hosting-Capacity 
In this project I created two low voltage networks of Electric Authority of Cyprus. 
One overhead and one with underground cables. 

Using Time Series algorithm I investigated the overhead network`s behavior under the impact of PV penetration. 
During the day, the sun radiation changes, thus the power production of PVs, Similarly the load consumtion varies from hour to hour. 
With the use of Time Series algorithm we can see the level of voltage bus and the level of loading of the lines during the day. 
Time Series Calculation algorithm: 
https://github.com/e2nIEE/pandapower/blob/develop/tutorials/time_series.ipynb


I also calculated the maximum hosting capacity for the current network 
With the use of a Monte Carlo simulation I checked the maximum hosting capacity for PV installation. 
Hosting Capacity algorithm:
https://github.com/e2nIEE/pandapower/blob/develop/tutorials/hosting_capacity.ipynb



In the Overhead folder you will find: 

hosting_capacity.py -> This calculates the hosting capacity for only one case. 

hosting_capacity_overhead_multiple_loads.py -> This calculates the hosting capacity for multiple loads.

overhead_network_Simple.py -> This is the overhead network.

overhead_network_for_TSS.py -> This is the overhead network for time series calculation.

overhead_network_for_hosting_capacity_Multiple_Values.py -> This is the network for calculation hosting capacity for multiple values.

In the underground folder you will find: 
hosting_capacity_underground.py -> The hosting capacity algorithm for the underground network. 

underground_network.py -> This is the underground netowrk. 



Required Software: Pandapower 
https://www.pandapower.org/
