# Installation and importation
> `pip install python-imager`
```
import pyimager
```

# Pyimager
 Pyimager is a python package for creating, editing, showing and saving images with python.

 As it is based on opencv-python but not all of these functions are implemented here, you can still use their functions with this library to get the best result of them. But still, open an issue on [GitHub](https://github.com/rigavid/python-imager/issues) if you would like me to implement functions you need.

 I would be so happy if you request or propose any modification of this package :-)

# Images
## Creating an image
To create an image you just need to proceed as following:
```
img = image()
```
You can modify the parameters of this image specifying it's size, background color and name via the following function:
> `img = new_img(dimensions=[200, 500], background=COL.cyan, name="myImage")`  
Definition for an image of 200x500 pixels with a cyan background color with "myImage" as name.

You can also import a local image:
```
img = image(name="myLocalImage").open_img(path)
```
## Showing an image (until gets a keypress)
To show an image just until you get a keypress:
```
img.show_(0)
```

To add a timeout, define t as miliseconds before closing:
```
img.show_(t)
```
If you want the image to be shown forever: set t to 0.

To get the key that has been pressed:
```
wk = img.show_(t)
```
I use wk for WaitKey, as it's the cv2 function called by this function.

## Showing an image
To show an image, you should build it first, even if you could use `image.show_()` to show the images without 'building' them, this way is cleaner than the previos one.
So, to properly show an image, proceed as following:
```
img = new_img()
img.build()
while img.is_opened():
    img.show()
```

You can use `img = image().build()` too if you prefer as `image.build()` returns itself as an `image`.  
Neverthmore I recommend to build it later if you want to modify it before showing it.

## Closing an image
Though you can close the window with key `esc`, you can also close it with `image.close()`.  
> Even if it may not seem useful right now, you can combine it to a `button`'s function to create a close button. _cf_. <a href="#buttons">Buttons</a>.


## Editing an image
To edit an image, we'll stick with the empty basic image:
> `img = image()` or `img = new_img()`

Then, you can modify your image using inner functions of the `image` class.


You have 5 inner functions to draw shapes:
1. `image.line(p1, p2, colour, thickness, lineType)`
2. `image.rectangle(p1, p2, colour, thickness, lineType)`
3. `image.circle(ct, radius, colour, thickness, lineType)`
4. `image.ellipse(cr, (radius1, radius2), colour, thickness, lineType, startAngle, endAngle, angle)`
5. `image.polygon(pts:[pt], colour, thickness, lineType)`

And you have 3 inner functions more to write text:
1. `image.text(text, ct, col, thickness, fontsize, ...)`
2. `image.write(text, pt, colour, thickness, fontSize, font, lineType)`
3. `image.write_centered(text, ct, colour, thickness, fontSize, font, lineType)`

To draw a diagonal line accross the image, you can do as follows:
```
img.line(p1=[0, 0], p2=img.size(), colour=COL.red, thickness=5, lineType=2)
```
You now have a line going from `p1` (0, 0) to `p2` (bottom right), of red `colour`, `thickness` of 5px and the `lineType` is setted to 2 (there's 0, 1 and 2).

> To use colors, use `COL`.  
You can either chose a color in col defined as a `CSS` color name (camelBack written) or using hexadecimal RGB with  `COL.new("#xxxxxx")` to use a custom color.

## Coordinates
The top-left of the image is at `[0, 0]` (XY coordinates).

### Define a point
Define a var of type `list` or `tuple` of len 2. Values may be `int` or `float`.

### Function with points
There are some useful functions to manipulate coordinates:

1. `ct_sg(p1, p2)`  
Standing for center of segment from p1 to p2, returns the point at the center of the segment.
2. `pt_sg(p1, p2, m1, m2)`  
Standing for point in segment p1, p2, does as `ct_sg()` but you can define `m1` and `m2` to increase the weight of the sides to approach to an end.
3. `ct_cr(p1, p2, p3, p4)`  
Stands for _centre carré_, returns the center of a parallelogram.
4. `coosCircle(ct, radius, angle)`  
Gets the coordinates as if you were using a compass, from the `ct` to a distance of `radius` to an `angle`.
5. `coosEllipse(ct, radiuses, angle, rotation)`  
Similar to `coosCircle()`, works for elipses.
6. `dist(p1, p2)`  
Returns the distance of two points in `float`.

## Buttons
To add buttons to your images, you can use the sub-class `image.button_` using `image.button()`.

Defining a button:
```
button = image.button(name, coos)
button.on_click(funct, params)
```
Pass a function to the button to execute when clicked on.
> Use params if you have variables to give to your funct.
### Removing buttons
Use `image.remove_button()`
`button = image.button(name, coos)`
```
image.remove_button(button)
```
> You will have to rewrite the image if you want the button to disapear.  
To do so, I would recomend you to copy the image with `image.copy()` before creating your button and restoring the copy of the image after deleting the button.

## Trackbars
To add trackbars to your images, you can use the sub-class `image.trackbar_` using `image.trackbar()`.

Defining a trackbar:
```
trackbar = image.trackbar(name, coos, min, max, val)
```
### Removing trackbars
Use `image.remove_trackbar()`
```
trackbar = image.trackbar(name, coos, min, max, val)
image.remove_trackbar(trackbar)
```
> You will have to rewrite the image if you want the trackbar to disapear.  
For more info, _cf_. <a href="#removing-buttons">_Removing buttons_</a>

## Access mouse info
Whenever the mouse is on your python window, you can get info about the mouse using `image.mouse.get()`.

```
event, x, y, flags = image.mouse.get()
```
Events are cv2 defined events, _cf_. <a href="https://docs.opencv.org/4.x/d0/d90/group__highgui__window__flags.html#ga927593befdddc7e7013602bca9b079b0">cv2 events</a>.  
x and y are the position of the mouse on the window.  
Flags are cv2 defined events, _cf_. <a href="https://docs.opencv.org/4.x/d0/d90/group__highgui__window__flags.html#gaab4dc057947f70058c80626c9f1c25ce">cv2 flags</a>.

# Layouts
Layouts are deprecated it's been a while since i've taken a glance on them.