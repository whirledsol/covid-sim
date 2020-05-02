#!/usr/bin/env python3
"""
dynamic matplotlib slider
@author: whirledsol
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import collections

def start():
    test()

def test():
    def parabolic(xs,params):
        return (params['a']*xs)**(params['exp'])
    xs = np.arange(-1, 1, 0.001)
    options = {'a':[0,5,1],'exp':[1,4,1]}
    graph_slider(xs,parabolic,options)

def isList(item):
    return isinstance(item, (collections.Sequence, np.ndarray))

def graph_slider(xs,func,sliderOptions):
    '''
    func = function definition
    sliderOptions = {name1:[min1,max1,step1],name2:[min2,max2,step2],...}
    '''
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.25)
    ax.margins(x=0)

    state_init = {k:o[0]  for k, o in sliderOptions.items()}
    yss = func(xs,state_init)
    if not isList(yss[0]): yss = [yss]

    graphs = []
    for ys in yss:
        graph, = plt.plot(xs, ys, lw=2)
        graphs.append(graph)
    

    axcolor = 'lightgoldenrodyellow'

    
    sliders = {}
    sliderCount = 0
    for key,param in sliderOptions.items():
        sliderAxes = plt.axes([0.25, 0.1+sliderCount*0.05, 0.65, 0.03], facecolor=axcolor)
        sliders[key] = Slider(sliderAxes, key, param[0], param[1], valstep=param[2])
        sliderCount+=1

    def update(val):
        state = {k: s.val for k, s in sliders.items()}
        
        yss = func(xs,state)
        if not isList(yss[0]): yss = [yss]
        for i, graph in enumerate(graphs):
            graph.set_ydata(yss[i])
        fig.canvas.draw_idle()

    for slider in sliders.values():
        slider.on_changed(update)

    plt.show()

if  __name__ =='__main__':start()