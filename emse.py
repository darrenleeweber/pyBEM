#!/usr/bin/env python

"""
A module to work with EMSE/MRVU data, from the source signal imaging
company.

For example:

import emse
# read and display an EMSE wireframe
test_file = 'mesh_emse_mrev4_scalp.wfr'
test_wfr = emse.wfr()
test_wfr.read(test_file)
test_wfr.view()


-----------------------------------------------------------------------------------
Licence: GNU GPL, no express or implied warranties

Copyright (C) 2007 Darren L. Weber

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
USA.

"""

import pdb

import os

#import numpy
import vtk


ver = '$Revision: 1.1 $ $Date: 2007/12/27 00:21:20 $'


class reg:
    """
    A class to work with EMSE registration data.
    """
    def __init__(self):
        pass
    def read(self, file):
        "read a registration file (*.reg)"
        pass
    def write(self, file):
        "write a registration file (*.reg)"
        pass


## function [reg] = emse_read_reg(file)

## % emse_read_reg - Read EMSE/MRVU coregistration matrices
## %
## % [reg] = emse_read_reg(file)
## %
## % reg is a struct with the following fields:
## %
## % reg.translation - the translation in meters along the
## %                   x, y and z axes respectively, from
## %                   the MRI image frame to head/elec frame.
## %
## % reg.rotation - The rotation vector contains the angles
## %                (in radians) about the x, y and z axes,
## %                also from the MRI image frame to the
## %                head/elec frame.
## %
## % reg.elec2mri - 'HeadToImageMatrix' is the 4 x 4 matrix
## %                containing the electrode to MRI translation and
## %                rotation transformations in homogeneous coordinates:
## %                * the upper left 3 x 3 submatrix is rotations
## %                  around z, y, x in that order;
## %                * the rightmost 3 x 1 column is a projection
## %                  vector (all zeros here);
## %                * the bottom 1 x 3 row is a translation vector,
## %                  equal to -1 * reg.translation here; and
## %                * the bottom right (1 x 1) scalar is the
## %                  homogenous scale unit, usually 1
## %
## % reg.mri2elec - 'ImageToHeadMatrix' is the inverse of elec2mri,
## %                ie, reg.mri2elec = inv(reg.elec2mri).
## %
## % This function also reads the fiducial points and the electrode
## % coordinates from the registration file, they are returned into:
## % reg.RPA, reg.LPA, reg.NAS, reg.Helec, and reg.Melec.  Each of
## % the fiducial structs (RPA,LPA,NAS) contains the electrode
## % fiducials in the head space (Hh) and the MRI space (Hm), plus the
## % MRI fiducials in the head space (Mh) and the MRI space (Mm).
## %
## % The transformation matrices (T) multiply a column vector, so that
## % [x', y', z', 1] = [x, y, z, 1] * T;
## % where x',y',z' are in the other coordinate system. For example,
## % MRI coordinates into head space:
## % tmp = [ reg.Melec ones(size(reg.Melec,1),1) ] * reg.mri2elec;
## % Note reg.Helec ~= tmp(:,1:3) due to floating point rounding only.
## % Similarly, head space (electrodes) into MRI coordinates:
## % tmp = [ reg.Helec ones(size(reg.Helec,1),1) ] * reg.elec2mri;
## % Note reg.Melec ~= tmp(:,1:3) due to floating point rounding only.
## %
## % EMSE Note: The origin in the head frame is at or near the center of
## % the skull, while the origin in the image frame is located at the
## % bottom right front corner of the bounding box (and so would be
## % located at the upper left corner of the first axial slice as
## % displayed by MR Viewer).
## %
## % A useful chapter on homogeneous coordinates, among other things,
## % may be found in Mortenson, M. (1985, Chpt. 8), Geometric Modelling,
## % New York: John Wiley & Sons.
## %


## % $Revision: 1.1 $ $Date: 2007/12/27 00:21:20 $

## % Licence:  GNU GPL, no express or implied warranties
## % History:  06/2002, Darren.Weber@flinders.edu.au
## %           09/2002, Darren.Weber@flinders.edu.au
## %                    - transposed HeadToImageMatrix so it
## %                      can be used as described above
## %                    - added reading of most other fields
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


## if ~exist('file','var'),
##     fprintf('No input file - see help open_emse_reg\n');
##     return;
## end

## [path,name,ext] = fileparts(file);
## file = fullfile(path,[name ext]);

## [fid,msg] = fopen(file,'r');
## if ~isempty(msg), error(msg); end

## fprintf('EMSE_READ_REG: Reading registration data...');
## tic
## fid = fopen(file,'r','ieee-le');
## reg = read_reg(fid);
## fclose(fid);
## t = toc;
## fprintf('done (%6.2f sec).\n',t);

## return

## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## function [reg] = read_reg(fid)

## while 1,
##     text = fgetl(fid);
##     if ~ischar(text), break, end

##     if strmatch('Offset',text),
##         % Offset is the translation in meters along the x, y and z axes
##         % respectively, from the MRI image frame to head/elec frame.
##         text = strrep(text,sscanf(text,'%c',8),'');
##         text = strrep(text,']','');
##         text = strrep(text,',','');
##         reg.translation = sscanf(text,'%f')';
##     end
##     if strmatch('Rotation',text),
##         % The Rotation vector contains the angles (in radians) about
##         % the x, y and z axes, also from the MRI image frame to the
##         % head/elec frame.
##         text = strrep(text,sscanf(text,'%c',10),'');
##         text = strrep(text,']','');
##         text = strrep(text,',','');
##         reg.rotation = sscanf(text,'%f')';
##     end
##     if strmatch('HeadToImageMatrix',text),
##         reg.elec2mri = zeros(4,4);
##         for i=1:4,
##             text = fgetl(fid);
##             reg.elec2mri(i,:) = sscanf(text,'%f')';
##         end
##         % The emse matrix requires transposition
##         reg.elec2mri = reg.elec2mri';
##         % It is more accurate to do this:
##         reg.mri2elec = inv(reg.elec2mri);
##     end
##     % See inverse calculation above to get reg.mri2elec
##     %if strmatch('ImageToHeadMatrix',text),
##     %    reg.mri2elec = zeros(4,4);
##     %    for i=1:4,
##     %        text = fgetl(fid);
##     %        reg.mri2elec(i,:) = sscanf(text,'%f')';
##     %    end
##     %    % The emse matrix requires transposition
##     %    reg.mri2elec = reg.mri2elec';
##     %end

##     % The coordinates of the three fiducials are given in both frames.
##     % For example, Head lists the fiducial coordinates (taken from the
##     % electrode data) in the head frame, while Head' are the fiducial
##     % coordinates from the image data expressed in the head frame.
##     % Similarly, Image lists the fiducial coordinates from the image
##     % data in the image frame while Image' lists those from the electrode
##     % data in the image frame. The two sets of numbers should be close but
##     % not identical.

##     if strmatch('RPA',text,'exact'),
##         format = '%7c %f %f %f';
##         % Read the Right Preauricular coordinates
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.RPA.Hh = tmp(8:10);
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.RPA.Mh = tmp(8:10);
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.RPA.Mm = tmp(8:10);
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.RPA.Hm = tmp(8:10);
##     end

##     if strmatch('LPA',text,'exact'),
##         format = '%7c %f %f %f';
##         % Read the Left Preauricular coordinates
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.LPA.Hh = tmp(8:10);
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.LPA.Mh = tmp(8:10);
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.LPA.Mm = tmp(8:10);
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.LPA.Hm = tmp(8:10);
##     end

##     if strmatch('Nasion',text,'exact'),
##         format = '%7c %f %f %f';
##         % Read the Nasion coordinates
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.NAS.Hh = tmp(8:10);
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.NAS.Mh = tmp(8:10);
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.NAS.Mm = tmp(8:10);
##         text = fgetl(fid);
##         tmp = sscanf(text,format)';
##         reg.NAS.Hm = tmp(8:10);
##     end

##     % The Electrode Positions block lists the coordinates (x, y, and z)
##     % first in the head frame and then in the image frame.
##     if strmatch('Electrode Positions',text),
##         reg.Helec = zeros(1,3);
##         reg.Melec = zeros(1,3);
##         n = 1;
##         while n < 400,
##             % Read the Head space coordinates
##             text = fgetl(fid);
##             if isempty(text), break; end
##             tmp = sscanf(text,'%f : %f %f')';
##             reg.Helec(n,1:3) = tmp(2:4);
##             % Read the MRI space coordinates
##             text = fgetl(fid);
##             tmp = sscanf(text,'%s %f %f %f')';
##             reg.Melec(n,1:3) = tmp(2:4);
##             n = n + 1;
##         end
##     end

## end

## % Create essential fiducial marker matrices
## % The order of these points in the matrices is very
## % important if they are used for coregistration
## reg.fiducials.head = [ reg.NAS.Hh; reg.RPA.Hh; reg.LPA.Hh ];
## reg.fiducials.mri  = [ reg.NAS.Mm; reg.RPA.Mm; reg.LPA.Mm ];


## return


class wfr:
    """
    A class to work with EMSE wireframe data.
    """
    
    def __init__(self):
        
        #self.face = numpy.array(0, dtype='double', order='C', ndmin=2)
        
        self.vert = {
            'index': [],
            'address': [],
            'channel_index': [],
            'xyz': [],
            'normal': [],
            'potential': [],
            'curvature': []
            }
        
        self.face = {
            'index': [],
            'address': [],
            'solid_angle': [],
            'magnitude': [],
            'potential': [],
            'area': [],
            'center': [],
            'normal': [],
            'vertex': [],
            'edge': []
            }
        
        self.edge = {
            'index': [],
            'address': [],
            'vertex': []
            }
        
    def read(self, file_name, options = ['vertex','face','edge']):
        """
        emse.wfr.read - read EMSE wireframe file (.wfr)
        
        emse.wfr.read(file_name,[options])
        
        The wfr class contains values for the vertices, faces, edges,
        and the mesh_type.  All coordinate values are in meters.
        
        'options' is a list of strings.  By default it contains
        options = ['vertex','face','edge'].  By default, this routine
        reads all available data from the emse file.  If 'options' is
        given, only the data type specified is returned.
        
        mesh_type is: 'unknown','scalp','outer skull','inner skull',
        or 'cortex'.
        
        space - 'hspace' for head space (electrodes)
                'vspace' for MRI volume space
        """
        
        print '\nemse.wfr.read [v%s]' % ver[11:15].strip()
        
        # reset all the wfr data structures, in case they already hold
        # data from another file
        self.__init__()
        
        # first read the data using python (numpy?), then allocate the
        # data into vtk.vtkPolyData - how do we do this?
        
        file_name = os.path.normpath(file_name)
        file_name = os.path.realpath(file_name)
        if not os.path.isfile(file_name):
            raise ValueError, 'file_name is not a file'
        else:
            self.file_name = file_name
            basename = os.path.basename(file_name)
            print '...reading: %s' % basename
        
        fid = open(file_name, 'r')
        
        # ------------------------------------------
        # Read prolog
        
        [version, file_type] = fid.readline().split()
        self.version   = int(version)
        self.file_type = int(file_type)
        [minor_revision,] = fid.readline().split()
        self.minor_revision = int(minor_revision)
        
        print '...WFR version = %d' % self.version
        print '...WFR file-type = %d' % self.file_type
        print '...WFR minor_revision = %d' % self.minor_revision
        
        if not(self.file_type == 4000 or self.file_type == 8000):
            msg = 'cannot read WFR file type: %d' % self.file_type
            raise ValueError, msg
        
        # ------------------------------------------
        # Read header (format depends on minor revision)
        
        if self.minor_revision == 3:
            [mesh_type_num,] = fid.readline().split()
            mesh_type_num = int(mesh_type_num)
        else:
            if minor_revision == 1:
                [radius, vert_num, face_num, edge_num] = fid.readline().split()
                mesh_type_num = 0
            else:
                [radius, vert_num, face_num, edge_num, mesh_type_num] = fid.readline().split()
                mesh_type_num = int(mesh_type_num)
            
            radius = float(radius)
            vert_num = int(vert_num)
            face_num = int(face_num)
            edge_num = int(edge_num)
            
            print '...average radius = %f meters' % radius
            print '...mesh file contains:'
            print '...%d vertices' % vert_num
            print '...%d faces' % face_num
            print '...%d edges' % edge_num
        
        if self.minor_revision == 1:
            mesh_type = 'unknown'
        else:
            if mesh_type_num >= 80000:
                mesh_space = 'vspace' # MRI "volume space"
                mesh_type_num = mesh_type_num - 80000
            else:
                mesh_space = 'hspace' # electrode "head space"
            
            if mesh_type_num == 0:
                mesh_type = 'unknown'
            elif mesh_type_num in [ 64,  40]:
                mesh_type = 'scalp'
            elif mesh_type_num in [128,  80]:
                mesh_type = 'outer skull'
            elif mesh_type_num in [256, 100]:
                mesh_type = 'inner skull'
            elif mesh_type_num in [512, 200]:
                mesh_type = 'cortex'
            else:
                mesh_type = 'unknown'
        
        print '...mesh type: %s' % mesh_type
        print '...mesh space: %s' % mesh_space
        
        self.mesh_type = mesh_type
        self.mesh_type_num = mesh_type_num
        self.mesh_space = mesh_space
        
        # ------------------------------------------
        # Read data (format depends on minor revision)
        
        if self.minor_revision == 3:
            
            # Read the whole file
            print '...reading minor revision %d data' % self.minor_revision,
            lines = fid.readlines()
            fid.close()
            print '...done'
            
            # strip all the new-line characters
            lines = [s.rstrip() for s in lines]
            
            if 'vertex' in options:
                print '...creating vertex array',
                
                for line in lines:
                    if 'v' in line:
                        v = line.split()[1:4]
                        v = [float(x) for x in v]
                        self.vert['xyz'].append(v)
                print '...done'
                
                vert_num = len(self.vert['xyz'])
                self.vert['index'] = range(vert_num)
                
            else:
                print '...skipping vertices'
            
            # Faces
            if 'face' in options:
                print '...creating face array',

                for line in lines:
                    if 't' in line:
                        f = line.split()[1:4]
                        f = [int(x) for x in f]
                        self.face['vertex'].append(f)
                print '...done'
                
                face_num = len(self.face['vertex'])
                self.face['index'] = range(face_num)
                
                # calculate these values?
                # 'solid_angle',
                # 'center',
                # 'area',
                # 'normal',
                # 'edge',
                
            else:
                print '...skipping faces'
            
            # Edges
            print '...there are no edges for minor revision 3'
            
            del lines
        
        elif self.minor_revision in [1,2]:
            
            print '...reading minor revision %d data' % self.minor_revision
            
            if 'vertex' in options:
                
                print '...reading %d vertices' % vert_num,
                
                for key in ['index','address','channel_index',
                            'xyz','normal','potential','curvature']:
                    self.vert[key] = range(vert_num)
                
                for i in range(vert_num):
                    
                    line = fid.readline() # discard empty line
                    
                    line = fid.readline()
                    line = line.split()
                    #self.vert['index'][i] = int(line[0])
                    self.vert['address'][i] = line[1]
                    self.vert['channel_index'][i] = int(line[2])
                    self.vert['xyz'][i] = [float(x) for x in line[4:7]]
                    
                    line = fid.readline()
                    line = line.split()
                    self.vert['normal'][i] = [float(x) for x in line[1:4]]
                    
                    line = fid.readline()
                    line = line.split()
                    self.vert['potential'][i] = float(line[0])
                    self.vert['curvature'][i] = float(line[1])
                
            else:
                
                print '...skipping %d vertices' % vert_num,
                
                # define an empty vert dictionary
                for key in ['index','address','channel_index',
                            'xyz','normal','potential','curvature']:
                    self.vert[key] = []
                
                # read enough lines to skip all the vertex data
                for i in range(vert_num):
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
            
            print '...done'
            
            #-------------------------------------
            if 'face' in options:
                
                print '...reading %d faces' % face_num,
                
                for key in ['index','address','solid_angle',
                            'magnitude','potential','area',
                            'center','normal','vertex','edge']:
                    self.face[key] = range(face_num)
                
                for i in range(face_num):
                    line = fid.readline() # discard empty line
                    line = fid.readline()
                    line = line.split()
                    #self.face['index'][i] = int(line[0])
                    self.face['address'][i] = line[1]
                    self.face['solid_angle'][i] = float(line[2])
                    self.face['magnitude'][i] = float(line[3])
                    self.face['potential'][i] = float(line[4])
                    self.face['area'][i] = float(line[5])
                    line = fid.readline()
                    line = line.split()
                    self.face['center'][i] = [float(x) for x in line]
                    line = fid.readline()
                    line = line.split()
                    self.face['normal'][i] = [float(x) for x in line]
                    line = fid.readline() # discard empty line
                    line = fid.readline()
                    line = line.split()
                    self.face['vertex'][i] = line[0:3]
                    self.face['edge'][i] = line[3:7]
                print '...done'
                
                print '...converting face vertices from address to index',
                for i in range(face_num):
                    for j in range(3):
                        a = self.face['vertex'][i][j]
                        if a in self.vert['address']:
                            self.face['vertex'][i][j] = self.vert['address'].index(a)
                        else:
                            raise ValueError, 'face vertex address is not in vert[''address'']'
                print '...done'
                
            else:
                
                print '...skipping %d faces' % face_num
                
                # define an empty face dictionary
                for key in ['index','address','solid_angle',
                            'magnitude','potential','area',
                            'center','normal','vertex','edge']:
                    self.face[key] = []
                
                for i in range(face_num):
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
                print '...done'
                
            #-------------------------------------
            if 'edge' in options:
                
                print '...reading %d edges' % edge_num,
                
                for key in ['index','address','vertex']:
                    self.edge[key] = range(edge_num)
                
                line = fid.readline()   # discard empty line
                for i in range(edge_num):
                    line = fid.readline()
                    line = line.split()
                    #self.edge['index'][i] = int(line[0])
                    self.edge['address'][i] = line[1]
                    self.edge['vertex'][i] = line[2:4]
                print '...done'
                
                print '...converting edge vertices from address to index',
                for i in range(edge_num):
                    for j in range(2):
                        a = self.edge['vertex'][i][j]
                        if a in self.vert['address']:
                            self.edge['vertex'][i][j] = self.vert['address'].index(a)
                print '...done'
                
                print '...converting face edges from address to index',
                for i in range(face_num):
                    for j in range(3):
                        a = self.face['edge'][i][j]
                        if a in self.edge['address']:
                            self.face['edge'][i][j] = self.edge['address'].index(a)
                        else:
                            raise ValueError, 'face edge address is not in edge[''address'']'
                print '...done'
                
            else:
                
                print '...skipping %d edges' % edge_num,
                
                for key in ['index','address','vertex']:
                    self.edge[key] = []
                
                line = fid.readline()   # discard empty line
                for i in range(edge_num):
                    line = fid.readline()
                print '...done'
            
        elif self.minor_revision == 4:
            
            print '...reading minor revision 4 data'
            
            if 'vertex' in options:
                
                print '...reading %d vertices' % vert_num,
                
                for key in ['index','channel_index',
                            'xyz','normal','potential','curvature']:
                    self.vert[key] = range(vert_num)
                
                for i in range(vert_num):
                    line = fid.readline() # discard empty line
                    line = fid.readline()
                    line = line.split()
                    #self.vert['index'][i] = i
                    self.vert['channel_index'][i] = int(line[0])
                    self.vert['xyz'][i] = [float(x) for x in line[2:5]]
                    line = fid.readline()
                    line = line.split()
                    self.vert['normal'][i] = [float(x) for x in line[1:4]]
                    line = fid.readline()
                    line = line.split()
                    self.vert['potential'][i] = float(line[0])
                    self.vert['curvature'][i] = float(line[1])
                print '...done'
                
                # Should we create the address list here?
                
            else:
                
                print '...skipping %d vertices' % vert_num,
                
                for key in ['index','channel_index',
                            'xyz','normal','potential','curvature']:
                    self.vert[key] = []
                
                for i in range(vert_num):
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
                print '...done'
                
            if 'face' in options:
                
                print '...reading %d faces' % face_num,
                
                for key in ['index','solid_angle',
                            'magnitude','potential','area',
                            'center','normal','vertex','edge']:
                    self.face[key] = range(face_num)
                
                for i in range(face_num):
                    line = fid.readline() # discard empty line
                    line = fid.readline()
                    line = line.split()
                    #self.face['index'][i] = i
                    self.face['solid_angle'][i] = float(line[0])
                    self.face['magnitude'][i] = float(line[1])
                    self.face['potential'][i] = float(line[2])
                    self.face['area'][i] = float(line[3])
                    line = fid.readline()
                    line = line.split()
                    self.face['center'][i] = [float(x) for x in line]
                    line = fid.readline()
                    line = line.split()
                    self.face['normal'][i] = [float(x) for x in line]
                    line = fid.readline() # discard empty line
                    line = fid.readline()
                    line = line.split()
                    line = [int(x) for x in line]
                    self.face['vertex'][i] = line[0:3]
                    self.face['edge'][i] = line[3:7]
                print '...done'
                
            else:
                
                print '...skipping %d faces' % face_num,

                for key in ['index','solid_angle',
                            'magnitude','potential','area',
                            'center','normal','vertex','edge']:
                    self.face[key] = []
                
                for i in range(face_num):
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
                    line = fid.readline()
                print '...done'
                
            if 'edge' in options:
                
                print '...reading %d edges' % edge_num,
                
                for key in ['index','vertex']:
                    self.edge[key] = range(edge_num)
                
                line = fid.readline()   # discard empty line
                for i in range(edge_num):
                    line = fid.readline()
                    line = line.split()
                    line = [int(x) for x in line]
                    self.edge['vertex'][i] = line
                print '...done'
                
            else:
                
                print '...skipping %d edges' % edge_num,
                
                for key in ['index','vertex']:
                    self.edge[key] = []
                
                line = fid.readline()   # discard empty line
                for i in range(edge_num):
                    line = fid.readline()
                print '...done'
        
        fid.close()
        return
    
    def write(self, file_name):
        "write a wireframe file"
        pass

## function emse_write_wfr(file,vertex,face,mesh_type,space)

## % emse_write_wfr - write mesh to EMSE wireframe (.wfr)
## % 
## % emse.wfr.write(file,vertex,face,mesh_type,space)
## % 
## % Write a .wfr file, in minor revision 3 format (ascii).
## % See the EMSE website at http://www.sourcesignal.com
## % for more information on file formats.
## % 
## % This function assumes the vertex coordinate axes are 
## % +X anterior, +Y left, +Z superior
## %
## % vertex - Nx3 matrix of XYZ values (in meters)
## % face - Nx3 matrix of vertex indices for triangulation
## % mesh_type - a string, with values of:
## %
## %     'unknown',     
## %     'scalp',       
## %     'outer skull', 
## %     'inner skull', 
## %     {'cortex', 'pial', 'white', 'smoothwm'}
## %
## % space - 'hspace' for head space (electrodes, default)
## %         'vspace' for MRI volume space
## %


## % $Revision: 1.1 $ $Date: 2007/12/27 00:21:20 $


## % History:  12/2004 Darren.Weber_at_radiology.ucsf.edu
## %                 - created function from mesh_emse2matlab
## %
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## ver = '$Revision: 1.1 $ $Date: 2007/12/27 00:21:20 $';
## fprintf('\nEMSE_WRITE_WFR [v%s]\n',ver(11:15));

## if ~exist('mesh_type', 'var'),
##   mesh_type = '';
## end

## if ~exist('space', 'var'),
##   space = 'hspace';
## end
## if isempty(space),
##   space = 'hspace';
## end


## [path,name,ext] = fileparts(file);
## ext = '.wfr';
## file = fullfile(path,[name ext]);
## fprintf('...writing to: %s\n',file);

## fid = fopen(file,'w','ieee-le');

## if(fid == -1),
##   msg = sprintf('...could not open file: %s',file);
##   error(msg);
## else
  
##   % Write prolog
##   fprintf(fid,'3\t4000\n');
##   fprintf(fid,'3\n');
  
##   % Write mesh type
##   type = lower(mesh_type);
##   switch type,
##    case 'unknown',
##     meshcode = 0;
##    case 'scalp',
##     meshcode = 40;
##    case 'outer skull',
##     meshcode = 80;
##    case 'inner skull',
##     meshcode = 100;
##    case {'cortex', 'pial', 'white', 'smoothwm'},
##     meshcode = 200;
##    otherwise,
##     meshcode = 0;
##     fprintf('\n...WARNING, unknown mesh_type!\n\n');
##   end
  
##   if strmatch('vspace', space, 'exact'),
##     meshcode = meshcode + 80000;
##   end
##   fprintf(fid, '%d\n', meshcode);
  
  
##   % EMSE Voxel Coordinates
##   % Voxel coordinates measure location in terms of the voxels inherent in 
##   % the given volumetric set. The origin is the bottom (inferior) axial 
##   % slice, the posterior row and in the rightmost column. This coordinate 
##   % system is right-handed (although, internally, the origin is in the 
##   % anterior row, and thus is left-handed; this representation is not 
##   % available to the user). The order of the displayed coordinates is 
##   % (slice#, row#, column#).
##   %
##   % EMSE MRI Coordinates
##   % MRI coordinates share the same origin as internal voxel coordinates, 
##   % but differ from the latter in two ways: first, the coordinates 
##   % are measured in millimeters, not voxels. Secondly, the origin is that 
##   % of the internal representation; that is, the inferior slice, anterior 
##   % row and rightmost column. As mentioned above, this internal representation 
##   % is left-handed. To correct for this, the row axis is numbered in the 
##   % opposite direction, making the displayed coordinate system right-handed. 
##   % The order of the displayed coordinates is (x, y, z).
  
##   % Given a point P(x,y,z) in head frame (the activation point on the 
##   % cortical mesh) and you want to find the corresponding voxel in the 
##   % vmi file.  Symbolically you have P(head) and you want to find P(voxel).
##   % 
##   % 1.  The registration file contains the matrix HeadToImage,
##   %     so P(MRI-mm) = HeadToImage*P(head), where P(MRI-mm) is the 
##   %     point in MRI coordinates.
##   % 2.  From the voxel size, you can find P(MRI-voxel), which 
##   %     is the MRI coordinates expressed in voxels
##   % 3.  Use the offset between the MRI coordinate frame and 
##   %     the Image coordinate frame to find P(voxel).
##   %
##   %Demetrios Voreades, Ph.D.
##   %Applications Engineer, Source Signal Imaging
##   %
  
  
##   % Rotate -90 degrees around Z, given that emse coordinates
##   % have +X through Nasion and +Y through left ear.
##   fprintf('...assuming coordinate axes are +X anterior, +Y left, +Z superior\n');
##   %vertex = rz(vertex,-90,'degrees');
  
##   % Write vertex data
##   for v = 1:size(vertex,1),
##     fprintf(fid,'v\t%12.8f\t%12.8f\t%12.8f\n',vertex(v,1),vertex(v,2),vertex(v,3));
##   end
  
##   % matlab vertex indices start at one,
##   % not zero, so we subtract one from matlab values
##   fprintf('...subtracting 1 from face indices, so they start at zero\n');
##   face = face - 1;
##   for t = 1:size(face,1),
##     fprintf(fid,'t\t%d\t%d\t%d\t\n',face(t,1),face(t,2),face(t,3));
##   end
  
##   fclose(fid);
  
## end

## return


    
    def edges(self):
        pass
    
    def elec2mri(self, reg):
        """
        Convert from electrode to MRI volume coordinates.
        
        wfr.elec2mri(reg)
        
        reg - a class containing coordinate transform matrices, which
        is read using emse.reg('regFile')
        
        Given a point P(x,y,z) in head frame (eg, an activation point on a 
        cortical mesh) this function will find the corresponding voxel in a 
        vmi file.  Symbolically we have P(head) and want to find P(voxel).

        1.  The registration file contains the matrix HeadToImage,
            so P(MRI-mm) = P(head)*HeadToImage, where P(MRI-mm) is the 
            point in MRI coordinates.
        2.  From the voxel size, you can find P(MRI-voxel), which 
            is the MRI coordinates expressed in voxels
        3.  Use the offset between the MRI coordinate frame and 
            the Image coordinate frame to find P(voxel).
        """
        # vertices is Nx3 matrix that should be represented
        # in homogenous coordinates:
        #elec = [ elec ones(size(elec,1),1) ];
        v = self.vertices
        o = numpy.ones(v.shape[0], 1)
        v = numpy.append(v, o, axis=1);

        # 1.  The registration file contains the matrix HeadToImage,
        #     so P(MRI) = HeadToImage*P(head), where P(MRI-mm) is the
        #     point in MRI coordinates.
        #
        # However, I've translated HeadToImage, so we now right-multiply,
        # which is consistent with a text book account of the subject.

        v = v * reg.elec2mri

        # reg.elec2mri is a 4x4 matrix, eg:
        #
        #  -0.9525    0.0452    0.3012         0
        #  -0.0522   -0.9985   -0.0154         0
        #   0.3000   -0.0304    0.9534         0
        #  -0.1295    0.1299    0.0756    1.0000
        #
        # The first 3x3 cells are the rotations,
        # the last row is the translations, and
        # the last column is the scale, if any.

        # In homogeneous coordinates, the last column
        # is the scale factor, usually 1
        v[:,0] = v[:,0] / v[:,3]
        v[:,1] = v[:,1] / v[:,3]
        v[:,2] = v[:,2] / v[:,3]
        
        self.vertices = v
        return
    
    def mri2elec(self, reg):
        "convert from MRI volume to electrode coordinates"
        pass

## function [hspace] = emse_mri2elec(vspace, reg)

## % EMSE_MRI2ELEC - Convert mri coordinates to points in head frame
## % 
## % [hspace] = emse_mri2elec(vspace, reg)
## % 
## % vspace - a struct with a mesh in MRI volume coordinates (mm)
## % vspace.vertices - the Nx3 (X,Y,Z) MRI coordinates to be converted
## % vspace.faces    - the Nx3 face connectivity of the mesh
## %
## % reg - a structure containing coordinate transform matrices,
## %       which is returned by emse_read_reg.m
## % 
## % hspace - a struct like vspace in electrode coordinates (meters)
## %
## % Given a point P(x,y,z) in MRI volume (eg, an fMRI activation overlayed
## % onto a high res T1 volume) this function will find the corresponding
## % location in the coordinates of the scalp electrodes (head space).
## % Symbolically we have P(voxel) and want to find P(head).
## % 
## % 1.  Use the offset between the MRI coordinate frame and the MRI volume
## % coordinate frame to find P(MRI-voxel).
## % 2.  Given P(MRI-voxel) and the voxel size, we can find P(MRI-mm), which is
## % the MRI coordinates expressed in mm.
## % 3.  The registration file contains the matrix ImageToHeadMatrix, so
## % P(head) = P(MRI-mm)*reg.mri2elec, where P(MRI-mm) is the point in MRI
## % coordinates, in millimeters.  The values in P(head) are in meters.
## % 
## % This function performs the last calculation, so all the inputs are assumed
## % to be correct.  To load an EMSE wireframe (ie, mesh), see emse_read_wfr.m
## % and to load a registration file, see emse_read_reg.m
## % 
## % See also: EMSE_READ_WFR, EMSE_READ_REG, EMSE_ELEC2MRI
## % 

## % $Revision: 1.1 $ $Date: 2007/12/27 00:21:20 $

## % Licence:  GNU GPL, no express or implied warranties
## % History:  06/2002, Darren.Weber@flinders.edu.au
## %                    EMSE details thanks to:
## %                    Demetrios Voreades, Ph.D.
## %                    Applications Engineer, Source Signal Imaging
## %           10/2007, modified code from Justin Ales
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## ver = '$Revision: 1.1 $ $Date: 2007/12/27 00:21:20 $';
## fprintf('EMSE_MRI2ELEC [v %s]\n',ver(11:15));

## if(nargin < 1)
##     help emse_mri2elec;
##     return;
## end

## if size(vspace.vertices,2) ~= 3,
##   error('Input vspace is not an Nx3 matrix')
## end

## % Convert from millimeter to meter units for EMSE hspace
## vs = vspace.vertices / 1000;

## % vs is an Nx3 matrix that must be represented in
## % homogenous coordinates, so we add ones to the last column
## nVertices = size(vs,1);
## vs = [vs, ones(nVertices,1)];

## % Black-magic: We need to switch to EMSE head space coordinate orientation,
## % by taking negative y and re-ordering the axes so we get:
## % hspace_x = -1 * vspace-y
## % hspace_y = vspace-z
## % hspace_z = vspace-x
## vs(:,2) = -1 * vs(:,2);
## vs = vs(:,[2 3 1 4]);

## % Apply the mri2elec transform
## hspace.faces = vspace.faces;
## hspace.vertices = vs * reg.mri2elec;

## % Notes:
## % reg.mri2elec is a 4x4 matrix, eg:
## %
## %  -0.9525    0.0452    0.3012         0
## %  -0.0522   -0.9985   -0.0154         0
## %   0.3000   -0.0304    0.9534         0
## %  -0.1295    0.1299    0.0756    1.0000
## %
## % The first 3x3 cells are the rotations,
## % the last row is the translations,
## % the last column is projections (usually 0),
## % and the value at 4,4 is the homogenous
## % coordinate scale unit, usually 1.

## % In homogeneous coordinates, the last column
## % is the scale factor, usually 1, but in case
## % it is ~= 1
## hspace.vertices(:,1) = hspace.vertices(:,1) ./ hspace.vertices(:,4);
## hspace.vertices(:,2) = hspace.vertices(:,2) ./ hspace.vertices(:,4);
## hspace.vertices(:,3) = hspace.vertices(:,3) ./ hspace.vertices(:,4);

## hspace.vertices = hspace.vertices(:,1:3);

## return
    
    
    
    def vtkSurf(self):
        
        nVert = len(self.vert['xyz'])
        nFace = len(self.face['vertex'])
        
        if nVert > 0:
            
            # put data into vtk data structure
            points = vtk.vtkPoints()
            points.SetNumberOfPoints(nVert)
            for i in range(nVert):
                v = self.vert['xyz'][i]
                points.SetPoint(i, v[0], v[1], v[2])
            
            faces = vtk.vtkCellArray()
            faces.Allocate(nFace, 1)
            for i in range(nFace):
                fv = self.face['vertex'][i]
                faces.InsertNextCell(3)
                # double check the order of vertices for vtk outward normals
                faces.InsertCellPoint(fv[0])
                faces.InsertCellPoint(fv[1])
                faces.InsertCellPoint(fv[2])
            
            vtkSurf = vtk.vtkPolyData()
            vtkSurf.SetPoints(points)
            vtkSurf.SetPolys(faces)
            
            #wfrDecimate = vtk.vtkDecimatePro()
            #wfrDecimate.SetInput(vtkSurf)
            #wfrDecimate.SetTargetReduction(0.9)
            #wfrDecimate.PreserveTopologyOn()
            
            #wfrSmooth = vtk.vtkSmoothPolyDataFilter()
            ##wfrSmooth.SetInput(wfrDecimate.GetOutput())
            #wfrSmooth.SetInput(wfrSurf)
            #wfrSurf = wfrSmooth.GetOutput()
            
            #wfrNormals = vtk.vtkPolyDataNormals()
            ##wfrNormals.SetInput(wfrSmooth.GetOutput())
            #wfrNormals.SetInput(wfrSurf)
            #wfrNormals.SetFeatureAngle(60)
            #wfrSurf = wfrNormals.GetOutput()
            
            return vtkSurf
            
        else:
            print "No data to convert to vtkPolyData"
    
    
    def view(self):
        
        wfrSurf = self.vtkSurf()
        
        #wfrDecimate = vtk.vtkDecimatePro()
        #wfrDecimate.SetInput(wfrSurf)
        #wfrDecimate.SetTargetReduction(0.9)
        #wfrDecimate.PreserveTopologyOn()
        
        #wfrSmooth = vtk.vtkSmoothPolyDataFilter()
        ##wfrSmooth.SetInput(wfrDecimate.GetOutput())
        #wfrSmooth.SetInput(wfrSurf)
        #wfrSurf = wfrSmooth.GetOutput()
        
        #wfrNormals = vtk.vtkPolyDataNormals()
        ##wfrNormals.SetInput(wfrSmooth.GetOutput())
        #wfrNormals.SetInput(wfrSurf)
        #wfrNormals.SetFeatureAngle(60)
        #wfrSurf = wfrNormals.GetOutput()
        
        # map data into a vtk actor
        wfrMapper = vtk.vtkPolyDataMapper()
        wfrMapper.SetInput(wfrSurf)
        #wfrMapper.SetInput(wfrNormals.GetOutput())
        
        wfrActor = vtk.vtkActor()
        wfrActor.SetMapper(wfrMapper)
        
        # create rendering
        ren1 = vtk.vtkRenderer()
        ren1.SetViewport(0.0, 0.0, 1.0, 1.0)
        ren1.SetBackground(0.0, 0.0, 0.0)
        ren1.AddViewProp(wfrActor)
        
        renWin = vtk.vtkRenderWindow()
        renWin.SetSize(300,300)
        renWin.AddRenderer(ren1)
        ren1.ResetCamera()
        
        # Add mouse interactions
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)
        iren.Initialize()
        iren.Start()
        
    
## function [Channel] = emse_elp2brainstorm(elp,chanFile)

## % emse_elp2brainstorm - Convert EMSE elp to brainstorm channel file
## % 
## % The EMSE elp struct is returned from emse_read_elp.  The elp data
## % structure is converted into the brainstorm format and returned.
## % 
## % Useage: Channel = emse_elp2brainstorm(elp,[brainstormChanFile])
## % 
## % elp = see emse_read_elp for more details
## % 
## % brainstormChanFile = a full path to a channel.mat file.  If this is
## % empty, the function will not save an output file.
## %
## % Channel is an array of structures.  The fields are:
## % 
## %  Loc     - a 3x2 matrix of electrode and reference coordinates.  Each
## %            column contains [X;Y;Z] values.
## %  Orient  - a corresponding matrix of sensor orientations for MEG; 
## %             all zero for EEG.
## %  Weight  - a vector of relative or absolute weights (eg, gain);
## %            all ones for this routine.
## %  Type    - a character string, 'EEG' in this function.
## %  Name    - a charater string indicating the electrode name.
## %  Comment - a charater string indicating the reference electrode. Empty
## %            for active electrodes and 'EEG REF' for the reference.
## % 
## % See brainstorm website at http://neuroimage.usc.edu/, including a
## % download pdf file describing the brainstorm database formats.
## % 

## % $Revision: 1.1 $ $Date: 2007/12/27 00:21:20 $

## % Licence:  GNU GPL, no express or implied warranties
## % History:  05/2007, Darren.Weber_at_radiology.ucsf.edu
## % 
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## if ~exist('elp', 'var'),
##   error('no input elp struct')
## end
## if isempty(elp),
##   error('empty elp struct')
## end

## if ~exist('chanFile', 'var'),
##   chanFile = '';
## end

## tic;

##   ver = '$Revision: 1.1 $';
##   fprintf('\nEMSE_ELP2BRAINSTORM [v %s]\n',ver(11:15));
##   fprintf('...Converting to brainstorm structure.\n');

##   for i=1:length(elp.x),
##     Channel(i).Loc = [[elp.x(i) elp.y(i) elp.z(i)]',elp.ref'];
##     Channel(i).Orient = [];     % used for MEG rather than EEG
##     Channel(i).Weight = 1;      % Like Amplification
##     Channel(i).Type = 'EEG';
##     Channel(i).Name = elp.name{i};
##     Channel(i).Comment = '';
##   end
##   Channel(i+1).Loc = [elp.ref',elp.ref'];
##   Channel(i+1).Orient = [];
##   Channel(i+1).Weight = 1;
##   Channel(i+1).Type = 'EEG';
##   Channel(i+1).Name = 'EEG REF';
##   Channel(i+1).Comment = 'EEG REF';

##   if ~isempty(chanFile),
##     fprintf('...saving BrainStorm channel data to:\n...%s\n',chanFile);
##     save(chanFile, 'Channel');
##   end

##   t = toc; fprintf('...done (%6.2f sec).\n\n',t);

##   return




    





    
## function [EMSE] = emse_read_avg(file_name)

## % emse_read_avg - Load EMSE .avg data (actually ascii format)
## % 
## % Useage: [EMSE] = emse_read_avg(file_name)
## %
## % where 'file_name' is the full path + fileprefix + filextension
## %
## % The returned struct has the following fields:
## % 
## % EMSE.channels
## % EMSE.pnts
## % EMSE.rate       - sample rate (msec)
## % EMSE.xmin       - prestim baseline period (msec)
## % EMSE.volt       - potential floating point matrix, 
## %                   size [points,channels]
## % 
## % No variance data is yet read or returned
## % 

## % $Revision: 1.1 $ $Date: 2007/12/27 00:21:20 $

## % Licence:  GNU GPL, no implied or express warranties
## % History:  08/2000, Darren.Weber_at_radiology.ucsf.edu
## %
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## ver = '$Revision: 1.1 $';
## fprintf('EMSE_READ_AVG [v %s]\n',ver(11:15));

## [path,name,ext] = fileparts(file_name);
## file = fullfile(path,[name ext]);

## if exist(file) ~= 2,
##   lookfile = which(file);
##   if isempty(lookfile),
##     msg = sprintf('Cannot locate %s\n', file_name);
##     error(msg);
##   else
##     file = lookfile;
##   end
## end

## fprintf('...reading: %s\n', file);

## fid = fopen(file);

## version   = fscanf(fid,'%d',1);
## file_type = fscanf(fid,'%d',1);
## minor_rev = fscanf(fid,'%d',1);

## if isempty(version),
##   EMSE.channels = [];
##   EMSE.pnts = [];
##   EMSE.rate = [];
##   EMSE.xmin = [];
##   EMSE.volt = [];
##   fprintf('...this is not an EMSE file.\n...it might be a Neuroscan file.\n');
##   return
## end

## fprintf('...Version = %d, File-Type = %d, Minor_Revision = %d\n',...
##   version,file_type,minor_rev);

## unknown  = fscanf(fid,'%d',1);
## channels = fscanf(fid,'%d',1);
## points   = fscanf(fid,'%d',1);
## samples  = fscanf(fid,'%f',1) * 1000; % msec sample rate
## unknown  = fscanf(fid,'%f',1);
## baseline = fscanf(fid,'%f',1) * -1000; % msec baseline
## unknown  = fscanf(fid,'%d',1);
## unknown  = fscanf(fid,'%d',1);


## fprintf('...Sample Rate (msec) = %6.3f, Baseline (msec) = %6.3f\n',...
##   samples,baseline);

## for i = 1:channels,
##   discard = fscanf(fid,'%d',2)';
## end

## volt = zeros(points,channels);

## for i = 1:points,
##   volt(i,:) = fscanf(fid,'%f',channels)';
## end

## fclose(fid);

## fprintf('...Points (rows) = %d, Channels (cols) = %d\n',points,channels);

## EMSE.channels = channels;
## EMSE.pnts = points;
## EMSE.rate = samples;
## EMSE.xmin = baseline;
## EMSE.volt = volt;

## return




    
## function elp = emse_read_elp(file_name)

## % emse_read_elp - Read an EMSE probe file (*.elp)
## % 
## % Usage: elp = emse_read_elp(file_name)
## % 
## % This function extracts x,y,z values from an EMSE probe (*.elp) file, only
## % if it contains EEG electrodes.
## % 
## % EMSE *.elp files are in meters.  When EMSE *.elp files are imported into
## % the eeg_toolbox, the X and Y values are swapped (this is handled by
## % elec_open).  There are no coordinate transforms in this function.
## % 
## % An example of the elp struct:
## % 
## %        version: 3
## %       filetype: 2
## %      minor_rev: 1
## %     sensorType: 4001
## %        sensorN: 125
## %         nasion: [0.0957 0 0]
## %            lpa: [-7.1503e-004 0.0804 0]
## %            rpa: [7.1503e-004 -0.0804 0]
## %              x: [124x1 double]
## %              y: [124x1 double]
## %              z: [124x1 double]
## %            ref: [0.0089 -0.0732 -0.0214]
## %         origin: [-0.0083 0.0043 0.0496]
## %           type: {124x1 cell}
## %           name: {124x1 cell}
## %
## % See also: ELEC_OPEN, ELEC_LOAD
## % 

## % $Revision: 1.1 $ $Date: 2007/12/27 00:21:20 $

## % Licence:  GNU GPL, no express or implied warranties
## % History:  10/2002, Darren.Weber_at_radiology.ucsf.edu
## % 
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## [path,name,ext] = fileparts(file_name);
## file = fullfile(path,[name ext]);

## [fid,msg] = fopen(file,'r');
## if ~isempty(msg), error(msg); end

## ver = '$Revision: 1.1 $';
## fprintf('\nEMSE_READ_ELP [v %s]\n',ver(11:15));
## fprintf('...reading .elp data.\n');

## tic

##   elp = read_elp(fid);

##   t = toc; fprintf('done (%6.2f sec).\n',t);

##   return


## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
## function [elp] = read_elp(fid)

## elp = [];

## % Probe files contain position information for electrode locations 
## % and/or gradiometer locations. The file consists of a prolog, a 
## % header, and a list of one or more sensor fields.

## % Any line beginning with '//' is a comment line, which is ignored

## % Read the prolog
## tmp = fscanf(fid,'%d',3);
## elp.version = tmp(1);
## elp.filetype = tmp(2); % type 2 is a probe file, extension .elp
## elp.minor_rev = tmp(3); % usually 1

## % Read the header
## % The header consists of one optional entry and 2 entries in 
## % mandatory sequence and one optional entry:
## % Name [optional] > %N %s replace %s with name string (8 or fewer characters)
## % Type Code       > %x    replace %x with 1 (all electric), 2 (all magnetic) or 4 (mixed).
## % #Channels       > %d    number of points per channel per epoch

## % Sensor state (which appears in the 'type code' field) may 
## % be obtained by logically OR-ing suitable combinations from 
## % Table A-3. Note that not all combinations are physically valid.
## %
## % type/state        type code 
## % magnetic          200
## % electric          400
## % off               800
## % reference         1000
## % optical           4000
## % trigger           8000
## % other             10000
## % named point       20000

## % Other types (such as named points, trigger, and optical) should 
## % be represented in the same pattern as electrodes, with the type 
## % code set to identify the type. Even those types (e.g. trigger) 
## % which do not have a true location, should have a nominal 
## % location, (e.g. 0 0 0).

## while 1,
##   tmp = fgetl(fid); % This should be: //TypeCode	nsensors
##   if strmatch('//TypeCode',tmp),
##     tmp = fscanf(fid,'%d',2);
##     elp.sensorType = tmp(1);
##     elp.sensorN = tmp(2);
##     break;
##   end
## end

## % Fiducial points may be included optionally. They are required 
## % for MRI registration. If they are included, they must be in 
## % the obligatory order : nasion, left preauricular point, 
## % right preauricular point. Table A-2 defines the format for 
## % representing fiduciary points.

## n = 0;
## while n <= 2,
##   n = n + 1;
##   tmp = fgetl(fid); % This should be: //Fiducials:  Nasion  Left  Right
##   if strmatch('//Fiducials',tmp),
##     tmp = fgetl(fid);
##     tmp = sscanf(tmp,'%2c %f %f %f');
##     elp.nasion = [tmp(3) tmp(4) tmp(5)];
##     tmp = fgetl(fid);
##     tmp = sscanf(tmp,'%2c %f %f %f');
##     elp.lpa    = [tmp(3) tmp(4) tmp(5)];
##     tmp = fgetl(fid);
##     tmp = sscanf(tmp,'%2c %f %f %f');
##     elp.rpa    = [tmp(3) tmp(4) tmp(5)];
##     break;
##   end
## end

## elp.x = zeros(elp.sensorN - 1,1);
## elp.y = zeros(elp.sensorN - 1,1);
## elp.z = zeros(elp.sensorN - 1,1);
## elp.ref = [];
## elp.origin = [];

## n = 1;
## while n <= elp.sensorN,
  
##   tmp = fgetl(fid);
##   if ~ischar(tmp),
##     break;
##   elseif strmatch('//',tmp);
##     % Ignore the comment lines, get the next one
##     tmp = fgetl(fid);
##   end
  
##   % Each electrode is represented by an electric sensor, 
##   % and consists of 5 fields, of which 1 (the name) is 
##   % optional. The electric sensor field data is shown 
##   % in Table A-6.
##   % Name              Format      Description 
##   % Type Code         %S          %x replace %x with 400 (electrode) or 1c00 if reference channel
##   % Name [optional]   %N          %s replace %s with name string (8 or fewer characters)
##   % Position          %g %g %g    electrode location with respect to head frame (Cartesian, meters)
##   % Orientation       %g %g %g    not used, replace with 0 0 1
  
##   if strmatch('%S',tmp),
    
##     if findstr('c00',tmp),
##       ref = 1; % A reference sensor
##     else
##       ref = 0;
##       %tmp = sscanf(tmp,'%2c %d');
##       elp.type{n,1} = tmp(4:end);
##     end
    
##     tmp = fgetl(fid);
##     if strmatch('//',tmp);
##       % Ignore the comment lines, get the next one
##       tmp = fgetl(fid);
##     end
    
##     tmp = deblank(tmp);
##     if strmatch('%N',tmp),
      
##       % Read the name of the sensor
##       tmp = strrep(tmp,'%N','');
##       tmp = fliplr(deblank(fliplr(tmp)));
##       if ~ref, elp.name{n,1} = tmp; end
      
##       % Read the location XYZ
##       tmp = fgetl(fid);
##       if strmatch('//',tmp);
##         % Ignore comments, get the next line
##         tmp = fgetl(fid);
##       end
      
##       if strmatch('%O',tmp),
##         if isempty(elp.origin),
##           % Get the sphere origin
##           elp.origin = sscanf(tmp(3:end),'%f',3)';
##         end
##         tmp = fgetl(fid);
##         tmp = fgetl(fid);
##         % Read the xyz location
##         tmp = sscanf(tmp,'%f',3);
##         if ref,
##           elp.ref = tmp';
##         else
##           elp.x(n) = tmp(1);
##           elp.y(n) = tmp(2);
##           elp.z(n) = tmp(3);
##           n = n + 1;
##         end
##         % Skip the next line (empty)
##         tmp = fgetl(fid);
##       else
##         tmp = sscanf(tmp,'%f',3);
##         if ref,
##           elp.ref = tmp';
##         else
##           elp.x(n) = tmp(1);
##           elp.y(n) = tmp(2);
##           elp.z(n) = tmp(3);
##           n = n + 1;
##         end
##       end
##     end
##   end
## end

## fclose(fid);

## return




if __name__ == '__main__':
    
    for mrev in [2,3,4]:
        
        if mrev == 2:
            test_file = '/data/matlab/bioelectromagnetism/eeg_example_data/mesh_emse_mrev2_scalp.wfr'
        if mrev == 3:
            test_file = '/data/matlab/bioelectromagnetism/eeg_example_data/mesh_emse_mrev3_test.wfr'
        if mrev == 4:
            test_file = '/data/matlab/bioelectromagnetism/eeg_example_data/mesh_emse_mrev4_scalp.wfr'
        
        test_wfr = wfr()
        test_wfr.read(test_file)
        test_wfr.view()
        
##         if mrev = 2:
##             print test_wfr.vert['xyz']
##         else:
##             print test_wfr.vert
##             print test_wfr.face
        
