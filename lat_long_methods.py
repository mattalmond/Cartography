def latlong_to_xyz(coords, degrees=True, radius=6371):
    '''Return 3-vectors for position on the Earth.
    Input ndarray of shape (n, 2). Columns : 0=longitude, 1=latitude
    '''
    k = np.pi/180 if degrees else 1
    array = coords*k
    
    return np.c_[
        radius*np.cos(array[:,1])*np.cos(array[:,0]),
        radius*np.cos(array[:,1])*np.sin(array[:,0]),
        radius*np.sin(array[:,1])
    ]
    
    
def latlong_to_norths(coords, degrees=True):
    '''Return unit 3-vectors for the north direction on a sphere.
    Input ndarray of shape (n, 2). Columns : 0=longitude, 1=latitude
    '''
    k = np.pi/180 if degrees else 1
    array = coords*k
    return np.c_[
        np.cos(np.pi/2 + array[:,1])*np.cos(array[:,0]),
        np.cos(np.pi/2 + array[:,1])*np.sin(array[:,0]),
        np.sin(np.pi/2 + array[:,1])
    ]
    
    
def latlong_to_easts(coords, degrees=True):
    '''Return unit 3-vectors for the north direction on a sphere.
    Input ndarray of shape (n, 2). Columns : 0=longitude, 1=latitude
    '''
    k = np.pi/180 if degrees else 1
    array = coords*k
    return np.c_[
        np.cos(np.pi/2 + array[:,0]),
        np.sin(np.pi/2 + array[:,0]),
        0
    ]
    
    
def latlong_distances(A, B, degrees=True, radius=6371):
    '''Return spherical distance matrix on Earth.
    Input ndarrays of shape (a, 2), (b, 2). Columns : 0=longitude, 1=latitude
    Output ndarray of shape (a, b).
    
    distance = acos(sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon2-lon1))*6371
    '''
    k = np.pi/180 if degrees else 1
    arr_a = (A*k)[:,None,:]
    arr_b = (B*k)[None,:,:]
    
    sines    = np.sin(arr_a[:,:,1])*np.sin(arr_b[:,:,1])
    cosines  = np.cos(arr_a[:,:,1])*np.cos(arr_b[:,:,1])
    long_cos = np.cos(arr_b[:,:,0] - arr_a[:,:,0])
    argument = sines + cosines*long_cos
    return np.arccos(argument)*radius


def latlong_north_devs(A, B, degrees=True):
    '''Return matrix of angles between north vectors on a sphere.
    Input ndarrays of shape (a, 2), (b, 2). Columns : 0=longitude, 1=latitude
    Output ndarray of shape (a, b).
    
    '''    
    a_north  = latlong_to_norths(A, degrees=degrees)
    b_north  = latlong_to_norths(B, degrees=degrees)
    b_east   = latlong_to_easts( B, degrees=degrees)
    
    arg_1 = np.linalg.norm(np.cross(a_north[:,None,:], b_east[None,:,:]), axis=2)
    arg_2 = np.dot(a_north, b_east.T)
    
    return np.abs(np.arctan2(arg_1, arg_2) - np.pi/2)
    #return -np.arcsin(np.linalg.norm(np.cross(a_north[:,None,:], b_east[None,:,:]), axis=2))


def latlong_bearings(A, B, degrees=True):
    '''Return bearings matrix on a sphere.
    Input ndarrays of shape (a, 2), (b, 2). Columns : 0=longitude, 1=latitude
    Output ndarray of shape (a, b).
    
    bearing = arctan2(
        sin(lon2-lon1)*cos(lat2),
        cos(lat1)*sin(lat2) - sin(lat1)*cos(lat2)*cos(lon2-lon1)
    )
    '''
    k = np.pi/180 if degrees else 1
    arr_a = (A*k)[:,None,:]
    arr_b = (B*k)[None,:,:]
    
    arg_1  = np.sin(arr_b[:,:,0] - arr_a[:,:,0])*np.cos(arr_b[:,:,1])
    arg_2a = np.cos(arr_a[:,:,1])*np.sin(arr_b[:,:,1])
    arg_2b = np.sin(arr_a[:,:,1])*np.cos(arr_b[:,:,1])*np.cos(arr_b[:,:,0]-arr_a[:,:,0])
    
    return np.arctan2(arg_1, arg_2a - arg_2b)