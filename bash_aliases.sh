#
# bash aliases and other goodies for mongo movies
#
printf %"s\n" '==> source bash_aliases.sh'

function mdbfind() { find . -iname "$1" -print0 | xargs -0 ls -al; }

alias s='stty sane; echo ""; clear;'
alias l='ls -l'
alias cls='clear'
alias rm='rm -i'
alias mv='mv -i'
alias cp='cp -i'
alias man='man -a'
alias grep='grep -n --color=auto'
alias lh='ls -lt | head -30'
alias h='history'

txtblk='\e[0;30m' # Black - Regular
txtred='\e[0;31m' # Red
txtgrn='\e[0;32m' # Green
txtylw='\e[0;33m' # Yellow
txtblu='\e[0;34m' # Blue
txtpur='\e[0;35m' # Purple
txtcyn='\e[0;36m' # Cyan
txtwht='\e[0;37m' # White

bldblk='\e[1;30m' # Black - Bold
bldred='\e[1;31m' # Red
bldgrn='\e[1;32m' # Green
bldylw='\e[1;33m' # Yellow
bldblu='\e[1;34m' # Blue
bldpur='\e[1;35m' # Purple
bldcyn='\e[1;36m' # Cyan
bldwht='\e[1;37m' # White

bakblk='\e[40m'   # Black - Background
bakred='\e[41m'   # Red
bakgrn='\e[42m'   # Green
bakylw='\e[43m'   # Yellow
bakblu='\e[44m'   # Blue
bakpur='\e[45m'   # Purple
bakcyn='\e[46m'   # Cyan
bakwht='\e[47m'   # White
txtrst='\e[0m'    # Text Reset

# set prompt
# export PS1="\[$bldred\]`hostname`: \[$bldgrn\]\$PWD\[$bldred\]> \[$txtrst\]"
export PS1="\[$bldred\][\u]: \[$bldgrn\]\$PWD\[$bldred\]> \[$txtrst\]"

# set node version
SRC_DIR="/Users/mark.brettin/local/src/python/fluser";
cd $SRC_DIR;

function rnr_fluser() {
    # rebuild and run docker container

    #SRC_DIR="/Users/mdb/local/src/mongo_movies"

    echo "==> cd $SRC_DIR";
    cd $SRC_DIR;

    echo "==> docker stop fluser";
    docker stop fluser;

    echo "==> docker rm fluser";
    docker rm fluser;

    echo "==> docker rmi -f fluser";
    docker rmi -f fluser;

    echo "==> docker build -t fluser .";
    docker build -t fluser .;

    printf %"s\n" "==> docker run --detach -p 5000:5000" \
                  "               --name fluser fluser" \
                  "               -v $SRC_DIR:/app fluser";

    docker run --detach -p 5000:5000 \
               --name fluser fluser
               #-v $SRC_DIR/node/lib:/app/lib
}

function fluser_bash() {
  printf %"s\n" "==> docker exec -it fluser bash"
  docker exec -it fluser bash
}
