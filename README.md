# Volcanic project

> MoSIG M1 - 3D Graphics

## Author Names

- Aleksandr Sergeev
- Pia Dopper
- Farah Maria Majdalani

## How to Run the Code

Run in the terminal:

```bash
 make run
```

This command will make sure all the dependencies required for the project are downloaded.

```bash
 make help
```

Will print detailed description of all the console commands available.

## Controls

See [configurations](#configurations) section for configuration file description.
In runtime, the following actions are recognized:

1. `SPACEBAR` key: restart the animation time (from `initial_time` see [configs](#configurations)).
2. `A` or `LEFT` key: move camera left by one unit.
3. `W` or `UP` key: move camera up by one unit.
4. `D` or `RIGHT` key: move camera right by one unit.
5. `S` or `DOWN` key: move camera down by one unit.
6. Mouse wheel scroll: zoom the simulation.
7. Mouse drag with right button pressed: move camera in the direction of drag.
8. Mouse drag with left button pressed: rotate camera in the direction of drag.

## Features Implemented

Our simulation has different input parameters to configure them, such as size, heat, initialization time. The parameter Size regulates the size of the simulation. So how big is the volcano, the water, the island...

### Volcano

The volcano was implemented using a terrain with the laplacian on gaussian applied to it. In addition to that, perlin noise was also applied to it in order to make the terrain seem "bumpy" rather than flat. We have programmed the Perlin Noise ourselves in order not to have to include any additional libraries. For this we have:  
The perlin noise started from a certain offset and applied square root function. Other than its use on the terrain, it was used to simulate seashore details. !!

### Weather

The parameter heat schedules the weather on our island. We have two different time types 0 and 2. The parameter heat can also be counted to the interval  [0,2]   and in order to calculate the exact parameters of color choice and features we use the lerp function between the defined values for heat equal to 0,1,2. If heat is chosen equal to -1 then each time a parameter from [0,2] is chosen randomly.

- For the cold weather: The color choice is white and brown. The trees have branches like this. There are icebergs in the water.
- For the moderate weather:  The trees have leaves represented as cubes. The color choice is brown and green - the top of the volcano is white. The color of the objects is always calculated from the color of the material and the shininess.
- For the hot weather: the color choice is vivid green and vivid yellow. The volcano is brown and the trees have leaves that we have rendered with textures.

### Water and Lava

We have transparent water and lava in ambient color. Both are represented by shaders and we have calculated and applied normal maps. We can adjust the water height or lava height with parameters.

### Trees

The trees are displayed differently depending on the weather/time zone. In the cold time they have hierachical branches, in the middle temperature they have represented leaves as cubes and in the summer they have represented leaves with textures.

#### Leaves

The leaves in the moderate time zone are interpolated according to the season and adjust their color. In spring vivid green, in summer green, in autumn orange and in winter transparent.

### Skybox

The skybox was implemented by adding textures to a CubeMap. The textured CubeMap was implemented similar to the Textured Mesh; however, for the CubeMap, we are looping through the textures that are corresponding to each side of the cube, in addition to disabling then re-enabling the depth test in order to have the skybox be unaffected by the translation.
Moreover, two different skybox textures were created to simulate the day and night cycles. This is dependent on the chronogram's time of day as it seamlessly interpolates between day and night.

### Smoke

The smoke particle system follows a sinus function to move up. When the smoke reaches its maximum height, the particles restart. Each particle has different speeds and trajectories. The particles' colors are interpolated between white and black according to the time of day.

### Sun

The sun moves in a cycle around the x axis. So we can make a daily cycle and a yearly cycle on our island. The annual cycle has 364 days and day 0 is the first day of spring. The sun has a position (0,x) with bias x. This bias x increases to a positive x value in winter. So the sun is further away from the island and the sun, shadow sides change. In summer the sun is centered over the island. For the remaining values we interpolate over these two states. For the moderate climate we have a single bias, for the cold climate we have a double bias. Thus, we can use our heat parameter to represent the different climates and their changing solar irradiance. For the hot climate we have bias 0.

### Birds

The birds are equipped with a keyframe animation and move their wings within it, which we have implemented with the skeleton animation. TODO

## Configurations

## Technical Details

- We have implemented a decorater class to cache function output and not calculate it multiple times. We used it especially for the Perlin Noise.
- We have a MeshedNode class that we use for the trees, for example. This allows to link meshes and nodes more easily.
- In the file default.ini the simulation can be configured and the input parameters can be defined.
- Under sources/wrapper you will find all the given classes from the lecture
- Under sources/utils you will find some helping classes from us, mostly for calculation
- Under sources/objects you will find most of the features/objects like trees etc.

## Screenshots
