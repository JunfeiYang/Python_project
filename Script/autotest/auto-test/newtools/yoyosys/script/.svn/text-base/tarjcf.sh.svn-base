#! /bin/bash
direc=$1
echo $direc;
if [ ! $direc ] ;  then
  echo "Usage : $shell please input direc "
  exit 0 ;
fi

for dir in $direc/* ; do
  if [ -d $dir ] ; then
    fileName=${dir##*/};
    cd $direc;
    echo "tar" $fileName ".....";
    tar -jcf $fileName.tar.bz2 $fileName;
    rm -rf $fileName;
  fi
done ;
