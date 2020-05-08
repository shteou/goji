latest=$(git tag | egrep "^v[0-9]+\.[0-9]+\.[0-9]+$" | sort -V | tail -n 1)
semver_pattern="([0-9]+\.[0-9]+)\.([0-9]+)"

function sed_inplace() {
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sed -i "$@"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i "" "$@"
  fi
}

if [[ $latest =~ $semver_pattern ]]
then
  major_minor="${BASH_REMATCH[1]}"
  patch="${BASH_REMATCH[2]}"

  # Increment patch version
  patch=$(($patch+1))

  new_version="${major_minor}.${patch}"
  git checkout -b "v$new_version"

  sed_inplace "s/version=\"0.0.1\"/version=\"$new_version\"/" setup.py
  sed_inplace "s/version: 0.1.0/version: $new_version/" charts/goji/Chart.yaml
  sed_inplace "s/appVersion: \"1.0\"/appVersion: \"$new_version\"/" charts/goji/Chart.yaml

  git add setup.py charts/goji/Chart.yaml
  git commit -m "Bump version to $new_version"

  git tag "v$new_version"

  git checkout master
  git branch -D "v$new_version"
  git push origin "v$new_version"
else
  echo "No tags found?"
fi