# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# import numpy as np
# from io import StringIO
# from flask import make_response
#
#
#
# def GetGraph(dataList, xIndex, yIndex):
#     dataArray = np.array(dataList)
#     x = dataArray[:, xIndex]
#     y = dataArray[:, yIndex]
#
#     fig = Figure()
#     ax = fig.add_subplot(1, 1, 1)
#     ax.plot(x, y, 'bo--')
#
#     canvas = FigureCanvas(fig)
#     output = StringIO()
#     canvas.print_png(output)
#     response = make_response(output.getvalue())
#     response.mimetype = 'image/png'
#     return response
