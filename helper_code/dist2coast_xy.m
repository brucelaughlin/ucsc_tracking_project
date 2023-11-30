function dist2cst=dist2coast_xy(x,y,lonr,latr,maskr,lonc,latc);
% dist2coast_xy: finds the shortest distance to coast 
%                (defined by a coastline) using ROMS grid x,y values
%
% SYNTAX
% ------
% dist2cst=dist2coast_xy(x,y,lonr,latr,maskr,lonc,latc);
%
% where x,y are the x/y points of the grid
%       lonr,latr are the lon/lat points of the grid (corresponding to x/y)
%       maskr is the mask of the grid (used to only find dist for ocean points
%       lonc,latc define the coastline (can and should probably have NaNs in it)
%  and  dist2cst is what's returned (in units of x/y)
%
% Chris Edwards		                          June 2018

% get cells that have coastline in them
[ni,nj]=size(x);

% get x/y coords of coastline
xc=griddata(lonr,latr,x,lonc,latc);
yc=griddata(lonr,latr,y,lonc,latc);

dist2cst=NaN*zeros([ni nj]);

% find minimum distance to that set of coastlines
[iocean,jocean]=find(maskr==1);
nocean=length(jocean);
for kocean=1:nocean
  j0=jocean(kocean);
  i0=iocean(kocean);
  x0=x(i0,j0);
  y0=y(i0,j0);
  distx=x0-xc;
  disty=y0-yc;
  distt = sqrt(distx.*distx+disty.*disty);
  dist2cst(i0,j0)=min(distt);
end

return
