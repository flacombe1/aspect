'''Create example NetCDF file

see https://unidata.github.io/netcdf4-python/ for more information

These are used in the ASPECT unit tests located in
./unit_tests/netcdf.cc to check that we can load files correctly.

'''

import netCDF4 as nc
import numpy as np
import pathlib



def cart():
    fn = 'test-3d-cartesian.nc'
    ds = nc.Dataset(fn, 'w', format='NETCDF4')

    # Write metadata attributes
    ds.title = 'Cartesian 3d example file'
    ds.source = ('generated by an example python script as part of github.com/geodynamics/aspect')

    print(f'\n\nInfo:\n{ds}')

    coord_x = [0., 1000., 2000.]
    coord_y = [500., 1000., 1500., 2000.]
    coord_z = [0., 300., 600., 700., 800.]
    n_x = len(coord_x)
    n_y = len(coord_y)
    n_z = len(coord_z)
    
    # Create dimensions.
    dims = [ds.createDimension('X', len(coord_x)),
            ds.createDimension('Y', len(coord_y)),
            ds.createDimension('Z', len(coord_z))]

    print('\n\Dimensions:\n')
    for dim in ds.dimensions.items(): print(dim)

    # variables or dimensions:
    data_x = ds.createVariable('X', np.float64, ('X'))
    data_x.units = 'm'
    data_y = ds.createVariable('Y', np.float64, ('Y'))
    data_y.units = 'm'
    data_z = ds.createVariable('Z', np.float64, ('Z'))
    data_z.units = 'm'
    
    # Create variables for each of the data columns. We give the
    # reverse ordering for the dimensions because this is what
    # ParaView expects (first dimension is Z, then Y, then X
    # regardless of name):
    data_1 = ds.createVariable('index', np.float64, ('Z','Y','X'))
    data_1.units = ''
    data_1.long_name = 'an index counting in lexicographic ordering'

    data_2 = ds.createVariable('depth', np.float64, ('Z','Y','X'))
    data_2.units = 'm'
    data_2.long_name = 'the depth of the point'
    
    print(f'\n\nVariables:\n{ds}'
      f'{data_1}\n'
      f'{data_2}\n')

    # coordinate data
    data_x[:] = coord_x
    data_y[:] = coord_y
    data_z[:] = coord_z

    # Column data, also indexed in reverse

    # Note: this looks wrong, but np.reshape() takes indices in reverse order as well
    data_1[:] = np.reshape(range(0, n_x*n_y*n_z), (n_z, n_y, n_x))
    
    for x in range(n_x):
        for y in range(n_y):
            data_2[:,y,x] = 800. - np.array(coord_z)

    # Finsh and close file
    ds.close()


cart()
