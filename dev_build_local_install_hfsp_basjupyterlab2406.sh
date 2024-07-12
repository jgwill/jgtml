#v=93
tenv=hfsp_basjupyterlab2406
. pre-build.sh  && make dist && (cdjgtd;conda activate $tenv;pip uninstall jgtml -y;pip install /a/src/_jgt/jgtml/dist/jgtml-*.whl)
