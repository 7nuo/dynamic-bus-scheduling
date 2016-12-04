# Bus Scheduling including Dynamic Events

This project provides a realistic simulation of a transportation system, including connections among the road network of operation areas, bus lines connecting multiple bus stops, routes and timetables for bus vehicles, travel requests registered by potential passengers, and factors which usually affect the normal schedule such as the levels of traffic density.

In addition, a reasoning mechanism is introduced, capable of evaluating travel requests and generating timetables for bus vehicles, while limiting the average waiting time of passengers as well as the number of passengers per vehicle.

Finally, traffic flow detection is utilized, in order to make adjustments to the regular path of each bus and limit the waiting time of passengers which could be increased due to traffic congestion.

The provided system is able to:

* Process OpenStreetMap files and extract geospatial data related to the road network of operation areas.
* Generate bus lines connecting multiple bus stops.
* Receive real-time traffic data from the CityPulse Data Bus.
* Simulate traffic events.
* Identify all the possible routes connecting multiple bus stops, implementing a variation of the Breadth-first Search Algorithm.
* Identify the less time-consuming routes connecting multiple bus stops, implementing a variation of the A* Search Algorithm, while taking into consideration current levels of traffic density.
* Simulate travel requests registered by potential passengers.
* Apply a timetable generation algorithm capable of evaluating travel requests, utilizing dynamic clustering procedures, and generating timetables for bus vehicles while limiting the average waiting time of passengers as well as the number of passengers per vehicle.
* Monitor the levels of traffic density and make adjustments to the regular path of each bus, in order to limit the level of affection of the average waiting time of passengers due to traffic incidents.

# Contributors

The project is supervised by [Ericsson] (https://www.ericsson.com/) and is considered as a use case of [CityPulse] (http://www.ict-citypulse.eu/), a European project focused on the development of a distributed framework for semantic discovery and processing of large-scale real-time Internet of Things and relevant social data streams, which could be used for knowledge extraction in urban environments.

# Related Work

The development of the project was inspired by [Mobile Network Assisted Driving (MoNAD)] (https://github.com/EricssonResearch/monad), an [Ericsson Research project] (https://www.ericsson.com/research-blog/smart-cities/personalized-bus-transportation/) developed by [Uppsala University] (http://www.uu.se/en/) in the scope of the [Project Computer Science 2015] (http://www.it.uu.se/edu/course/homepage/projektDV/ht15) course.
