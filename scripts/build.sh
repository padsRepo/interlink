#!/bin/bash

[[ -z $1 ]] && printf "Syntax: ${0##*/} <projectName>\n" && exit 2

base_dir=$(dirname "$(readlink -f "${0%/*}")")
randpass=$(sudo < /dev/urandom tr -dc A-Za-z0-9{\!@#$%^\&*\(\){}[]?} | head -c14; echo)
database="$(find ${base_dir}/scripts -type d -iname db)"
saveFile="${base_dir}/tests/.env"
exampleDir="${base_dir}/examples"
projectDir="${base_dir}/tests/${1}"
venvDir="${base_dir}/tests/venv"

[[ -d $projectDir ]] && printf " :: Project already exists \n" && exit 1

# Set up test env
if [[ ! $(mariadb --version) ]]; then 
  printf " :: Installing Mariadb"
  sudo pacman -Syu mariadb
  sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
  printf " :: Enabling/Starting service" 
  sudo systemctl enable mariadb.service &> /dev/null && sudo systemctl start mariadb.service &> /dev/null
  sudo mariadb-secure-installation
else
  printf " :: MariaDB already installed! \n"
fi

printf " :: Creating PADS profile... \n"
# Create Mariadb user
sudo mariadb --user=root -e "USE mysql; CREATE USER IF NOT EXISTS 'pads'@'%' IDENTIFIED BY '${randpass}'; GRANT ALL PRIVILEGES ON *.* TO 'pads'@'%'; FLUSH PRIVILEGES;"

# Install DB's from PADS dir
for file in $(ls ${database}); do
  [[ $? -eq 0 ]] && sudo mariadb < "${database}/${file}" 2> /dev/null && printf "[INSTALLED] :: ${file} \n" || printf "[ERROR] :: ${file} \n"
done

# Save pads profile for later
if [[ ! -f ${saveFile} ]]; then
  printf " :: Saving PADS Profile... \n"
  echo "#!/bin/bash" > ${saveFile}
  echo "export DB_USER=\"pads\"" >> ${saveFile}
  echo "export DB_PASS=\"${randpass}\"" >> ${saveFile}
  echo "export SECRET_KEY=\"\$(tr -dc A-Za-z0-9 </dev/urandom | head -c 64)\"" >> "${saveFile}"
  # Create ENV VARS for each DB, saved to saveFile
  for i in $(sudo mariadb -e 'SHOW DATABASES WHERE `Database` NOT in ("information_schema", "performance_schema", "mysql", "sys")';); do
    echo "export ${i^^}=\"${i}\"" | sed s/'export DATABASE="Database"'/" "/g >> ${saveFile}
  done
else
  printf " :: PADS Profile exists...\n"
fi

# Make project
cp -r "${exampleDir}/*" ${projectDir}

# Install virtual env and interlink
python -m venv ${venvDir}
. ${venvDir}/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ${base_dir}
