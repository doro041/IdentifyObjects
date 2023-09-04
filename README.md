# IdentifyObjects
Freshers Fayre AI society project

## config.json file
This file is used for configuring which images should be compared for differences.

Inside the root json object each set of images is laid out with a name of your choosing.
For each image set object, there should be a field named before which has the path to one image and another field called after which has the path of the other image.
There should also be the field num_differences which is the number of differences between the images. There should also be the field solutions.
The field solutions is an array of objects which can be empty but probably shouldn't be.
For each object:
There should be a field top_left which is an object with fields w and h where w is the x coord of the top left corner of the difference and y is the y coord
There should also be a field bottom_right which is an object like top_left but the coordinates are for the bottom right corner
The box defined should just cross the edge pixels of the difference
There should also be a field called score which holds the score gained for finding that difference. This cannot be larger than or equal to 1000000000 due to selecting the score for multiple differences in a selected area
