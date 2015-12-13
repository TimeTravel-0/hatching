# hatching

 this is ugly, experimental, slow, unoptimized code.
 its purpose is to verify my (propably) stupid idea
 of an "image to hatching pen plotter drawing".
 The usual warning applies: I have no idea what I am doing.
 
 for now the script finds edges and fills areas in between with colors
 
 edge detection works as expected, but drawn edges
 (black lines...) are not handled in a special way
 = handled like a normal area/fill = results in double
 lines detected for comic like input drawings

 motion vector recovery works ok-ish.

 this script now generates lots of data from an image file
 
 next, yet unimplemented, step is to combine all this data
 and generate polygon lines

 another, yet unimplemented, part is to write all the polygons
 out in HPGL form.
