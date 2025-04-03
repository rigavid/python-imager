# Pyimager
 Pyimager is a python package for creating, editing and showing images with python.  
 It can be used to create videogames (that's why I use it for) and to many other uses.

 As it is based on opencv-python but not all of these functions are implemented here, you can still use their functions with this library to get the best result of them. But still, open an issue on [GitHub](https://github.com/T-Sana/python-imager/issues) so I can add the functions you need.

# Tutorial
## Creating an image
To create an image you just need to proceed as following:
> `img = image(name="myImage")`

You can modify the parameters of this image specifying it's size, background color and name via the following function:
> `img = new_img(dimensions=[200, 500], background=COL.cyan, name="myImage")`  
Definition for an image of 200x500 pixels with a cyan background color with "myImage" as name.

You can also import a local image:
> `img = image(name="myLocalImage").open_img(path)`
## Showing an image (until gets a keypress)
To show an image just until you get a keypress:
> `img.show_(0)`

To add a timeout, define t as miliseconds before closing
> `img.show_(t)`  
If you want the image to be shown forever: set t to 0.

To get the key that has been pressed:
> `wk = img.show_(t)` wk comes from WaitKey, the cv2 function used by this library.
## Showing an image
To show an image, you should build it first even if you could use `image.show_()` to show the images without 'building' them.  
So, to properly show an image, proceed as following:
> `img = image()`  
> `img.build()`  
> `img.show()`  
You could use `img = image().build()` too if you prefer because `imag.build()` returns an `image`.
## Editing an image
To edit an image, you have to create one first:
> `img = image()` or `img = new_img()`

Then, you can modify your image using the inner functions of the `image` class.  
For drawing a diagonal line accross the image, you can do like this:
> `img.line(p1=[0, 0], p2=img.size(), colour=COL.red, thickness=5, lineType=2)`  
And like this you have a line going from `p1` (0, 0) to `p2` that are the coordinates of the bottom right of the image, the `colour` is red, the `thickness` of the line is 5px and, finally, the `lineType` is setted to 2.

You have 5 inner functions to draw shapes:
> - `image.line(p1, p2, colour, thickness, lineType)`
> - `image.rectangle(p1, p2, colour, thickness, lineType)`
> - `image.circle(ct, radius, colour, thickness, lineType)`
> - `image.ellipse(cr, (radius1, radius2), colour, thickness, lineType, startAngle, endAngle, angle)`
> - `image.polygon(pts:[pt], colour, thickness, lineType)`

And you have 2 inner functions more to write text:
> - `image.write(text, pt, colour, thickness, fontSize, font, lineType)`
> - `image.write_centered(text, ct, colour, thickness, fontSize, font, lineType)`

# Installation
> `pip install python-imager`