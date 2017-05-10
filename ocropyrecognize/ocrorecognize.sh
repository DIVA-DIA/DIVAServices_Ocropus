inputZip=$1
resultFile=$2

export PYTHONWARNINGS="ignore"

unzip $inputZip -d recognize

/ocropy/ocropus-rpred -Q 4 -m recognize/model.pyrnn.gz recognize/*.bin.png

declare -a files
files=(/data/recognize/*.txt)
pos=$((${#files[*]}-1))
last=${files[$pos]}

echo "{\"output\":[" > $resultFile

for f in "${files[@]}"
do
 fileName=$(basename "$f")
 fileContent="$(cat $f)"
 if [[ $f == $last ]]
 then
   echo "{ \"file\": {\"mime-type\": \"text/plain\", \"name\":\""$fileName"\", \"options\":{ \"type\": \"text\", \"visualization\":false}, \"content\": \""$fileContent"\"}}" >> $resultFile
 else
  echo "{ \"file\": {\"mime-type\": \"text/plain\", \"name\":\""$fileName"\", \"options\":{ \"type\": \"text\", \"visualization\":false}, \"content\": \""$fileContent"\"}}," >> $resultFile
 fi
done
echo "]}" >> $resultFile
