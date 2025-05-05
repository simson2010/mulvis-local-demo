# MulVis 项目演示

## 项目简介
MulVis 是一个用于多维度数据可视化的演示项目。该项目旨在通过直观的图表和交互界面，帮助用户更好地理解和分析复杂的数据集。

## 运行环境要求
- Linux 操作系统
- Python 3.11
- Docker
- Docker Compose

## 功能特性
- 支持多种图表类型：折线图、柱状图、饼图等
- 数据动态更新
- 交互式数据探索
- 响应式设计，适配不同设备

## 快速开始
1. 克隆本仓库
   ```bash
   git clone https://github.com/your-repo/mulvis-demo.git
   ```
2. 进入项目目录
   ```bash
   cd mulvis-demo
   ```
3. 使用 Docker Compose 启动服务
   ```bash
   docker-compose up -d
   ```

## 项目结构

mulvis-demo/
├── demos/ # 源代码目录
│ ├── configs.py # 配置文件
│ ├── search.py # 搜索文件
│ ├── insert_delete.py # 插入删除文件
│ ├── load_unload_collection.py # 加载卸载集合文件
│ └── data/ # 数据文件
├── docker/ # Docker 配置文件
├── public/ # 静态资源
└── requirements.txt # Python 依赖

## 贡献指南
欢迎提交 Pull Request 或 Issue 来改进本项目。

## 许可证
本项目采用 MIT 许可证，详情请见 LICENSE 文件。
