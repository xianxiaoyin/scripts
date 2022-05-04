'''
Date: 2021-12-09 21:04:25
LastEditors: xianxiaoyin
LastEditTime: 2022-05-04 09:25:52
FilePath: \learn\scripts\mhxy.py
'''
# -*- encoding: utf-8 -*-
'''
@File: 		   t.py
@Descriptions: 
@Date: 		   2022-03-26 10:48:44
@Author: 	   xianxiaoyin
'''
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.imread(r'D:\learn\scripts\mhxy.png', 0)
print(img)
img2 = img.copy()
template = cv.imread(r'D:\learn\scripts\dl.png', 0)
w, h = template.shape[::-1]
# All the 6 methods for comparison in a list
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
           'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
for meth in methods:
    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    res = cv.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img, top_left, bottom_right, 255, 2)
    plt.subplot(121), plt.imshow(res, cmap='gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img, cmap='gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()
