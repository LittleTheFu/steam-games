# Steam 游戏游玩时间页面

在线页面：[https://littlethefu.github.io/steam-games/](https://littlethefu.github.io/steam-games/)

## 发布到 GitHub Pages

1. 在 GitHub 新建一个仓库，例如 `steam-games`。
2. 上传本目录中的 `index.html` 和 `games.csv`。
3. 打开仓库的 **Settings → Pages**，在 **Build and deployment** 中选择 **Deploy from a branch**，选 `main` 分支和 `/(root)`，保存。
4. 等待 Pages 部署完成后，页面地址会显示在 Pages 设置中，形式类似 `https://你的用户名.github.io/steam-games/`。

GitHub Free 需要公开仓库才能使用 Pages；发布出来的页面也会公开。上传前请确认愿意公开游戏清单和游玩时间。

## 自动同步

GitHub Actions 每天北京时间 02:00 从 Steam 同步一次，也可以在 Actions 页面手动运行。到 **Settings → Secrets and variables → Actions** 添加以下仓库 Secret：

- `STEAM_API_KEY`：Steam Web API Key
- `STEAM_ID`：Steam 账号 ID

同步会更新 `games.csv`。游戏图标优先使用 Steam 返回的图标，缺失时回退到商店图片。
