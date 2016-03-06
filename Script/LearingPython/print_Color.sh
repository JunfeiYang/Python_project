#!/bin/bash
#Purpose:
#了解shell下printf格式化的颜色

####
# 输出red 
printf "\033[31m=========== console  begin Color =================\n"
echo "command eg: ./compareSoftLib.sh smartstorage_segserver"
echo "code : 0-> compare success "
echo "       1-> bitsflow not exist "
echo "       2-> config file not exist or empty "
echo "       3-> scp file not exist"
echo "       4-> scp file failure"
echo "       5-> execute remote file failure"
echo "       6-> yoyopkg install xxxx failure"
echo "       7-> plugins init failure"
printf "=========== console lib help end =================== \033[0m \n"
#printf "\033[47;31m=========== console  begin Color =================\n"
#printf "=========== console lib help end =================== \033[0m \n"

#输出bule 
printf  "\033[34m=========== console  help begin =================\n"
echo "command eg: ./compareSoftLib.sh smartstorage_segserver"
echo "code : 0-> compare success "
echo "       1-> bitsflow not exist "
echo "       2-> config file not exist or empty "
echo "       3-> scp file not exist"
echo "       4-> scp file failure"
echo "       5-> execute remote file failure"
echo "       6-> yoyopkg install xxxx failure"
echo "       7-> plugins init failure"
printf "=========== console lib help end =================== \033[0m \n"
#printf "\033[47;34m=========== console  begin Color =================\n"
#printf "=========== console lib help end =================== \033[0m \n"

#输出Purple(紫色)
printf "\033[35m=========== console  begin Color =================\n"
echo "command eg: ./compareSoftLib.sh smartstorage_segserver"
echo "code : 0-> compare success "
echo "       1-> bitsflow not exist "
echo "       2-> config file not exist or empty "
echo "       3-> scp file not exist"
echo "       4-> scp file failure"
echo "       5-> execute remote file failure"
echo "       6-> yoyopkg install xxxx failure"
echo "       7-> plugins init failure"
printf "=========== console lib help end =================== \033[0m \n"
#printf "\033[47;35m=========== console  begin Color =================\n"
#printf "=========== console lib help end =================== \033[0m \n"
