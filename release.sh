#!/usr/bin/env bash

# Retrieves the current version from VERSION. This will likely be in the format: x.x.x-SNAPSHOT
CURRENT_VERSION=$(cat VERSION);
# Define and remove the -SNAPSHOT suffix from CURRENT_VERSION and assign the result to RELEASE_VERSION
suffix="-SNAPSHOT";
RELEASE_VERSION=${CURRENT_VERSION%$suffix};
# Increment RELEASE_VERSION by one. This should result in: x.x.x -> x.x.x+1
NEXT_VERSION=$(echo $RELEASE_VERSION | awk -F. -v OFS=. 'NF==1{print ++$NF}; NF>1{if(length($NF+1)>length($NF))$(NF-1)++; $NF=sprintf("%0*d", length($NF), ($NF+1)%(10^length($NF))); print}')
# Defines the next SNAPSHOT release version
NEXT_SNAPSHOT_VERSION=$NEXT_VERSION-SNAPSHOT


echo $RELEASE_VERSION > VERSION
git commit -m "prepare release"

rm -f -R ./dist/
python ./setup.py sdist bdist_wheel
python -m twine upload dist/*

git tag v$RELEASE_VERSION

echo $NEXT_SNAPSHOT_VERSION > VERSION
git commit -m "prepare for next development iteration"

# Cleanup containers/images, build new image and push to Docker Hub
REPO=cyclonedx/cyclonedx-python
docker rm cyclonedx-python
docker rmi $REPO:latest
docker rmi $REPO:$RELEASE_VERSION
docker build -f Dockerfile -t $REPO:$RELEASE_VERSION -t $REPO:latest .
docker login
docker push $REPO:latest
docker push $REPO:$RELEASE_VERSION
