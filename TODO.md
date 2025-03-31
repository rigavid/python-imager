[ ] Check this out: https://packaging.python.org/en/latest/guides/modernize-setup-py-project/

[ ] Change resolution by backspace in built_in_functs in image.show_(self)

[x] Permit percentiles in coordinates arguments as image.rectangle([20%, 20%], [80%, 80%], COL.red, 0) -> use RES.percentile(x, y)

[ ] Voir pour implémenter ce code :
```
from PIL import Image
from cairosvg import svg2png
from io import BytesIO

def openSVG(path, height=None, width=None):
    img = new_img()
    with open(path, "r") as file:
        img.img = cv2.cvtColor(np.array(Image.open(BytesIO(svg2png(bytestring=file.read(), output_height=height, output_width=width))).convert('RGB')), cv2.COLOR_RGB2BGR)
    return img
```