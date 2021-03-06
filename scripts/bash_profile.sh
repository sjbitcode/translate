# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac
# Case-insensitive globbing (used in pathname expansion)
shopt -s nocaseglob

# append to the history file, don't overwrite it
shopt -s histappend

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# Prefer US English and use UTF-8
export LC_ALL="en_US.UTF-8"
export LANG="en_US"

function parse_git_dirty {
  [[ $(git status 2> /dev/null | tail -n1) != "nothing to commit, working directory clean" ]] && echo "*"
}

function env_set {
  if [ -z "$ENV" ]; then
    echo ""
    else
    echo "($ENV)"
  fi
}

function parse_git_branch {
  git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e "s/* \(.*\)/[\1$(parse_git_dirty)]/"
}

RED="\[\e[0;36m\]"
GRAY="\[\e[0;37m\]"
YELLOW="\[\e[0;33m\]"
BLUE="\[\e[0;34m\]"
GREEN="\[\e[0;32m\]"
WHITE="\[\e[1;37m\]"
LIGHT_GREEN="\[\e[1;32m\]"
TXTRST='\[\e[0m\]'

export CLICOLOR=1
# export LSCOLORS=ExFxCxDxBxegedabagacad
# export PS1="[$GREEN\t \u@\h:$YELLOW\w$TXTRST]$RED\$(parse_git_branch)$TXTRST\$(env_set) $ \[\e[m\]"
export PS1="[\u@\h:$YELLOW\w$TXTRST]$RED\$(parse_git_branch)$TXTRST\$(env_set) $ \[\e[m\]"
export EDITOR=/usr/bin/vim

# timestamps for bash history. www.debian-administration.org/users/rossen/weblog/1
# saved for later analysis
export HISTSIZE=32768
export HISTFILESIZE=$HISTSIZE
export HISTCONTROL=ignoredups
# export HISTIGNORE="ls:ls *:cd:cd -:pwd;exit:date:* --help"
HISTTIMEFORMAT='%F %T '
export HISTTIMEFORMAT

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

alias pycls='find . -name '\''*.pyc'\'' -print0|xargs -0 rm'
alias chcls='find . -name '\''*__pycache__'\'' -print0|xargs -0 rm -rf'
alias python="python3"
alias pip="pip3"
alias m="python manage.py"
alias r="python manage.py runserver 0.0.0.0:8000"
alias shell="python -i /vagrant/scripts/django_shell.py"
alias collectstatic="sudo python3 manage.py collectstatic"
export DJANGO_SECRET_KEY='django-secret-key'
export DJANGO_SETTINGS_MODULE='translate.settings.local'
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/file"