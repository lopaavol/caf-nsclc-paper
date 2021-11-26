% Extract cores from TMA array using coordinates in csv files

rootpath = '';
scaling = 1;

dirs = dir(rootpath);
dirs = dirs([dirs.isdir]);
dirs = dirs(~ismember({dirs.name},{'.','..'}));

for d=1:size(dirs,1)
    disp(sprintf('Processing dir %d/%d',d,size(dirs,1)));
    inputpath = dirs(d).name;
    if ~exist(fullfile(rootpath,inputpath,'rois'))
        mkdir(fullfile(rootpath,inputpath,'rois'));
    end
    imgfiles = dir(fullfile(rootpath,inputpath,'*.tif'));
    imgfiles(~startsWith({imgfiles.name},'.'))

    coordsfile = dir(fullfile(rootpath,inputpath,'*.csv'));
    coordsfile(~startsWith({coordsfile.name},'.'))
    
    coords = readtable(fullfile(rootpath,inputpath,coordsfile(1).name));
    coords = table2array(coords(:,4:7));
    coords = coords * scaling;

    for imgidx=1:size(imgfiles,1)
        imgname = fullfile(rootpath,inputpath,imgfiles(imgidx).name);
        disp(sprintf('Processing file %d/%d',imgidx,size(imgfiles,1)));
        [~,basename,~] = fileparts(imgname);
        img = imread(imgname);
        for roiidx=1:size(coords,1)
            ys = coords(roiidx,2) + 1;
            ye = coords(roiidx,2) + coords(roiidx,4);
            if ye > size(img,1)
                ye = size(img,1);
                ys = ye - coords(roiidx,4) + 1;
            end
            xs = coords(roiidx,1) + 1;
            xe = coords(roiidx,1) + coords(roiidx,3);
            if xe > size(img,2)
                xe = size(img,2);
                xs = xe - coords(roiidx,3) + 1;
            end
            cimg = img(ys:ye,xs:xe);
            imwrite(cimg,fullfile(rootpath,inputpath,'rois',sprintf([basename '_roi%03d.tif'],roiidx)));
            disp(sprintf('%d/%d rois done',roiidx,size(coords,1)));
        end
    end
end
