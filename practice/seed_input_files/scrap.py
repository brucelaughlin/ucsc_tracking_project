point_ij = [99999,99999]

for ii in range(np.shape(lon)[0]): 
    for jj in range(np.shape(lon)[1]):
        if lon[ii,jj] == points_in_box[0,pp] and lat[ii,jj] == points_in_box[1,pp]:
            point_ij = [ii,jj]
