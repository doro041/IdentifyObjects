# IdentifyObjects
Freshers Fayre AI society project

## config.json file
This file serves as a configuration document for specifying the criteria for comparing images to detect disparities.

Within the primary JSON object, each collection of images is organized with a user-defined name. For each image set object, two essential fields must be included: "before," which denotes the path to one image, and "after," which designates the path to another image. Additionally, there should be a field labeled "num_differences" representing the count of discrepancies observed between the images. Furthermore, the document should encompass a "solutions" field, which takes the form of an array of objects. While this array can be empty, it is advisable to provide content.

For each object within the "solutions" array, certain key attributes are expected:

    "top_left": This is an object containing the fields "w" and "h," where "w" represents the x-coordinate of the top-left corner of the difference, and "h" denotes the y-coordinate of the same corner.

    "bottom_right": Similar to "top_left," this is an object with "w" and "h" fields, specifying the coordinates of the bottom-right corner of the difference. It's important to note that the defined rectangle should encompass the edge pixels of the observed difference.

    "score": This field holds the score assigned for detecting the respective difference. It's crucial to ensure that this score does not exceed or equal 1,000,000,000, considering that multiple differences within a selected area are evaluated in terms of their scores.
