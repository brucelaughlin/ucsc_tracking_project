#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 12:21:37 2023

@author: blaughli
"""
y = np.arange(np.shape(mask)[0])
x = np.arange(np.shape(mask)[1])
fig, ax = plt.subplots()
ax.pcolormesh(x,y,mask)
plt.title('rho')

y = np.arange(np.shape(mask_p)[0])
x = np.arange(np.shape(mask_p)[1])
fig, ax = plt.subplots()
ax.pcolormesh(x,y,mask_p)
plt.title('psi')

y = np.arange(np.shape(mask_u)[0])
x = np.arange(np.shape(mask_u)[1])
fig, ax = plt.subplots()
ax.pcolormesh(x,y,mask_u)
plt.title('u')

y = np.arange(np.shape(mask_v)[0])
x = np.arange(np.shape(mask_v)[1])
fig, ax = plt.subplots()
ax.pcolormesh(x,y,mask_v)
plt.title('v')
