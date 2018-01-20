#!/bin/bash
docker ps -f name=t4re
docker restart t4re
TASK_TMP_DIR=temp
RESULT_DIR="$1_$2"
mkdir RESULT_DIR
echo "====== TASK $TASK_TMP_DIR started ======"
docker exec -it t4re mkdir \-p ./$TASK_TMP_DIR/
docker exec -it t4re mkdir \-p ./$TASK_TMP_DIR/

for file in $1/*
do
    if [[ -f $file ]]; then
        filename=$(basename $file)
        just_name="${filename%.*}"
        echo $filename
        docker cp $1/$filename t4re:/home/work/$TASK_TMP_DIR/
        docker exec -it t4re /bin/bash -c "mkdir -p ./$TASK_TMP_DIR/out/; cd ./$TASK_TMP_DIR/out/; tesseract ../$filename $just_name -l $2 --psm 7 --oem $3 txt"
        docker cp t4re:/home/work/$TASK_TMP_DIR/out/ ./$RESULT_DIR/
        docker exec -it t4re ls
    fi
done
echo "====== Result files was copied to ======"
docker exec -it t4re rm -r \-p ./$TASK_TMP_DIR/*
