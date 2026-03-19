# 🚀 Clarus 快速开始指南

## 5 分钟启动项目

### 第一次运行

#### 1. 安装后端依赖

```bash
cd D:\ai\Clarus\backend
setup.bat
```

这会自动：
- ✅ 创建虚拟环境
- ✅ 安装所有依赖
- ✅ 创建 `.env` 配置文件

#### 2. 配置 API Keys 和 KataGo

编辑 `backend\.env` 文件：

```env
# Gemini API（必须配置！）
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro

# KataGo 配置（可选，不配置将使用 Mock 数据）
KATAGO_PATH=C:\katago\katago.exe
KATAGO_CONFIG=C:\katago\analysis_config.cfg
KATAGO_MODEL=C:\katago\kata1-b40c256-s11840935168-d2898845681.bin.gz

# 安全配置
SECRET_KEY=your-secret-key-here
```

**关于 KataGo**:
- 如果不配置 KataGo，系统会自动使用 Mock 数据（演示模式）
- 要使用真实的围棋 AI 分析，请参考 `backend/KATAGO_SETUP.md` 安装 KataGo

#### 3. 启动后端服务器

```bash
cd D:\ai\Clarus\backend
start.bat
```

服务器将在 `http://localhost:8000` 启动

#### 4. 打开前端

双击打开 `D:\ai\Clarus\workspace-go.html`

或使用简单 HTTP 服务器：
```bash
cd D:\ai\Clarus
python -m http.server 8080
```

然后访问 `http://localhost:8080/workspace-go.html`

---

## ✅ 验证安装

### 检查后端健康状态

浏览器访问：`http://localhost:8000/api/go/health`

应该看到：
```json
{
  "status": "healthy",
  "agents": {
    "grandmaster": "ready",
    "scribe": "ready",
    "profiler": "ready",
    "arbiter": "ready",
    "delta_hunter": "ready"
  },
  "war_room": "operational"
}
```

### 测试分析功能

1. 打开 `workspace-go.html`
2. 保持默认值（着法 A: Q16, 着法 B: D4）
3. 点击"开始辩证分析"
4. 观察实时进度和最终结果

**注意**: 当前使用 Mock KataGo 数据，分析结果是演示性质的。

---

## 🔧 常见问题

### Q: 启动后端时报错 "No module named 'fastapi'"
**A**: 虚拟环境未激活或依赖未安装
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### Q: API 调用失败 "CORS error"
**A**: 检查 `.env` 中的 `CORS_ORIGINS` 包含你的前端地址
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://localhost:8080,http://127.0.0.1:8080
```

### Q: Gemini API 报错
**A**: 检查 API Key 是否正确配置，且有可用配额

### Q: 分析结果是假数据？
**A**: 如果未配置 KataGo，是的！系统会使用 Mock 数据演示工作流程。
要使用真实的 AI 分析，请按照 `backend/KATAGO_SETUP.md` 安装和配置 KataGo。

### Q: 如何启用真实的 KataGo 分析？
**A**: 按以下步骤：
1. 阅读 `backend/KATAGO_SETUP.md`
2. 下载 KataGo 和神经网络模型
3. 在 `.env` 中配置路径
4. 重启后端服务器

---

## 📚 下一步

- 阅读 [README.md](README.md) 了解完整架构
- 查看 [API 文档](http://localhost:8000/api/docs)
- **配置 KataGo** - 见 `backend/KATAGO_SETUP.md`（真实 AI 分析）
- 设置 PostgreSQL 数据库

---

## 🎯 项目状态（v2.0.0）

| 功能 | 状态 |
|------|------|
| 后端 API | ✅ 可运行 |
| 前端 UI | ✅ 完整（编辑模式、棋谱库、对话等） |
| Gemini 集成 | ✅ 已配置 |
| **KataGo 集成** | **✅ 完整实现**（需手动安装 KataGo） |
| 数据库 | 🚧 待实现 |
| Reconstruction Loop | ✅ 完整实现 |
| 差分热力图 | ✅ 三视图切换 |
| 术语提示 | ✅ 17+ 术语 |
| 苏格拉底对话 | ✅ 预设问题 + 自由追问 |
| 编辑模式 | ✅ 自由摆放棋子 |
| 棋谱库 | ✅ 6 个经典对局 |

---

**需要帮助？** 查看 [README.md](README.md) 的详细文档。
