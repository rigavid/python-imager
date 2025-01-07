from screeninfo import get_monitors

monitors = [m for m in get_monitors()]

class resolution:
    resolutions = [(m.width, m.height) for m in monitors]
    try: index = [m.is_primary for m in monitors].index(True)
    except: index = 0
    resolution = resolutions[index]
    def update():
        resolution.index = (resolution.index+1)%len(resolution.resolutions)
        resolution.resolution = resolution.resolutions[resolution.index]
    def update_resses():
        monitors = [m for m in get_monitors()]
        resolution.resolutions = [(m.width, m.height) for m in monitors]
        resolution.index = [m.is_primary for m in monitors].index(True)
        resolution.resolution = resolution.resolutions[resolution.index]
    def percentile(x, y):
        return [resolution.resolution[0]/100*x, resolution.resolution[1]/100*y]