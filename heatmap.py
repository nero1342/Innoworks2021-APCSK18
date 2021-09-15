from ipywidgets.embed import embed_minimal_html
import gmaps
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import time 

gmaps.configure(api_key='AIzaSyCgr9wEU9berFkrhCNewwBAMRgz8uF1c1I')

def heatmap2html(html_file, locations):
    """
    Visualize heatmap base on location points and export to html file

    Params:
    - (str) fname: name of exported html file
    - (list) locations: include list of (latitude, longtitude) pairs
    """

    fig = gmaps.figure()

    for location, value in locations:
        heatmap = gmaps.heatmap_layer(location)
        heatmap.point_radius = value
        fig.add_layer(heatmap)

    embed_minimal_html(html_file, views=[fig])

def heatmap2png(png_file, locations):
    """
    Visualize heatmap base on location points and export to html file

    Params:
    - (str) png_file: name of exported png file
    - (list) locations: include list of (latitude, longtitude) pairs
    """
    print("Start")
    # heatmap2html
    html_file = png_file.split('.')[0] + '.html'

    fig = gmaps.figure()

    for location, value in locations:
        heatmap = gmaps.heatmap_layer(location)
        heatmap.point_radius = value
        fig.add_layer(heatmap)

    embed_minimal_html(html_file, views=[fig])

    # html2png
    options = Options()
    options.headless = True
    root_path = os.path.dirname(os.path.realpath(__file__)) # directory contains this python file
    driver = webdriver.Firefox(options=options, executable_path='./geckodriver')
    print('file://' + os.path.join(root_path, html_file))
    driver.get('file:////' + os.path.join(root_path, html_file))
    while True:
        elements = driver.find_elements_by_class_name('dismissButton')
        if len(elements) == 0:
            continue 
        for e in elements:
            e.click()
        print(len(elements))
        driver.save_screenshot(png_file)
        driver.quit()
        break 

    print('Finish')

def genRelatedPoints(pt):
    dir =[random.randint(0, 1) * 2 - 1, random.randint(0, 1) * 2 - 1]
    n = random.randint(1, 1)
    cur = pt 
    total = []
    for i in range(n):
        total.append(cur)
        cur = (cur[0] + random.uniform(0, 1) / 1000 * dir[0], cur[1] + random.uniform(0, 1)/ 1000 * dir[1])
    return total


# pts = [(10.762913,106.6821717), (10.765913,106.6524717), (10.7739789,106.6880888), (10.7735451,106.6637059),
#         (10.7586745,106.6317317), (10.744487,106.6390273), (10.7643547,106.66642), (10.7338196,106.6511723),
#         (10.7986166,106.6576985), (10.8164056,106.6637925)
#         # (10.7752692,106.6929486),
# ]

# random.seed(12345678)

# total = []
# for pt in pts:
#     dir =[random.randint(0, 1) * 2 - 1, random.randint(0, 1) * 2 - 1]
#     print(dir)
#     n = random.randint(1, 5)
#     cur = pt 
#     for i in range(n):
#         total.append(cur)
#         cur = (cur[0] + random.uniform(0, 1) / 1000 * dir[0], cur[1] + random.uniform(0, 1)/ 1000 * dir[1])
#         print(cur)
        
# heatmap2png("out.png", total)
# heatmap_to_html("out.html", [(10.762913,106.6821717), (10.765913,106.6524717), (10.765913,106.6529717), (10.765313,106.6511717), (10.764313,106.6501717)])



