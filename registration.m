function register_fold(filepaths)
% Read the input Excel sheet and run registration between all listed TMA cores

warning('off','all')

T = readtable( filepaths );
 
for i = 1:height(T)
    try
        reg_f( T.first_scan{i}, T.second_scan{i} );
    catch
        disp( ['Failure 1 with: '  T.first_scan{i} ' and ' T.second_scan{i}] )
    end
end

end
 
 
function reg_f(f1, f2)
% Run registration between two cores

mkdir( [f2 filesep 'regs'] );
mkdir( [f2 filesep 'thumbs'] );
 
% Metasystems
%img_names = dir( [f1 filesep '*Spot0*-B.tif'] );
% Z1
img_names = dir( [f1 filesep '*_DAPI_ORG_roi*.tif'] );
%
 
for i = 1:length( img_names )
    try
        img_name_1 = [f1 filesep img_names(i).name];

        % Metasystems
        % spot_str = img_name_1(end-11:end-6);
        % tmp = dir( [f2 filesep '*' spot_str '*-B.tif'] );
        % Z1
        spot_str = img_name_1(end-6:end-4);
        tmp = dir([f2 filesep '*_DAPI_ORG_roi' spot_str '*']);
        %
        img_name_2 = [f2 filesep tmp(1).name];                
        thumb_name = [f2 filesep 'thumbs' filesep img_names(i).name];
        reg_opts = reg_imgs( imread(img_name_1), imread(img_name_2), thumb_name );
        transform_ims(reg_opts, f2, spot_str, img_name_1)
    catch
        disp(['Failure 2 with: ' img_name_1 ' and ' img_name_2 ])
    end
end
 
end
 
 
function reg_opts = reg_imgs(fixed, moving, thumb_name)
% General registration function that optimizes the tranformation and
% saves a thumbnail image showing the overlap of the channels after registration
reg_opts.ds = 1/4;
fixed = imresize(fixed, reg_opts.ds);
moving = imresize(moving, reg_opts.ds);

reg_opts.tformEstimate = imregcorr(moving,fixed);
movingReg = imwarp(moving,reg_opts.tformEstimate,'OutputView',imref2d(size(fixed)));
imwrite( imresize( imfuse(fixed,movingReg,'falsecolor'), 1 ), thumb_name ); 
reg_opts.tformEstimate.T(3) = reg_opts.tformEstimate.T(3) / reg_opts.ds;
reg_opts.tformEstimate.T(6) = reg_opts.tformEstimate.T(6) / reg_opts.ds;
 
end
 
 
function transform_ims( reg_opts, f2, spot_str, img_name_1 )
% Transform and save images using the given transformation
fixed = imread(img_name_1);
tmp = dir( [f2 filesep '*roi' spot_str '*.tif'] );

try
    for i=1:length(tmp)        
        img_name_2 = [f2 filesep tmp(i).name];
        moving = imread( img_name_2 );
        movingReg = imwarp(moving,reg_opts.tformEstimate,'OutputView',imref2d(size(fixed)),'FillValues',0);
        imwrite( movingReg, [f2 filesep 'regs' filesep tmp(i).name(1:end-4) '_reg.tif'] );
        clear img_name_2 moving movingReg
    end
catch
    disp( ['Failure 3: with ' img_name_1] )
end
 
end
