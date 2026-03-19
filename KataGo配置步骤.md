# 🚀 KataGo 配置步骤（3 分钟完成）

你已经下载了 KataGo，现在只需要 3 个简单步骤就能启用真实的 AI 围棋分析！

---

## 📋 准备工作检查

✅ KataGo 已下载到：`D:\ai\katago-v1.16.4-cuda12.8-cudnn9.8.0-windows-x64`

现在需要：
- [ ] 下载神经网络模型
- [ ] 生成配置文件
- [ ] 配置 Clarus 后端

---

## 步骤 1: 下载神经网络模型（2 分钟）

### 方法 A：自动下载（推荐）

双击运行：
```
D:\ai\katago-v1.16.4-cuda12.8-cudnn9.8.0-windows-x64\下载模型.bat
```

这会自动下载推荐的 40-block 模型（~200MB）。

### 方法 B：手动下载

如果自动下载失败，手动下载：

1. 打开浏览器，访问：
   ```
   https://media.katagotraining.org/uploaded/networks/models/kata1/kata1-b40c256-s11840935168-d2898845681.bin.gz
   ```

2. 保存文件到：
   ```
   D:\ai\katago-v1.16.4-cuda12.8-cudnn9.8.0-windows-x64\
   ```

3. 确认文件名为：
   ```
   kata1-b40c256-s11840935168-d2898845681.bin.gz
   ```

---

## 步骤 2: 运行配置脚本（30 秒）

模型下载完成后，双击运行：
```
D:\ai\Clarus\backend\setup_katago.bat
```

这个脚本会自动：
- ✅ 检查所有必需文件
- ✅ 生成 KataGo 配置文件
- ✅ 更新 Clarus 后端 .env 文件
- ✅ 测试 KataGo 是否正常工作

**重要**：配置过程中会询问一些 GPU 设置，直接按 Enter 使用默认值即可。

---

## 步骤 3: 启动 Clarus 并测试（1 分钟）

### 3.1 启动后端

打开命令行，运行：
```bash
cd D:\ai\Clarus\backend
python -m app.main
```

你应该看到：
```
[Clarus] Starting up...
[Clarus] Initializing KataGo client...
[KataGo] Starting engine: D:\ai\katago-v1.16.4-cuda12.8-cudnn9.8.0-windows-x64\katago.exe ...
[KataGo] Engine started successfully
[Clarus] KataGo client ready
```

### 3.2 测试前端分析

1. 打开浏览器，访问：
   ```
   http://localhost:8000/../workspace-go.html
   ```
   或直接双击打开：`D:\ai\Clarus\workspace-go.html`

2. 在编辑模式下放置几个棋子（或使用棋谱库）

3. 切换到分析模式

4. 点击两个位置作为着法 A 和着法 B

5. 点击"开始辩证分析"

6. **观察胜率和目数**：
   - ✅ 如果看到动态变化的数值（如 8.3%、-2.1 目等），说明 KataGo 工作正常！
   - ❌ 如果始终是 5.2% 和 4.5 目，说明仍在使用 Mock 数据

---

## ✅ 验证 KataGo 是否正常工作

### 测试方法 1：API 健康检查

访问：http://localhost:8000/api/go/health

应该看到：
```json
{
  "status": "healthy",
  "agents": {
    "grandmaster": "ready"
  }
}
```

### 测试方法 2：直接测试 KataGo

双击运行：
```
D:\ai\Clarus\backend\test_katago.bat
```

如果看到 JSON 输出包含 `winrate`、`scoreLead` 等字段，说明正常！

---

## 🐛 故障排除

### 问题 1：找不到 CUDA/GPU

**症状**：
```
Error: Could not find CUDA
```

**解决方案**：
- 确保安装了 NVIDIA GPU 驱动
- 或下载 CPU 版本的 KataGo（性能会慢一些）

### 问题 2：模型下载失败

**解决方案**：
- 使用方法 B 手动下载
- 或尝试其他镜像站点

### 问题 3：配置文件生成失败

**解决方案**：
```bash
cd D:\ai\katago-v1.16.4-cuda12.8-cudnn9.8.0-windows-x64
katago.exe genconfig -model kata1-b40c256-s11840935168-d2898845681.bin.gz -output analysis_config.cfg
```

按提示选择：
- Analysis engine: Yes
- Threads: 8-16（根据你的 CPU）
- 其他选项：按 Enter 使用默认值

### 问题 4：后端无法连接 KataGo

**检查 .env 文件**：
```bash
# 确认这些路径正确
KATAGO_PATH=D:\ai\katago-v1.16.4-cuda12.8-cudnn9.8.0-windows-x64\katago.exe
KATAGO_CONFIG=D:\ai\katago-v1.16.4-cuda12.8-cudnn9.8.0-windows-x64\analysis_config.cfg
KATAGO_MODEL=D:\ai\katago-v1.16.4-cuda12.8-cudnn9.8.0-windows-x64\kata1-b40c256-s11840935168-d2898845681.bin.gz
```

---

## 📊 性能优化建议

### 如果你有强大的 GPU（8GB+ 显存）

编辑 `analysis_config.cfg`：
```cfg
numSearchThreads = 16
nnCacheSizePowerOfTwo = 23
maxVisits = 10000
```

### 如果你的 GPU 较弱（4GB 显存）

```cfg
numSearchThreads = 8
nnCacheSizePowerOfTwo = 22
maxVisits = 5000
```

### 如果你只有 CPU

```cfg
numSearchThreads = 4
nnCacheSizePowerOfTwo = 20
maxVisits = 2000
```

---

## 🎉 完成！

配置完成后，你的 Clarus 系统将使用真实的 KataGo 引擎进行分析：

- ✅ **真实胜率分析** - 精确到小数点后两位
- ✅ **真实目数评估** - 反映实际盘面价值
- ✅ **真实所有权图** - 361 个交叉点的概率分布
- ✅ **主变化推荐** - KataGo 的最佳后续手
- ✅ **策略图** - 每个位置的着法概率

享受超级人类级别的围棋 AI 分析吧！🎊

---

**需要帮助？** 查看：
- `backend/KATAGO_SETUP.md` - 完整技术文档
- `QUICKSTART.md` - 快速开始指南
- `README.md` - 项目架构说明
