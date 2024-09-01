# Morpheon #

Morpheon is a project with the goal of building a morphing wing aircraft.



The design can be broken down into the following areas:
- Design
- Aerodymanics
- Electronics
- Control


All of the above will be determined by the following performance goals and restrictions.
- Autonomous Vertical Take off and Landing
- Top speed of roughly 200km/h
- Bottom speed of roughly 20 km/h
- Max g-force of 20g
- Minimum drag possible
- Altitude 0m to 500m
- Payload 1kg
- Net weight goal 2kg
- Autonomous flight, waypoints and stuff
- Printable on the Kymeron 3d Printer. Max root chord of 400mm. Max wingspan of 600mm. These are the main dimension constraints




The design must be parametrically calculated.
Input parameters can vary from minimum requirements to specifics being provided.


Aerodymanics
Choose a flying wing to reduce drag.
Calculate sweep of flying wing for AC to be well behind CG.
Calculate wing area
Calculate Weight
Calculate stability https://www.mh-aerotools.de/airfoils/flywing1.htm
List flight profiles
- Take off
    - low speed
    - low reynolds
    - High alpha stall at low reynolds
    - High Cl at low reynolds
    - Drag is not important
    - Cl is way more important than drag
- Top speed straight cruising high efficient long distance
    - high speed
    - low drag
    - higher reynolds number
    - optimise for low drag
- Acrobatic manouvre at max g's
For each flight profile
- Calculate wing loading
- Calculate Reynolds number
- Find airfoils that produce the required lift
    Use a bell curve lift distribution
    - Use laminar for high speed
    - Use turbulent for low speed
    - use nueral foil to determine airfoil https://github.com/peterdsharpe/NeuralFoil
- Calculate drag at that speed
- Calculate required thrust
Morphing foil dimensions
- Calculate rib sizes for min to max airfoil


Automatically Draw aircraft in Fusion 360
- Draw fuselage
    - 2 x EDF and thrust vectoring exhuast
    - Gimballed camera at front
- Draw wings with morphing ribs and spars
- Include electronics to estimate weight
- Vaildate that weight is within goal weight





Electronics
    - Flight Controller
        - Pixhawk
        - Ardupilot includes VTOL
    - GPS
    - VTX
    - Camera with Gimbal
        - Walksnail
    - Airspeed sensor
    - Barometer

Build calculations with python
Use NACA Airfoils

Calculate top profile line for a given length of that line.

Calculate points for different desired profiles.
Calculate the location for every 1/10th distance along that line.

join the dots for each 1/10th point from one profile to the next
This will create a curved line.

Then find the center point that draws that curve.

To calculate the 1/10 point
sum the distances from each point to the next until it exceeds the 1/10 distance.




Visualise optimisations with matlibplot

Drive design formulas and parameters in fusion 360 with outputs from calculations above.

git clone https://github.com/usuaero/MachUp



References:
- https://www.mh-aerotools.de/airfoils/flywing1.htm
- https://ijettjournal.org/assets/year/2018/volume-59/number-4/IJETT-V59P233.pdf
- https://dergipark.org.tr/tr/download/article-file/629766
- https://www.ecalc.ch/wingdesigner.htm#:~:text=Flying%20Wings%3A%20The%20CG%20is,stability%20and%20use%20resulting%20CG.
- https://www.nestofdragons.net/weird-airplanes/flying-wings/flying-wing-designer/
- https://apmonitor.com/me575/uploads/Main/2013_Flying_Wing.pdf
- https://ijettjournal.org/assets/year/2018/volume-59/number-4/IJETT-V59P233.pdf
