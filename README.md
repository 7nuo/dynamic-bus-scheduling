# Bus Scheduling including Dynamic Events

Modern transportation systems should be designed according to the requirements of their passengers, while considering operational costs for the managing organizations, as well as being environmentally friendly. The main objective of this research project is to provide a realistic simulation of a transportation system, capable of identifying connections among the road network of operation areas, creating bus lines composed of multiple connected bus stops, simulating travel requests registered by potential passengers, as well as generating routes and timetables for bus vehicles, while taking into consideration factors which could affect the predefined schedule, including unpredictable events (e.g., traffic accidents) or dynamic levels of traffic density.

The implemented bus management system is able to generate timetables dynamically, introducing a reasoning mechanism capable of evaluating travel requests based on dynamic clustering techniques, while offering the opportunity to its administrator to make decisions regarding the number of generated timetables, operating bus vehicles, passengers per timetable, waiting time of passengers, and processing time. In addition, the routes of bus lines are generated or updated dynamically, while taking into consideration real-time traffic data and evaluating parameters, such as covered distance or travelling time, in order to identify the most effective connections between the bus stops of each bus line and make adjustments to the corresponding timetables. Finally, the number of operating bus vehicles that are required in order to transport the passengers of each bus line is estimated, leading to a more efficient distribution of available resources.

More precisely, the implemented system is able to:

* Process [OpenStreetMap](https://www.openstreetmap.org/) files and extract geospatial data related to the road network of operation areas (e.g., bus stops and paramenters of intermediate road connections).
* Identify multiple possible route connections between the bus stops of operation areas, implementing a variation of the *Breadth-first* search algorithm.
* Generate bus lines connecting the bus stops of operation areas.
* Receive real-time traffic data.
* Simulate traffic events capable of affecting the predefined schedule.
* Simulate travel requests registered by potential passengers.
* Identify the less time-consuming routes connecting the bus stops of operation areas, implementing a variation of the *A-star* search algorithm, while taking into consideration current levels of traffic density.
* Apply a timetable generation algorithm capable of evaluating travel requests utilizing dynamic clustering procedures and generating timetables for bus vehicles while offering the option to its administrator to make decisions regarding the number of generated timetables, operating bus vehicles, number of passengers per vehicle, average waiting time of passengers, and processing time.
* Monitor the levels of traffic density and make adjustments to the regular path of each bus, in order to limit the level of affection on the average waiting time of passengers due to traffic incidents.

# Contributors

The project is supervised by the Research and Development Department of [Ericsson](https://www.ericsson.com/) and is considered as a use case of [CityPulse](http://www.ict-citypulse.eu/).

# Project Report

Details regarding the implemented system, experimental evaluation, deployment guidance, and technical instructions are included in the [report](https://github.com/pinac0099/dynamic-bus-scheduling/blob/master/documents/project_report.pdf) of the project.
