#!/bin/sh

# execute any pre-init scripts
for i in /scripts/pre-init.d/*sh
do
    if [ -e "${i}" ]; then
        echo -e "[___PRE-INIT___] -- \e[32mENABLE\e[39m"
        echo -e "[ \033[0;35mMARIADB\033[0m ] -- pre-init.d - processing $i"
        . "${i}"
    fi
    echo -e "[___PRE-INIT___] -- \e[31mDISABLE\e[39m"
done

if [ -d "/run/mysqld" ]; then
    echo -e "[ \033[0;35mMARIADB\033[0m ] -- mysqld already present, skipping creation"
    chown -R mysql:mysql /run/mysqld
else
    echo -e "[ \033[0;35mMARIADB\033[0m ] -- mysqld not found, creating...."
    mkdir -p /run/mysqld
    chown -R mysql:mysql /run/mysqld
fi

if [ -d /var/lib/mysql/mysql ]; then
    echo -e "[ \033[0;35mMARIADB\033[0m ] -- MySQL directory already present, skipping creation"
    chown -R mysql:mysql /var/lib/mysql
else
    echo -e "[ \033[0;35mMARIADB\033[0m ] -- MySQL data directory not found, creating initial DBs"

    chown -R mysql:mysql /var/lib/mysql

    mysql_install_db --user=mysql --ldata=/var/lib/mysql > /dev/null

    if [ "$MYSQL_ROOT_PASSWORD" = "" ]; then
        MYSQL_ROOT_PASSWORD=`pwgen 16 1`
        echo -e "[ \033[0;35mMARIADB\033[0m ] -- MySQL root Password: $MYSQL_ROOT_PASSWORD"
    fi

    MYSQL_USER=${MYSQL_USER:-""}
    MYSQL_HOST=${MYSQL_HOST:-""}
    MYSQL_DATABASE=${MYSQL_DATABASE:-""}
    MYSQL_PASSWORD=${MYSQL_PASSWORD:-""}

    tfile=`mktemp`
    if [ ! -f "$tfile" ]; then
        return 1
    fi

    cat << EOF > $tfile
USE mysql;
FLUSH PRIVILEGES ;
GRANT ALL ON *.* TO 'root'@'localhost' identified by '$MYSQL_ROOT_PASSWORD' WITH GRANT OPTION ;
GRANT ALL ON *.* TO 'root'@'127.0.0.1' identified by '$MYSQL_ROOT_PASSWORD' WITH GRANT OPTION ;
SET PASSWORD FOR 'root'@'localhost'=PASSWORD('${MYSQL_ROOT_PASSWORD}') ;
SET PASSWORD FOR 'root'@'127.0.0.1'=PASSWORD('${MYSQL_ROOT_PASSWORD}') ;
DROP DATABASE IF EXISTS test ;
FLUSH PRIVILEGES ;
EOF

    if [ "$MYSQL_DATABASE" != "" ]; then
       echo -e "[ \033[0;35mMARIADB\033[0m ] -- Creating database: $MYSQL_DATABASE"
        if [ "$MYSQL_CHARSET" != "" ] && [ "$MYSQL_COLLATION" != "" ]; then
            echo -e "[ \033[0;35mMARIADB\033[0m ] -- with character set [$MYSQL_CHARSET] and collation [$MYSQL_COLLATION]"
            echo "CREATE DATABASE IF NOT EXISTS \`$MYSQL_DATABASE\` CHARACTER SET $MYSQL_CHARSET COLLATE $MYSQL_COLLATION;" >> $tfile
        else
            echo -e "[ \033[0;35mMARIADB\033[0m ] -- with character set: 'utf8' and collation: 'utf8_general_ci'"
            echo "CREATE DATABASE IF NOT EXISTS \`$MYSQL_DATABASE\` CHARACTER SET utf8 COLLATE utf8_general_ci;" >> $tfile
        fi

    if [ "$MYSQL_USER" != "" ]; then
        echo -e "[ \033[0;35mMARIADB\033[0m ] -- Creating user: $MYSQL_USER with password $MYSQL_PASSWORD"
        echo "GRANT ALL ON \`$MYSQL_DATABASE\`.* to '$MYSQL_USER'@'$MYSQL_HOST' IDENTIFIED BY '$MYSQL_PASSWORD';" >> $tfile
        fi
    fi

    /usr/bin/mysqld --user=mysql --bootstrap --verbose=0 --skip-name-resolve --skip-networking=0 < $tfile
    rm -f $tfile

    for f in /docker-entrypoint-initdb.d/*; do
        case "$f" in
            *.sql)    echo "$0: running $f"; /usr/bin/mysqld --user=mysql --bootstrap --verbose=0 --skip-name-resolve --skip-networking=0 < "$f"; echo ;;
            *.sql.gz) echo "$0: running $f"; gunzip -c "$f" | /usr/bin/mysqld --user=mysql --bootstrap --verbose=0 --skip-name-resolve --skip-networking=0 < "$f"; echo ;;
            *)        echo "$0: ignoring or entrypoint initdb empty $f" ;;
        esac
        echo
    done

    echo
    echo -e "[ \033[0;35mMARIADB\033[0m ] -- \e[32mENABLE\e[39m -- MySQL init process done. Ready for start up."
    echo

    echo -e "[ \033[0;35mMARIADB\033[0m ] -- exec /usr/bin/mysqld --user=mysql --console --skip-name-resolve --skip-networking=0" "$@"
fi

# execute any pre-exec scripts
for i in /scripts/pre-exec.d/*sh
do
    if [ -e "${i}" ]; then
        echo -e "[___PRE-EXEC___] -- \e[32mENABLE\e[39m";
        echo -e "[ \033[0;35mMARIADB\033[0m ] -- pre-exec.d - processing $i"
        . ${i}
    fi
    echo -e "[___PRE-EXEC___] -- \e[31mDISABLE\e[39m";
done

# create my.cnf for auto login
cat <<EOF > ~/.my.cnf
[client]
user=root
password=${MYSQL_PASSWORD}
EOF

chmod 600 ~/.my.cnf
echo -e "[___MY.CNF___] -- \e[32mCREATE WITH SUCCESS\e[39m";

echo -e "[ \033[0;35mMARIADB\033[0m ] -- \e[32mSTARTED\e[39m"
exec /usr/bin/mysqld --user=mysql --console --skip-name-resolve --skip-networking=0 $@
