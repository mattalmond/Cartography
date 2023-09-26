def bbox(array):
    x_max, y_max = np.max(array, axis=0)
    x_min, y_min = np.min(array, axis=0)
    
    return np.array([x_min, x_max, y_min, y_max])


def collision(box_a, box_b):
    
    x_bool = (box_a[0] <= box_b[1]) & (box_b[0] <= box_a[1])
    y_bool = (box_a[2] <= box_b[3]) & (box_b[2] <= box_a[3])
    
    return x_bool & y_bool


def intersect(array, box):
    
    x_bool = (array[:,0] >= box[0]) & (array[:,0] <= box[1])
    y_bool = (array[:,1] >= box[2]) & (array[:,1] <= box[3])
    bools  = x_bool & y_bool
    if bools[0]:
        indx = np.where(~bools)[-1]+1
    else:
        indx = np.where(bools)[0][0]
    
    rolled_bools = np.roll(bools, -indx, axis=0)
    rolled_array = np.roll(array, -indx, axis=0)
    last_indx = np.where(rolled_bools)[0][-1]
    
    return rolled_array[:last_indx]