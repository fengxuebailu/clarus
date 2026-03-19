# KataGo 安装和配置指南

本指南将帮助你配置 KataGo Analysis Engine 以与 Clarus 后端集成。

## 步骤 1: 下载 KataGo

### Windows

1. 访问 KataGo 发布页面：
   ```
   https://github.com/lightvector/KataGo/releases
   ```

2. 下载最新版本的 Windows 可执行文件：
   - 对于 NVIDIA GPU: `katago-vX.X.X-cuda-windows-x64.zip`
   - 对于 AMD GPU: `katago-vX.X.X-opencl-windows-x64.zip`
   - 对于 CPU only: `katago-vX.X.X-eigen-windows-x64.zip`

3. 解压到目录（例如 `C:\katago`）

### Linux/Mac

```bash
# 下载 KataGo
wget https://github.com/lightvector/KataGo/releases/download/v1.14.0/katago-v1.14.0-cuda11.8-linux-x64.zip

# 解压
unzip katago-v1.14.0-cuda11.8-linux-x64.zip -d ~/katago

# 添加执行权限
chmod +x ~/katago/katago
```

## 步骤 2: 下载神经网络模型

KataGo 需要一个训练好的神经网络模型。

```bash
cd ~/katago

# 下载 40 block 模型（推荐，适合大多数硬件）
wget https://media.katagotraining.org/uploaded/networks/models/kata1/kata1-b40c256-s11840935168-d2898845681.bin.gz

# 或下载更小的 20 block 模型（更快，精度稍低）
# wget https://media.katagotraining.org/uploaded/networks/models/kata1/kata1-b20c256x2-s5303129600-d1228401921.bin.gz
```

**Windows 用户**：将文件下载到 `C:\katago\` 目录

## 步骤 3: 生成配置文件

KataGo 需要一个配置文件来运行 Analysis Engine。

```bash
cd ~/katago

# 生成配置文件（会询问你的硬件配置）
./katago genconfig -model kata1-b40c256-s11840935168-d2898845681.bin.gz -output analysis_config.cfg
```

**重要提示**：
- 选择 **Analysis** 模式
- 根据你的 GPU 内存调整 `maxVisits` 和 `numSearchThreads`
- 推荐设置：
  - GPU 8GB+: `numSearchThreads = 16`, `maxVisits = 10000`
  - GPU 4GB: `numSearchThreads = 8`, `maxVisits = 5000`
  - CPU only: `numSearchThreads = 4`, `maxVisits = 2000`

## 步骤 4: 配置环境变量

### 方法 A: 在 `.env` 文件中配置

编辑 `backend/.env` 文件：

```env
# KataGo 路径配置
KATAGO_PATH=C:\katago\katago.exe           # Windows
# KATAGO_PATH=/home/user/katago/katago    # Linux/Mac

KATAGO_CONFIG=C:\katago\analysis_config.cfg
KATAGO_MODEL=C:\katago\kata1-b40c256-s11840935168-d2898845681.bin.gz

# KataGo Analysis Engine 配置
KATAGO_TIMEOUT=30
MAX_VISITS=10000
```

### 方法 B: 使用系统环境变量

**Windows**:
```cmd
setx KATAGO_PATH "C:\katago\katago.exe"
setx KATAGO_CONFIG "C:\katago\analysis_config.cfg"
setx KATAGO_MODEL "C:\katago\kata1-b40c256-s11840935168-d2898845681.bin.gz"
```

**Linux/Mac**:
```bash
export KATAGO_PATH="$HOME/katago/katago"
export KATAGO_CONFIG="$HOME/katago/analysis_config.cfg"
export KATAGO_MODEL="$HOME/katago/kata1-b40c256-s11840935168-d2898845681.bin.gz"

# 添加到 ~/.bashrc 或 ~/.zshrc 以永久保存
```

## 步骤 5: 测试 KataGo

### 测试 1: 命令行测试

```bash
cd ~/katago
./katago analysis -config analysis_config.cfg -model kata1-b40c256-s11840935168-d2898845681.bin.gz
```

然后输入测试请求：
```json
{"id":"test","moves":[["B","Q16"],["W","D4"]],"rules":"chinese","komi":7.5,"boardXSize":19,"boardYSize":19,"maxVisits":100}
```

按 Enter 键，你应该会看到 KataGo 返回的 JSON 响应。

按 Ctrl+C 退出。

### 测试 2: Python 集成测试

创建测试脚本 `test_katago.py`：

```python
import asyncio
import sys
sys.path.append('D:/ai/Clarus/backend')

from app.core.katago_client import KataGoClient

async def test_katago():
    async with KataGoClient() as katago:
        # 测试分析空棋盘的第一手棋
        result = await katago.analyze_position(
            moves=[("B", "Q16")],
            max_visits=100
        )

        print(f"Winrate: {result['winrate']:.2%}")
        print(f"Score Lead: {result['scoreLead']:.2f}")
        print(f"Top moves: {result['pv'][:5]}")

if __name__ == "__main__":
    asyncio.run(test_katago())
```

运行测试：
```bash
python test_katago.py
```

预期输出：
```
[KataGo] Starting engine: ...
[KataGo] Engine started successfully
Winrate: 51.23%
Score Lead: 0.85
Top moves: ['D4', 'D16', 'Q4', 'Q3', 'D3']
[KataGo] Stopping engine...
[KataGo] Engine stopped
```

## 步骤 6: 启动 Clarus 后端

```bash
cd D:/ai/Clarus/backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 API 文档查看 KataGo 状态：
```
http://localhost:8000/api/go/health
```

## 故障排除

### 问题 1: KataGo 找不到

**错误**: `FileNotFoundError: KataGo executable not found`

**解决方案**:
- 确认 KataGo 路径正确
- 检查环境变量 `KATAGO_PATH`
- 在 Windows 上确保使用 `.exe` 扩展名

### 问题 2: 配置文件无效

**错误**: `FileNotFoundError: KataGo config file not found`

**解决方案**:
- 运行 `katago genconfig` 生成配置文件
- 确认 `KATAGO_CONFIG` 路径正确

### 问题 3: 模型文件缺失

**错误**: `FileNotFoundError: KataGo model file not found`

**解决方案**:
- 下载神经网络模型（见步骤 2）
- 确认 `KATAGO_MODEL` 路径正确
- 确保文件扩展名是 `.bin.gz`

### 问题 4: KataGo 启动超时

**错误**: `asyncio.TimeoutError`

**解决方案**:
- 增加 `KATAGO_TIMEOUT` 值（默认 30 秒）
- 检查 GPU 驱动是否正确安装
- 对于 CPU-only 版本，第一次启动可能需要更长时间

### 问题 5: GPU 内存不足

**错误**: `CUDA out of memory`

**解决方案**:
- 编辑 `analysis_config.cfg`，减少 `nnCacheSizePowerOfTwo`
- 减少 `maxVisits`（例如从 10000 降到 5000）
- 使用更小的神经网络模型（20 block 而不是 40 block）

## 性能优化

### GPU 用户

在 `analysis_config.cfg` 中调整：

```cfg
# 使用多个搜索线程（推荐 GPU 内存 > 8GB）
numSearchThreads = 16

# 增加神经网络缓存（加速重复局面分析）
nnCacheSizePowerOfTwo = 23  # 8GB GPU
# nnCacheSizePowerOfTwo = 22  # 4GB GPU
# nnCacheSizePowerOfTwo = 21  # 2GB GPU
```

### CPU 用户

```cfg
numSearchThreads = 4  # 根据 CPU 核心数调整
nnCacheSizePowerOfTwo = 20
maxVisits = 2000  # CPU 模式下降低访问次数
```

## 验证安装成功

访问 Clarus 前端：
```
http://localhost:8000/../workspace-go.html
```

1. 在编辑模式下放置两个棋子
2. 切换到分析模式，选择着法 A 和着法 B
3. 点击"开始辩证分析"
4. 观察右侧面板是否显示真实的胜率和目数差异（而不是固定的 5.2% 和 4.5 目）

如果看到动态变化的数值和有意义的所有权图，说明 KataGo 集成成功！

## 进一步阅读

- KataGo 官方文档: https://github.com/lightvector/KataGo
- Analysis Engine 详细说明: https://github.com/lightvector/KataGo/blob/master/docs/Analysis_Engine.md
- GTP 协议参考: https://www.lysator.liu.se/~gunnar/gtp/gtp2-spec-draft2/gtp2-spec.html
