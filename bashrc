function findTodo {
   todome -i
   p=$?
   if [ "$p" -ge 1 ]; then
       echo -e "[\033[31m*$p*\033[0m]"
   fi
   #\$(findTodo)
}
