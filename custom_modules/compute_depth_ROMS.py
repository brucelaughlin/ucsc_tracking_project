#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copied from:
    
raphaeldussin/compute_depth_ROMS.py
"""


def compute_depth_layers(ds, grid, hmin=0.1):
    """ compute depths of ROMS vertical levels (Vtransform = 2) """
    
    # compute vertical transformation functional
    S_rho = (ds.hc * ds.s_rho + ds.Cs_r * ds.h) / (ds.hc + ds.h)
    S_w = (ds.hc * ds.s_w + ds.Cs_w * ds.h) / (ds.hc + ds.h)
    
    # compute depth of rho (layers) and w (interfaces) points
    z_rho = ds.zeta + (ds.zeta + ds.h) * S_rho
    z_w = ds.zeta + (ds.zeta + ds.h) * S_w
    
    # transpose arrays and fill NaNs with a minimal depth
    ds['z_rho'] = z_rho.transpose(*('time', 's_rho','yh','xh'),
                                  transpose_coords=False).fillna(hmin)
    
    ds['z_w'] = z_w.transpose(*('time', 's_w','yh','xh'),
                                  transpose_coords=False).fillna(hmin)
    
    # interpolate depth of levels at U and V points
    ds['z_u'] = grid.interp(ds['z_rho'], 'X', boundary='fill')
    ds['z_v'] = grid.interp(ds['z_rho'], 'Y', boundary='fill')
    
    # compute layer thickness as difference between interfaces
    ds['dz'] = grid.diff(ds['z_w'], 'Z')
    
    # add z_rho and z_w to xarray coordinates
    ds = ds.set_coords(['z_rho', 'z_w', 'z_v', 'z_u'])
    
    return ds
