# python 环境问题笔记

## 1. HiVT

## 1.1 环境安装

参考 https://blog.csdn.net/qq_43647582/article/details/136660801

https://zhuanlan.zhihu.com/p/670667061

40系新显卡不兼容readme中的配置

```
conda create -n HiVT40 python=3.8
conda activate HiVT40
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117

# 安装 scatter、sparse、cluster、spline_conv
# https://pytorch-geometric.com/whl/index.html 中根据torch版本找
pip install torch_scatter-2.1.1+pt113cu117-cp38-cp38-linux_x86_64.whl torch_sparse-0.6.17+pt113cu117-cp38-cp38-linux_x86_64.whl torch_cluster-1.6.1+pt113cu117-cp38-cp38-linux_x86_64.whl torch_spline_conv-1.2.2+pt113cu117-cp38-cp38-linux_x86_64.whl 

pip install pytorch-geometric==1.7.2

pip install pytorch-lightning==1.5.2

pip install torchmetrics==0.8.2
```

安装 Argoverse 1.1 api 

修改setup

将 sklearn 修改为 scikit-learn

注释 numpy

```
pip install -e /home/lxx/project/argoverse-api
```

tensorboard



## 1.2 训练

train

```
python train.py --root /home/lxx/project/argov1 --embed_dim 64

```

eval

```
python eval.py --root /home/lxx/project/argov1 --batch_size 32 --ckpt_path /home/lxx/project/HiVT/lightning_logs/version_3/checkpoints/epoch=63-step=63.ckpt

```



```
watch -n 1 nvidia-smi
```



